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