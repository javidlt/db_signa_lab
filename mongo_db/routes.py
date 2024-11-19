from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from pymongo.database import Database
from controllers import TweetsController
from model import TweetsModel
from db import get_mongo_db

router = APIRouter()
db = get_mongo_db()
tweets_controller = TweetsController(db)

@router.get("/tweets/")
async def get_tweets():
    return JSONResponse(content=tweets_controller.get_tweets())

@router.get("/tweets/{tweet_id}")
async def get_tweet(tweet_id: str):
    return JSONResponse(content=tweets_controller.get_tweet(tweet_id))

@router.post("/tweets/")
async def create_tweet(tweet: TweetsModel):
    tweet_id = tweets_controller.insert_tweet(tweet.model_dump())
    return {"id": tweet_id}

@router.put("/tweets/{tweet_id}")
async def update_tweet(tweet_id: str, tweet: TweetsModel):
    modified = tweets_controller.update_tweet(tweet_id, tweet.model_dump())
    return {"modified_count": modified}

@router.delete("/tweets/{tweet_id}")
async def delete_tweet(tweet_id: str):
    deleted = tweets_controller.delete_tweet(tweet_id)
    return {"deleted_count": deleted}