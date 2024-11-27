import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import DB
import pandas as pd
from datetime import datetime

db_instance = DB()
db_instance.connect_cassandra()
db_instance.connect_mongo()
db_instance.connect_dgraph()

datasetMongoUsers = pd.read_json('data/data_mongo_users.json')
datasetMongoTweets = pd.read_json('data/data_mongo_tweets.json')
datasetCassandraUsers = pd.read_json('data/data_cassandra_users.json')
datasetCassandraTweets = pd.read_json('data/data_cassandra_tweets.json')
datasetDgraphUsers = pd.read_json('data/data_dgraph_users.json')
datasetDgraphTweets = pd.read_json('data/data_dgraph_tweets.json')
datasetDgraphHashtags = pd.read_json('data/data_dgraph_hashtags.json')

# insertar datos a cassandra
db_cassandra = db_instance.get_db('cassandra')
for i in range(len(datasetCassandraUsers)):
    user = datasetCassandraUsers.iloc[i].to_dict()
    db_cassandra.execute(
        """
        INSERT INTO users (id, name, email) VALUES (%s, %s, %s)
        """,
        (user['id'], user['name'], user['email'])
    )
for i in range(len(datasetCassandraTweets)):
    tweet = datasetCassandraTweets.iloc[i].to_dict()
    db_cassandra.execute(
        """
        INSERT INTO tweets (id, user_id, content) VALUES (%s, %s, %s)
        """,
        (tweet['id'], tweet['user_id'], tweet['content'])
    )

# insertar datos a mongo
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

# insertar datos a dgraph
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