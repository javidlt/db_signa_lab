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