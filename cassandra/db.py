from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine import connection

def get_session():
    # Replace with your Cassandra credentials and host
    auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandra')
    cluster = Cluster(['localhost'], auth_provider=auth_provider)
    session = cluster.connect()
    return session

def init_db():
    # Initialize connection
    connection.setup(['localhost'], "keyspace_name", protocol_version=3)