from uuid import uuid4
from model import User
import jsonify

class UserController:
    @staticmethod
    async def create_user(user):
        new_user = User.create(
            id=uuid4(),
            username=user.username,
            email=user.email
        )
        return jsonify(new_user)

    @staticmethod
    async def get_user(user_id: str):
        return jsonify(User.get(id=user_id))