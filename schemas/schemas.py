import pydgraph
from pydantic import BaseModel

class Schema:
    def __init__(self, db):
        self.db = db
        self.MongoUser = self.UserMongo()
        self.MongoTweet = self.TweetMongo()
        self.CassandraTweetByDate = self.cass_tweets_by_created_at()
        self.CassandraUserFollowers = self.cass_user_followers()
        self.DgraphUser = self.UserDgraph()
        self.DgraphTweet = self.TweetDgraph()
        self.DgraphHashtag = self.HashtagDgraph()
    
    def UserMongo(self):
        return {
            'created_at': {
                'type': 'date'
            },
            'name': {
                'type': 'string'
            },
            'id': {
                'type': 'string'
            },
            'public_metrics': {
                'type': 'object',
                'properties': {
                    'followers_count': {'type': 'integer'},
                    'following_count': {'type': 'integer'},
                    'tweet_count': {'type': 'integer'},
                    'listed_count': {'type': 'integer'}
                }
            },
            'username': {
                'type': 'string'
            },
            'location': {
                'type': 'string'
            }
        }
    
    def TweetMongo(self):
        return {
            'text': {
                'type': 'string'
            },
            'id': {
                'type': 'string'
            },
            'created_at': {
                'type': 'date'
            },
            'source': {
                'type': 'string'
            },
            'retweet_count': {
                'type': 'integer'
            },
            'reply_count': {
                'type': 'integer'
            },
            'like_count': {
                'type': 'integer'
            },
            'quote_count': {
                'type': 'integer'
            },
            'author_id': {
                'type': 'string'
            },
            'user_name': {
                'type': 'string'
            },
            'user_username': {
                'type': 'string'
            },
            'user_created_at': {
                'type': 'date'
            },
            'user_followers_count': {
                'type': 'integer'
            },
            'user_tweet_count': {
                'type': 'integer'
            },
            'hashtags': {
                'type': 'array',
                'items': {
                    'type': 'string'
                }
            },
            'mentions': {
                'type': 'array',
                'items': {
                    'type': 'string'
                }
            },
            'urls': {
                'type': 'array',
                'items': {
                    'type': 'string'
                }
            },
            'sentiment': {
                'type': 'string'
            },
            'Embedding': {
                'type': 'array',
                'items': {
                    'type': 'number'
                }
            },
            'embeddingsReducidos': {
                'type': 'array',
                'items': {
                    'type': 'number'
                }
            }
        }
    
    #TABLAS CASSANDRA

    # puedo hacer queries por fecha (tweet)
    def cass_tweets_by_created_at(self): 
        return """
        CREATE TABLE IF NOT EXISTS tweets_by_created_at (
            year int,
            month int,
            day int,
            created_at timestamp,
            text text,
            retweet_count int,
            reply_count int,
            like_count int,
            user_username text,
            PRIMARY KEY ((year, month, day), created_at)
        ) WITH CLUSTERING ORDER BY (created_at DESC);
        """
    
    #consultar a los usuarios en base a sus seguidores
    def cass_user_followers(self):
        return """
        CREATE TABLE IF NOT EXISTS user_followers (
            year int,
            month int,
            day int,
            username text,
            user_id text,
            name text,
            location text,
            followers_count int,
            following_count int,
            tweet_count int,
            listed_count int,
            PRIMARY KEY (year, followers_count)
        ) WITH CLUSTERING ORDER BY (followers_count DESC);
        """

    def UserDgraph(self):
        # Define Dgraph user schema
        return """
        """
    
    def TweetDgraph(self):
        # Define Dgraph tweet schema
        return """
        """
    
    def HashtagDgraph(self):
        # Define Dgraph hashtag schema
        return """
        """

    def execute_mongo(self):
        db = self.db.get_db('mongo')
        if 'users' not in db.list_collection_names():
            db.create_collection('users')
        if 'tweets' not in db.list_collection_names():
            db.create_collection('tweets')

    def execute_cassandra(self):
        session = self.db.get_db('cassandra')
        session.execute(self.cass_tweets_by_created_at())
        session.execute(self.cass_user_followers())
        
    def execute_dgraph(self):
        client = self.db.get_db('dgraph')
        schema = self.UserDgraph() + self.TweetDgraph() + self.HashtagDgraph()
        op = pydgraph.Operation(schema=schema)
        client.alter(op)