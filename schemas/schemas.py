import pydgraph

class Schema:
    def __init__(self, db):
        self.db = db
        self.MongoUser = self.UserMongo()
        self.MongoTweet = self.TweetMongo()
        self.CassandraUser = self.UserCassandra()
        self.CassandraTweet = self.TweetCassandra()
        self.DgraphUser = self.UserDgraph()
        self.DgraphTweet = self.TweetDgraph()
        self.DgraphHashtag = self.HashtagDgraph()
    
    def UserMongo(self):
        return {
            # Define MongoDB user schema
        }
    
    def TweetMongo(self):
        return {
            # Define MongoDB tweet schema
        }
    
    def UserCassandra(self):
        # Define Cassandra user schema
        return """
        """
    
    def TweetCassandra(self):
        # Define Cassandra tweet schema
        return """
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
        session.execute(self.UserCassandra())
        session.execute(self.TweetCassandra())

    def execute_dgraph(self):
        client = self.db.get_db('dgraph')
        schema = self.UserDgraph() + self.TweetDgraph() + self.HashtagDgraph()
        op = pydgraph.Operation(schema=schema)
        client.alter(op)