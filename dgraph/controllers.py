import json
from datetime import datetime
from models import User
import pydgraph

class UserController:
    def __init__(self, client):
        self.client = client

    async def create_user(self, user_data: dict):
        txn = self.client.txn()
        try:
            user_data['created_at'] = datetime.now().isoformat()
            mutation = {
                'set_json': user_data
            }
            response = txn.mutate(set_obj=user_data)
            txn.commit()
            
            user_data['uid'] = response.uids['blank-0']
            return User(**user_data)
        finally:
            txn.discard()

    async def get_user(self, uid: str):
        query = """
        {
            user(func: uid($uid)) {
                uid
                username
                email
                created_at
            }
        }
        """
        variables = {'$uid': uid}
        txn = self.client.txn()
        try:
            response = txn.query(query, variables=variables)
            user_data = json.loads(response.json)['user'][0]
            return User(**user_data)
        finally:
            txn.discard()