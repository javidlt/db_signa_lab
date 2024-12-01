from fastapi import APIRouter, Request, Body
from controllers.users import UserController
from schemas.schema import UserModel

router = APIRouter()

@router.get("/users")
async def get_users(request: Request):
    user_controller = UserController(request.app.state.db)
    return await user_controller.get_users()

@router.get("/users/{user_id}")
async def get_user(request: Request, user_id: str):
    user_controller = UserController(request.app.state.db)
    return await user_controller.get_user(user_id)

@router.post("/users")
async def create_user(request: Request, user_model: UserModel = Body(...)):
    user_controller = UserController(request.app.state.db)
    return await user_controller.create_user(user_model.dict())

@router.delete("/users/{user_id}")
async def delete_user(request: Request, user_id: str):
    user_controller = UserController(request.app.state.db)
    return await user_controller.delete_user(user_id)

@router.put("/users/{user_id}")
async def update_user(request: Request, user_id: str, user_model: UserModel = Body(...)):
    user_controller = UserController(request.app.state.db)
    return await user_controller.update_user(user_id, user_model.dict())