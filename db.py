from pymongo import MongoClient
import pydgraph
from cassandra.cluster import Cluster
from schemas.schemas import Schema  

class DB:
    def __init__(self):
        self.databases = {
            'cassandra': None,
            'mongo': None,
            'dgraph': None,
        }
        self.schemas = Schema(self)
    
    def connect_cassandra(self, host='localhost', port=9042):
        cluster = Cluster([host], port=port)
        session = cluster.connect()
        session.execute("CREATE KEYSPACE IF NOT EXISTS twitter WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}")
        session.set_keyspace('twitter')
        self.set_db('cassandra', session)
        try: 
            self.schemas.execute_cassandra()
        except:
            print("Error creating cassandra tables")
        print("Connected to Cassandra")

    def connect_mongo(self, host='localhost', port=27017):
        client = MongoClient(f"mongodb://{host}:{port}")
        db = client['twitter']
        self.set_db('mongo', db)
        try:
            self.schemas.execute_mongo()
        except:
            print("Error creating mongo collections")
        print("Connected to MongoDB")

    def connect_dgraph(self, host='localhost', port=9080):
        client_stub = pydgraph.DgraphClientStub(f"{host}:{port}")
        client = pydgraph.DgraphClient(client_stub)
        self.set_db('dgraph', client)
        try: 
            self.schemas.execute_dgraph()
        except:
            print("Error creating dgraph schema")
        print("Connected to Dgraph")

    def get_db(self, db_name):
        return self.databases.get(db_name)
    
    def set_db(self, db_name, db_instance):
        self.databases[db_name] = db_instance