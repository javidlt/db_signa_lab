from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class User(Model):
    __keyspace__ = 'keyspace_name'
    id = columns.UUID(primary_key=True)
    username = columns.Text(required=True)
    email = columns.Text(required=True)
    created_at = columns.DateTime()