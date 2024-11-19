from pymongo import MongoClient
from pydantic import BaseModel

class MongoDBConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str
    database: str

def get_mongo_db():
    config = MongoDBConfig(
        host="your-azure-container-host",
        port=27017,
        username="your-username",
        password="your-password",
        database="your-database"
    )
    
    uri = f"mongodb://{config.username}:{config.password}@{config.host}:{config.port}/{config.database}"
    client = MongoClient(uri)
    return client[config.database]