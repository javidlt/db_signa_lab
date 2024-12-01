import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import DB
import pandas as pd
from datetime import datetime
from cassandra.query import BatchStatement

db_instance = DB()
db_instance.connect_cassandra()
db_instance.connect_mongo()
db_instance.connect_dgraph()

datasetMongoUsers = pd.read_json('data/data_mongo_users.json')
datasetMongoTweets = pd.read_json('data/data_mongo_tweets.json')
datasetDgraphUsers = pd.read_json('data/data_dgraph_users.json')
datasetDgraphTweets = pd.read_json('data/data_dgraph_tweets.json')
datasetDgraphHashtags = pd.read_json('data/data_dgraph_hashtags.json')

db_cassandra = db_instance.get_db('cassandra')

def process_tweet_date(timestamp_ms):
    timestamp_seconds = timestamp_ms.timestamp()
    dt = datetime.fromtimestamp(timestamp_seconds)

    return {
        'year': dt.year,
        'month': dt.month,
        'day': dt.day,
        'datetime': dt
    }

#populates de cassandra
def populate_tweets_by_created_at(datasetMongoTweets, db_cassandra):
    batch = BatchStatement()
    prepared_stmt = db_cassandra.prepare("""
        INSERT INTO tweets_by_created_at (
            year, 
            month, 
            day, 
            created_at, 
            text, 
            retweet_count, 
            reply_count, 
            like_count, 
            user_username
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """)

    for i in range(len(datasetMongoTweets)):
        tweet = datasetMongoTweets.iloc[i].to_dict()
        dt = process_tweet_date(tweet['created_at'])
        
        batch.add(prepared_stmt, (
            dt['year'],               
            dt['month'],              
            dt['day'],                
            dt['datetime'],               
            tweet['text'],     
            tweet['retweet_count'],  
            tweet['reply_count'],    
            tweet['like_count'],    
            tweet['user_username']  
        ))

        # Ejecuta el batch cada 100 inserciones para no saturar la memoria
        if (i + 1) % 100 == 0:
            db_cassandra.execute(batch)
            batch = BatchStatement()

    # Ejecuta cualquier inserción restante
    if batch:
        db_cassandra.execute(batch)

def populate_user_followers(datasetMongoUsers, db_cassandra):
    batch = BatchStatement()
    prepared_stmt = db_cassandra.prepare(""" 
        INSERT INTO user_followers (
            year,
            month,
            day,
            username, 
            user_id, 
            name, 
            location, 
            followers_count, 
            following_count, 
            tweet_count,
            listed_count
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """)

    for i in range(len(datasetMongoUsers)):
        user = datasetMongoUsers.iloc[i].to_dict()
        dt = process_tweet_date(user['created_at'])

        batch.add(prepared_stmt, (
            dt['year'],               
            dt['month'],              
            dt['day'],
            user['username'],                               
            str(user['id']),  
            user['name'],  
            user['location'],  
            user['public_metrics']['followers_count'],    
            user['public_metrics']['following_count'],
            user['public_metrics']['tweet_count'],
            user['public_metrics']['listed_count']         
        ))

        if (i + 1) % 100 == 0:
            db_cassandra.execute(batch)
            batch = BatchStatement()

    if batch:
        db_cassandra.execute(batch)

populate_tweets_by_created_at(datasetMongoTweets, db_cassandra)
populate_user_followers(datasetMongoUsers, db_cassandra)

db_mongo = db_instance.get_db('mongo')
for i in range(len(datasetMongoUsers)):
    user = datasetMongoUsers.iloc[i].to_dict()
    # Convert types
    if isinstance(user['created_at'], str):
        user['created_at'] = datetime.strptime(user['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
    user['public_metrics'] = {
        'followers_count': int(user['public_metrics']['followers_count']),
        'following_count': int(user['public_metrics']['following_count']),
        'tweet_count': int(user['public_metrics']['tweet_count']),
        'listed_count': int(user['public_metrics']['listed_count'])
    }
    db_mongo.users.insert_one(user)

for i in range(len(datasetMongoTweets)):
    tweet = datasetMongoTweets.iloc[i].to_dict()
    # Convert types
    if isinstance(tweet['created_at'], str):
        tweet['created_at'] = datetime.strptime(tweet['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
    if isinstance(tweet['user_created_at'], str):
        tweet['user_created_at'] = datetime.strptime(tweet['user_created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
    tweet['retweet_count'] = int(tweet['retweet_count'])
    tweet['reply_count'] = int(tweet['reply_count'])
    tweet['like_count'] = int(tweet['like_count'])
    tweet['quote_count'] = int(tweet['quote_count'])
    tweet['user_followers_count'] = int(tweet['user_followers_count'])
    tweet['user_tweet_count'] = int(tweet['user_tweet_count'])
    tweet['hashtags'] = list(tweet['hashtags'])
    tweet['mentions'] = list(tweet['mentions'])
    tweet['urls'] = list(tweet['urls'])
    tweet['Embedding'] = list(map(float, tweet['Embedding']))
    tweet['embeddingsReducidos'] = list(map(float, tweet['embeddingsReducidos']))
    db_mongo.tweets.insert_one(tweet)

db_dgraph = db_instance.get_db('dgraph')
for i in range(len(datasetDgraphUsers)):
    user = datasetDgraphUsers.iloc[i].to_dict()
    txn = db_dgraph.txn()
    try:
        txn.mutate(set_obj=user)
        txn.commit()
    finally:
        txn.discard()
for i in range(len(datasetDgraphTweets)):
    tweet = datasetDgraphTweets.iloc[i].to_dict()
    txn = db_dgraph.txn()
    try:
        txn.mutate(set_obj=tweet)
        txn.commit()
    finally:
        txn.discard()
for i in range(len(datasetDgraphHashtags)):
    hashtag = datasetDgraphHashtags.iloc[i].to_dict()
    txn = db_dgraph.txn()
    try:
        txn.mutate(set_obj=hashtag)
        txn.commit()
    finally:
        txn.discard()