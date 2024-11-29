from bson import ObjectId
from schemas.schema import UserModel
from datetime import datetime


class UserController:
    def __init__(self, db):
        self.db = db
        self.mongo = db.get_db('mongo')
        self.cassandra = db.get_db('cassandra')
        self.dgraph = db.get_db('dgraph')

    # TODO: Hacer que los filtros funcionen
    async def get_users(self, 
        author_id: str = None, 
        username: str = None, 
        min_followers: int = None, 
        max_followers: int = None, 
        min_tweets: int = None, 
        max_tweets: int = None,
        created_after: datetime = None,
        created_before: datetime = None,
        limit: int = 10,
        page: int = 1
    ):
        try:
            base_query = "SELECT * FROM users"
            where_clauses = []
            params = []

            if author_id:
                where_clauses.append("author_id = %s")
                params.append(author_id)

            if username:
                where_clauses.append("user_username LIKE %s")
                params.append(f"%{username}%")

            if min_followers is not None:
                where_clauses.append("user_followers_count >= %s")
                params.append(min_followers)

            if max_followers is not None:
                where_clauses.append("user_followers_count <= %s")
                params.append(max_followers)

            if min_tweets is not None:
                where_clauses.append("user_tweet_count >= %s")
                params.append(min_tweets)

            if max_tweets is not None:
                where_clauses.append("user_tweet_count <= %s")
                params.append(max_tweets)

            if created_after:
                where_clauses.append("user_created_at >= %s")
                params.append(created_after)

            if created_before:
                where_clauses.append("user_created_at <= %s")
                params.append(created_before)

            if where_clauses:
                query = f"{base_query} WHERE {' AND '.join(where_clauses)}"
            else:
                query = base_query
                
            query += " LIMIT %s"
            params.append(limit)

            print(f"Final Query: {query}")
            print(f"Final Params: {params}")

            results = self.cassandra.execute(query, params)
            return [
                {
                    'author_id': row.author_id,
                    'user_created_at': row.user_created_at,
                    'user_followers_count': row.user_followers_count,
                    'user_tweet_count': row.user_tweet_count,
                    'user_name': row.user_name,
                    'user_username': row.user_username
                } 
                for row in results
            ]

        except Exception as e:
            print(f"Error retrieving users: {e}")
            return [{'error': str(e)}]

    async def get_user(self, user_id: str):
        query = "SELECT * FROM users WHERE author_id = %s"
        results = self.cassandra.execute(query, [user_id])
        user = next(iter(results), None)
        
        # Convert row to dictionary with the same structure as before
        return {
            'author_id': user.author_id,
            'user_created_at': user.user_created_at,
            'user_followers_count': user.user_followers_count,
            'user_tweet_count': user.user_tweet_count,
            'user_name': user.user_name,
            'user_username': user.user_username
        } if user else None

    async def delete_user(self, user_id: str):
        result = self.mongo.users.delete_one({"_id": ObjectId(user_id)})
        
        delete_query = "DELETE FROM users WHERE author_id = %s"
        delete_tweets_query = "DELETE FROM tweets WHERE author_id = %s"
        self.cassandra.execute(delete_query, [user_id])
        self.cassandra.execute(delete_tweets_query, [user_id])
    
        if result.deleted_count:
            return {"message": "User deleted successfully"}
        else:
            return {"message": "User not found"}

    async def update_user(self, user_id: str, user_data: dict):
        update_fields = {k: v for k, v in user_data.items() if v is not None}
        result = self.mongo.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_fields})

        # TODO: Update user in Dgraph

        #Borra el usuario en Cassandra
        self.delete_user(user_id)

        # Extraer datos del usuario modificado desde MongoDB
        mongo_user = self.mongo.users.find_one({"_id": ObjectId(user_id)})

        if mongo_user is None:
            return {"message": "User not found"}

        # Extraer datos del usuario actualizado
        adapted_user_data = {
            "user_username": mongo_user.get("username"),
            "user_name": mongo_user.get("name"),
            "user_followers_count": mongo_user.get("public_metrics", {}).get("followers_count", None),
            "user_tweet_count": mongo_user.get("public_metrics", {}).get("tweet_count", None),
        }

        # Extraer el created_at
        user_created_at = mongo_user.get("created_at")

        new_user_data = {
            "author_id": user_id,
            "user_username": adapted_user_data["user_username"],
            "user_name": adapted_user_data["user_name"],
            "user_followers_count": adapted_user_data["user_followers_count"],
            "user_tweet_count": adapted_user_data["user_tweet_count"],
            "user_created_at": user_created_at
        }

        insert_query = """
            INSERT INTO users (author_id, user_username, user_name, user_followers_count, user_tweet_count, user_created_at) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        self.cassandra.execute(insert_query, (
            new_user_data['author_id'],
            new_user_data['user_username'],
            new_user_data['user_name'],
            new_user_data['user_followers_count'],
            new_user_data['user_tweet_count'],
            new_user_data['user_created_at']
        ))

        if result.matched_count:
            return {"message": "User updated successfully"}
        else:
            return {"message": "User not found"}

    async def create_user(self, user_data: dict):
        #extracción de datos para cassandra
        user_username = user_data.get("username")
        user_name = user_data.get("name")
        user_followers_count = user_data.get("public_metrics", {}).get("followers_count", 0)
        user_tweet_count = user_data.get("public_metrics", {}).get("tweet_count", 0)

        adapted_user_data = {
            "user_username": user_username,
            "user_name": user_name,
            "user_followers_count": user_followers_count,
            "user_tweet_count": user_tweet_count,
        }

        user = UserModel(**user_data)
        result = self.mongo.users.insert_one(user.dict(exclude_unset=True))
        created_user = self.mongo.users.find_one({"_id": result.inserted_id})
        if created_user:
            created_user["_id"] = str(created_user["_id"])

        insert_query = """
        INSERT INTO users (
            author_id, 
            user_username, 
            user_created_at, 
            user_followers_count, 
            user_tweet_count, 
            user_name
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.cassandra.execute(insert_query, (
            str(created_user['_id']),  # Usar el _id como author_id
            adapted_user_data.get('user_username'),
            datetime.now(),  
            adapted_user_data.get('user_followers_count', 0),
            adapted_user_data.get('user_tweet_count', 0),
            adapted_user_data.get('user_name')
        ))
        
        return created_user
    
    async def get_user_tweets(self, user_id: str):
        # TODO: Implement get_user_tweets method with dgraph
        pass