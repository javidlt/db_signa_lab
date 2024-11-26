from fastapi.responses import JSONResponse

class HashtagControllers:
    def __init__(self, db):
        self.db = db
        self.mongo = db.get_db('mongo')
        self.cassandra = db.get_db('cassandra')
        self.dgraph = db.get_db('dgraph')

    def get_hashtags(self):
        hashtags = []  
        return JSONResponse(content={"hashtags": hashtags})

    def get_hashtag(self):
        pass

    def create_hashtag(self):
        pass

    def delete_hashtag(self):
        pass

    def update_hashtag(self):
        pass

    def get_tweets(self):
        pass