from fastapi.responses import JSONResponse
import pydgraph

class HashtagControllers:
    def __init__(self, db):
        self.db = db
        self.mongo = db.get_db('mongo')
        self.cassandra = db.get_db('cassandra')
        self.dgraph = db.get_db('dgraph')

    def get_hashtags(self):
        txn = self.dgraph.txn(read_only=True)
        try:
            query = """
            {
                hashtags(func: has(hashtag_id)) {
                    hashtag_id
                    name
                }
            }
            """
            response = txn.query(query)
            result = response.json()
            return JSONResponse(content={"hashtags": result.get('hashtags', [])})
        finally:
            txn.discard()

    def get_hashtag(self, hashtag_id: str):
        txn = self.dgraph.txn(read_only=True)
        try:
            query = f"""
            {{
                hashtag(func: eq(hashtag_id, "{hashtag_id}")) {{
                    hashtag_id
                    name
                    tweets {{
                        tweet_id
                        text
                    }}
                }}
            }}
            """
            response = txn.query(query)
            result = response.json()
            return JSONResponse(content={"hashtag": result.get('hashtag', [])})
        finally:
            txn.discard()

    def create_hashtag(self, hashtag_data: dict):
        txn = self.dgraph.txn()
        try:
            nquads = f"""
            _:hashtag <hashtag_id> "{hashtag_data['hashtag_id']}" .
            _:hashtag <name> "{hashtag_data['name']}" .
            """
            mutation = pydgraph.Mutation(set_nquads=nquads)
            txn.mutate(mutation=mutation, commit_now=True)
            return {"message": "Hashtag created successfully"}
        finally:
            txn.discard()

    def delete_hashtag(self, hashtag_id: str):
        txn = self.dgraph.txn()
        try:
            query = f"""
            {{
                hashtag as var(func: eq(hashtag_id, "{hashtag_id}"))
            }}
            """
            mutation = pydgraph.Mutation(del_nquads=f"uid(hashtag) * * .")
            txn.mutate(mutation=mutation, commit_now=True)
            return {"message": "Hashtag deleted successfully"}
        finally:
            txn.discard()

    def update_hashtag(self, hashtag_id: str, hashtag_data: dict):
        txn = self.dgraph.txn()
        try:
            nquads = f'<_:hashtag> <hashtag_id> "{hashtag_id}" .\n'
            for key, value in hashtag_data.items():
                nquads += f'<_:hashtag> <{key}> "{value}" .\n'
            mutation = pydgraph.Mutation(set_nquads=nquads)
            txn.mutate(mutation=mutation, commit_now=True)
            return {"message": "Hashtag updated successfully"}
        finally:
            txn.discard()

    def get_tweets(self, hashtag_id: str):
        txn = self.dgraph.txn(read_only=True)
        try:
            query = f"""
            {{
                hashtag(func: eq(hashtag_id, "{hashtag_id}")) {{
                    tweets {{
                        tweet_id
                        text
                    }}
                }}
            }}
            """
            response = txn.query(query)
            result = response.json()
            return JSONResponse(content={"tweets": result.get('hashtag', [{}])[0].get('tweets', [])})
        finally:
            txn.discard()