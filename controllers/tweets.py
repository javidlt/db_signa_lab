class TweetsControllers:
    def __init__(self, db):
        self.db = db
        self.mongo = db.get_db('mongo')
        self.cassandra = db.get_db('cassandra')
        self.dgraph = db.get_db('dgraph')

    def get_tweets(self):
        pass

    def get_tweet(self):
        pass

    def create_tweet(self):
        pass

    def delete_tweet(self):
        pass

    def update_tweet(self):
        pass

    def get_tweets_by_topic(self, topic):
        query = f"""
        {{
            tweets(func: eq(topic, "{topic}")) {{
                tweet_id
                text
                author {{
                    username
                }}
                liked_by {{
                    username
                }}
                retweeted_by {{
                    username
                }}
                replies {{
                    tweet_id
                    text
                    topic
                }}
            }}
        }}
        """
        response = self.dgraph.txn(read_only=True).query(query)
        return response.json()
    
    def get_tweets_by_user(self, username):
        query = f"""
        {{
            user(func: eq(username, "{username}")) {{
                uid
                username
                tweets {{
                    tweet_id
                    text
                    topic
                    liked_by {{
                        username
                    }}
                    retweeted_by {{
                        username
                    }}
                    replies {{
                        tweet_id
                        text
                        topic
                    }}
                }}
            }}
        }}
        """
        response = self.dgraph.txn(read_only=True).query(query)
        return response.json()