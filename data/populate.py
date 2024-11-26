from db import DB
import pandas as pd

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
    db_mongo.users.insert_one(user)
for i in range(len(datasetMongoTweets)):
    tweet = datasetMongoTweets.iloc[i].to_dict()
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