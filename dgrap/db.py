import pydgraph
import json

class DgraphClient:
    def __init__(self):
        self.stub = pydgraph.DgraphClientStub('localhost:9080')
        self.client = pydgraph.DgraphClient(self.stub)

    def set_schema(self):
        schema = """
            type User {
                username: string
                email: string
                created_at: datetime
            }
            username: string @index(exact) .
            email: string @index(exact) .
            created_at: datetime .
        """
        return self.client.alter(pydgraph.Operation(schema=schema))

    def close(self):
        self.stub.close()