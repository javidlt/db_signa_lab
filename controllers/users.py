class UserController:
    def __init__(self, db):
        self.db = db
        self.mongo = db.get_db('mongo')
        self.cassandra = db.get_db('cassandra')
        self.dgraph = db.get_db('dgraph')

    async def get_users(self):
        pass

    async def get_user(self):
        pass

    async def delete_user(self):
        pass

    async def update_user(self):
        pass
    
    async def create_user(self):
        pass
    
    def get_user_interactions(self, username):
        query = f"""
        {{
            user(func: eq(username, "{username}")) {{
                uid
                username
                liked_tweets: ~liked_by {{
                    tweet_id
                    text
                    author {{
                        username
                    }}
                    topic
                }}
                retweeted_tweets: ~retweeted_by {{
                    tweet_id
                    text
                    author {{
                        username
                    }}
                    topic
                }}
            }}
        }}
        """
        response = self.dgraph.txn(read_only=True).query(query)
        return response.json()