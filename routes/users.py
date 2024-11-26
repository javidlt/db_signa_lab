from fastapi import APIRouter, Request
from controllers.users import UserController

router = APIRouter()

@router.get("/users")
def get_users(request: Request):
    user_controller = UserController(request.app.state.db)
    return user_controller.get_users()

@router.get("/users/{user_id}")
def get_user(request: Request, user_id: str):
    user_controller = UserController(request.app.state.db)
    return user_controller.get_user(user_id)

@router.post("/users")
def create_user(request: Request):
    user_controller = UserController(request.app.state.db)
    return user_controller.create_user()

@router.delete("/users/{user_id}")
def delete_user(request: Request, user_id: str):
    user_controller = UserController(request.app.state.db)
    return user_controller.delete_user(user_id)

@router.put("/users/{user_id}")
def update_user(request: Request, user_id: str):
    user_controller = UserController(request.app.state.db)
    return user_controller.update_user(user_id)