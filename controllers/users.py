from bson import ObjectId
from schemas.schema import UserModel

class UserController:
    def __init__(self, db):
        self.db = db
        self.mongo = db.get_db('mongo')
        self.cassandra = db.get_db('cassandra')
        self.dgraph = db.get_db('dgraph')

    async def get_users(self):
        # TODO: Implement get_users method with cassandra
        pass

    async def get_user(self, user_id: str):
        # TODO: Implement get_user method with cassandra
        pass

    async def delete_user(self, user_id: str):
        result = self.mongo.users.delete_one({"_id": ObjectId(user_id)})
        # TODO: Delete user in Dgraph
        # TODO: Delete user in Cassandra
        if result.deleted_count:
            return {"message": "User deleted successfully"}
        else:
            return {"message": "User not found"}

    async def update_user(self, user_id: str, user_data: dict):
        update_fields = {k: v for k, v in user_data.items() if v is not None}
        result = self.mongo.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_fields})
        # TODO: Update user in Dgraph
        # TODO: Update user in Cassandra
        if result.matched_count:
            return {"message": "User updated successfully"}
        else:
            return {"message": "User not found"}

    async def create_user(self, user_data: dict):
        user = UserModel(**user_data)
        result = self.mongo.users.insert_one(user.dict(exclude_unset=True))
        created_user = self.mongo.users.find_one({"_id": result.inserted_id})
        if created_user:
            created_user["_id"] = str(created_user["_id"])
        # TODO: Add user to Dgraph
        # TODO: Add user to Cassandra
        return created_user
    
    async def get_user_tweets(self, user_id: str):
        # TODO: Implement get_user_tweets method with dgraph
        pass