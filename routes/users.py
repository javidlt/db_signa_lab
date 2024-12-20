from fastapi import APIRouter, Request, Body
from controllers.users import UserController
from schemas.schema import UserModel

router = APIRouter()

@router.get("/users-by-followers")
async def get_users_by_followers(request: Request, year: int = None, min_followers: int = None, max_followers: int = None, limit: int = 100):
    user_controller = UserController(request.app.state.db)
    return await user_controller.get_users_by_followers(year=year, min_followers=min_followers, max_followers=max_followers, limit=limit)

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

@router.get("/user_relations")
async def get_user_relations(request: Request):
    user_controller = UserController(request.app.state.db)
    return await user_controller.get_user_relations()


@router.get("/interactions/by_user")
async def get_interactions_by_user(request: Request, user_id: str):
    user_controller = UserController(request.app.state.db)
    return await user_controller.get_interactions_by_user(user_id)