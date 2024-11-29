import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import DB
import pandas as pd
from datetime import datetime
from cassandra.query import BoundStatement

db_instance = DB()
db_instance.connect_cassandra()
db_instance.connect_mongo()
db_instance.connect_dgraph()

datasetMongoUsers = pd.read_json('data/data_mongo_users.json')
datasetMongoTweets = pd.read_json('data/data_mongo_tweets.json')
datasetCassandra = pd.read_json('data/data_cassandra.json')
# datasetDgraphUsers = pd.read_json('data/data_dgraph_users.json')
# datasetDgraphTweets = pd.read_json('data/data_dgraph_tweets.json')
# datasetDgraphHashtags = pd.read_json('data/data_dgraph_hashtags.json')

db_cassandra = db_instance.get_db('cassandra')

def parse_date(date_str):
    date_formats = [
        '%Y-%m-%dT%H:%M:%S.%fZ',  # ISO format with milliseconds
        '%Y-%m-%dT%H:%M:%SZ',     # ISO format without milliseconds
        '%Y-%m-%d %H:%M:%S',      # Standard datetime format
        '%Y-%m-%d'                # Date only
    ]
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    raise ValueError(f"Unable to parse date: {date_str}")


for i in range(len(datasetCassandra)):
    user = datasetCassandra.iloc[i].to_dict()

    if isinstance(user['user_created_at'], str):
        try:
            user['user_created_at'] = parse_date(user['user_created_at'])
        except ValueError:
            print(f"Warning: Could not parse date for user {user.get('user_username', 'Unknown')}: {user['user_created_at']}")
            continue

    prepared_stmt = db_cassandra.prepare("""
        INSERT INTO users (
            author_id,
            user_username, 
            user_created_at, 
            user_followers_count, 
            user_tweet_count, 
            user_name
        ) VALUES (?, ?, ?, ?, ?, ?)
    """)
    
    db_cassandra.execute(prepared_stmt, (
        str(user['author_id']),  # Now first in the list to match new PRIMARY KEY
        str(user['user_username']),  
        user['user_created_at'],
        int(user['user_followers_count']),  
        int(user['user_tweet_count']),  
        str(user['user_name'])  
    ))

for i in range(len(datasetCassandra)):
    tweet = datasetCassandra.iloc[i].to_dict()

    if isinstance(tweet['created_at'], str):
        tweet['created_at'] = parse_date(tweet['created_at'])

    prepared_stmt = db_cassandra.prepare("""
        INSERT INTO tweets (
            author_id, 
            created_at, 
            sentiment, 
            id, 
            text, 
            retweet_count, 
            reply_count, 
            like_count, 
            quote_count, 
            source, 
            user_username
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """)

    db_cassandra.execute(prepared_stmt, (
        str(tweet['author_id']),  # Ensure string
        tweet['created_at'],
        str(tweet['sentiment']),  # Ensure string
        str(tweet['id']),  # Ensure string
        str(tweet['text']),  # Ensure string
        int(tweet['retweet_count']),  # Ensure integer
        int(tweet['reply_count']),  # Ensure integer
        int(tweet['like_count']),  # Ensure integer
        int(tweet['quote_count']),  # Ensure integer
        str(tweet['source']),  # Ensure string
        str(tweet['user_username'])  # Ensure string
    ))


# insertar datos a mongo
# db_mongo = db_instance.get_db('mongo')
# for i in range(len(datasetMongoUsers)):
#     user = datasetMongoUsers.iloc[i].to_dict()
#     # Convert types
#     if isinstance(user['created_at'], str):
#         user['created_at'] = datetime.strptime(user['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
#     user['public_metrics'] = {
#         'followers_count': int(user['public_metrics']['followers_count']),
#         'following_count': int(user['public_metrics']['following_count']),
#         'tweet_count': int(user['public_metrics']['tweet_count']),
#         'listed_count': int(user['public_metrics']['listed_count'])
#     }
#     db_mongo.users.insert_one(user)

# for i in range(len(datasetMongoTweets)):
#     tweet = datasetMongoTweets.iloc[i].to_dict()
#     # Convert types
#     if isinstance(tweet['created_at'], str):
#         tweet['created_at'] = datetime.strptime(tweet['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
#     if isinstance(tweet['user_created_at'], str):
#         tweet['user_created_at'] = datetime.strptime(tweet['user_created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
#     tweet['retweet_count'] = int(tweet['retweet_count'])
#     tweet['reply_count'] = int(tweet['reply_count'])
#     tweet['like_count'] = int(tweet['like_count'])
#     tweet['quote_count'] = int(tweet['quote_count'])
#     tweet['user_followers_count'] = int(tweet['user_followers_count'])
#     tweet['user_tweet_count'] = int(tweet['user_tweet_count'])
#     tweet['hashtags'] = list(tweet['hashtags'])
#     tweet['mentions'] = list(tweet['mentions'])
#     tweet['urls'] = list(tweet['urls'])
#     tweet['Embedding'] = list(map(float, tweet['Embedding']))
#     tweet['embeddingsReducidos'] = list(map(float, tweet['embeddingsReducidos']))
#     db_mongo.tweets.insert_one(tweet)

# insertar datos a dgraph
# db_dgraph = db_instance.get_db('dgraph')
# for i in range(len(datasetDgraphUsers)):
#     user = datasetDgraphUsers.iloc[i].to_dict()
#     txn = db_dgraph.txn()
#     try:
#         txn.mutate(set_obj=user)
#         txn.commit()
#     finally:
#         txn.discard()
# for i in range(len(datasetDgraphTweets)):
#     tweet = datasetDgraphTweets.iloc[i].to_dict()
#     txn = db_dgraph.txn()
#     try:
#         txn.mutate(set_obj=tweet)
#         txn.commit()
#     finally:
#         txn.discard()
# for i in range(len(datasetDgraphHashtags)):
    # hashtag = datasetDgraphHashtags.iloc[i].to_dict()
    # txn = db_dgraph.txn()
    # try:
    #     txn.mutate(set_obj=hashtag)
    #     txn.commit()
    # finally:
    #     txn.discard()