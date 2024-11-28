from bson import ObjectId
from schemas.schema import UserModel
import pydgraph

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
        if result.deleted_count:
            # Delete user in Dgraph
            txn = self.dgraph.txn()
            try:
                query = f"""
                {{
                    user as var(func: eq(user_id, "{user_id}"))
                }}
                """
                mutation = pydgraph.Mutation(del_nquads=f"uid(user) <user_id> * .")
                txn.mutate(mutation=mutation, commit_now=True)
            finally:
                txn.discard()
        # TODO: Delete user in Cassandra
            return {"message": "User deleted successfully"}
        else:
            return {"message": "User not found"}

    async def update_user(self, user_id: str, user_data: dict):
        update_fields = {k: v for k, v in user_data.items() if v is not None}
        result = self.mongo.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_fields})
        if result.matched_count:
            # Update user in Dgraph
            txn = self.dgraph.txn()
            try:
                nquads = ""
                for key, value in update_fields.items():
                    nquads += f'<_:user> <{key}> "{value}" .\n'
                mutation = pydgraph.Mutation(set_nquads=nquads)
                txn.mutate(mutation=mutation, commit_now=True)
            finally:
                txn.discard()
        # TODO: Update user in Cassandra
            return {"message": "User updated successfully"}
        else:
            return {"message": "User not found"}

    async def create_user(self, user_data: dict):
        user = UserModel(**user_data)
        result = self.mongo.users.insert_one(user.dict(exclude_unset=True))
        created_user = self.mongo.users.find_one({"_id": result.inserted_id})
        if created_user:
            created_user["_id"] = str(created_user["_id"])
            #Add user to Dgraph
            txn = self.dgraph.txn()
            try:
                nquads = f"""
                _:user <user_id> "{created_user['_id']}" .
                _:user <name> "{created_user['name']}" .
                """
                mutation = pydgraph.Mutation(set_nquads=nquads)
                txn.mutate(mutation=mutation, commit_now=True)
            finally:
                txn.discard()
        # TODO: Add user to Cassandra
        return created_user
    
    async def get_user_tweets(self, user_id: str):
        # Implement get_user_tweets method with dgraph
        pass
        query = f"""
        {{
            user(func: eq(user_id, "{user_id}")) {{
            uid
            tweets {{
                tweet_id
                content
                timestamp
            }}
            }}
        }}
        """
        txn = self.dgraph.txn(read_only=True)
        try:
            response = txn.query(query)
            user_data = response.json
            return user_data
        finally:
            txn.discard()