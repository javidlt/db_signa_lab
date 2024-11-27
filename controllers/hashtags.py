from fastapi.responses import JSONResponse

class HashtagControllers:
    def __init__(self, db):
        self.db = db
        self.mongo = db.get_db('mongo')
        self.cassandra = db.get_db('cassandra')
        self.dgraph = db.get_db('dgraph')

    def get_hashtags(self):
        # TODO: Implement get_hashtags method with dgraph
        hashtags = []  
        return JSONResponse(content={"hashtags": hashtags})

    def get_hashtag(self):
        # TODO: Implement get_hashtag method with dgraph
        pass

    def create_hashtag(self):
        # TODO: Implement create_hashtag method with dgraph
        pass

    def delete_hashtag(self):
        # TODO: Implement delete_hashtag method with dgraph
        pass

    def update_hashtag(self):
        # TODO: Implement update_hashtag method with dgraph
        pass

    def get_tweets(self):
        # TODO: Implement get_tweets method with dgraph
        pass