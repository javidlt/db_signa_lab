from bson import ObjectId
from schemas.schema import UserModel
from fastapi import HTTPException


class UserController:
    def __init__(self, db):
        self.db = db
        self.mongo = db.get_db('mongo')
        self.cassandra = db.get_db('cassandra')
        self.dgraph = db.get_db('dgraph')

    async def get_users_by_followers(self, year: int = None, min_followers: int = None, max_followers: int = None, limit: int = 100):
        try:
            if min_followers is None and max_followers is None:
                raise ValueError("Debe proporcionar al menos un filtro de seguidores (min_followers o max_followers)")

            base_query = """
                SELECT *
                FROM user_followers
            """
            
            where_clauses = []
            parameters = []

            if year is not None:
                where_clauses.append("year = ?")
                parameters.append(year)

            if min_followers is not None:
                where_clauses.append("followers_count >= ?")
                parameters.append(min_followers)

            if max_followers is not None:
                where_clauses.append("followers_count <= ?")
                parameters.append(max_followers)

            if where_clauses:
                query = base_query + " WHERE " + " AND ".join(where_clauses) + " ORDER BY followers_count DESC LIMIT ?"
                parameters.append(limit)
            else:
                query = base_query + " ORDER BY followers_count DESC LIMIT ?"
                parameters.append(limit)

            try:
                prepared_query = self.cassandra.prepare(query)
                results = self.cassandra.execute(prepared_query, parameters)

                users = []
                for row in results:
                    user = {
                        'year': row.year,
                        'month': row.month,
                        'day': row.day,
                        'username': row.username,               
                        'user_id': row.user_id,
                        'name': row.name,
                        'location': row.location,
                        'followers_count': row.followers_count,
                        'following_count': row.following_count,
                        'tweet_count': row.tweet_count,
                        'listed_count': row.listed_count
                    }
                    users.append(user)
                
                print(f"Número de usuarios encontrados: {len(users)}")
                return users

            except Exception as e:
                print("Error al ejecutar consulta:", str(e))
                
                raise HTTPException(
                    status_code=500, 
                    detail={
                        "error": "Error al ejecutar consulta en Cassandra",
                        "exception": str(e)
                    }
                )

        except ValueError as ve:
            raise HTTPException(
                status_code=400, 
                detail={
                    "error": str(ve)
                }
            )
        except Exception as e:
            import traceback
            print(f"Error general en get_users_by_followers: {str(e)}")
            print(traceback.format_exc())

            raise HTTPException(
                status_code=500, 
                detail={
                    "error": "Error al obtener usuarios por seguidores",
                    "exception": str(e)
                }
            )

    async def delete_user(self, user_id: str):
        result = self.mongo.users.delete_one({"_id": ObjectId(user_id)})
    
        if result.deleted_count:
            return {"message": "User deleted successfully"}
        else:
            return {"message": "User not found"}

    async def update_user(self, user_id: str, user_data: dict):
        update_fields = {k: v for k, v in user_data.items() if v is not None}
        result = self.mongo.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_fields})

        # TODO: Update user in Dgraph

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
        
        return created_user
    
    async def get_user_tweets(self, user_id: str):
        # TODO: Implement get_user_tweets method with dgraph
        pass