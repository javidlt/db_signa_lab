from fastapi import APIRouter, HTTPException, Depends
from model import User
from controllers import UserController
from db import DgraphClient

router = APIRouter()

def get_db():
    db = DgraphClient()
    try:
        yield db.client
    finally:
        db.close()

@router.post("/users/", response_model=User)
async def create_user(user: User, db=Depends(get_db)):
    controller = UserController(db)
    return await controller.create_user(user.dict())

@router.get("/users/{uid}", response_model=User)
async def get_user(uid: str, db=Depends(get_db)):
    controller = UserController(db)
    try:
        return await controller.get_user(uid)
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found")