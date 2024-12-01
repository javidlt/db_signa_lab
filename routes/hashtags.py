from fastapi import APIRouter, Request
from controllers.hashtags import HashtagControllers

router = APIRouter()

@router.get("/hashtags")
def get_hashtags(request: Request):
    hashtag_controller = HashtagControllers(request.app.state.db)
    return hashtag_controller.get_hashtags()

@router.get("/hashtags/{hashtag}")
def get_hashtag(request: Request, hashtag: str):
    hashtag_controller = HashtagControllers(request.app.state.db)
    return hashtag_controller.get_hashtag(hashtag)

@router.post("/hashtags")
def create_hashtag(request: Request):
    hashtag_controller = HashtagControllers(request.app.state.db)
    return hashtag_controller.create_hashtag()

@router.delete("/hashtags/{hashtag}")
def delete_hashtag(request: Request, hashtag: str):
    hashtag_controller = HashtagControllers(request.app.state.db)
    return hashtag_controller.delete_hashtag(hashtag)

@router.put("/hashtags/{hashtag}")
def update_hashtag(request: Request, hashtag: str):
    hashtag_controller = HashtagControllers(request.app.state.db)
    return hashtag_controller.update_hashtag(hashtag)
@router.get("/interactions/by_hashtag")
async def get_interactions_by_hashtag(request: Request, hashtag: str):
    hashtag_controller = HashtagControllers(request.app.state.db)
    return await hashtag_controller.get_interactions_by_hashtag(hashtag)