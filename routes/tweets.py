from fastapi import APIRouter, Request, Body, Query
from controllers.tweets import TweetsControllers
from schemas.schema import TweetModel, QueryModel
from typing import Optional

router = APIRouter()

@router.get("/tweets-by-date")
def get_tweets_by_date(request: Request, year: int, month: int, day: int, limit: int = 20):
    tweet_controller = TweetsControllers(request.app.state.db)
    return tweet_controller.get_tweets_by_date(year, month, day, limit)

@router.get("/tweets/semantic")
def get_tweets_semantic(request: Request, query: str = Query(...), limit: int = Query(10), page: int = Query(1)):
    tweet_controller = TweetsControllers(request.app.state.db, request.app.state.embedder)
    return tweet_controller.get_tweets_semantic(query, limit, page)

@router.get("/tweets/by_sentiment")
def get_tweets_by_sentiment(request: Request, sentiment: Optional[str] = Query(None), limit: int = Query(10), page: int = Query(1)):
    tweet_controller = TweetsControllers(request.app.state.db, request.app.state.embedder)
    return tweet_controller.get_tweets_by_sentiment(sentiment, limit, page)

@router.get("/tweets/by_id/{tweet_id}")
def get_tweet(request: Request, tweet_id: str):
    tweet_controller = TweetsControllers(request.app.state.db)
    return tweet_controller.get_tweet_by_id(tweet_id)

@router.post("/tweets")
def post_tweet(request: Request, tweet_model: TweetModel = Body(...)):
    tweet_controller = TweetsControllers(request.app.state.db, request.app.state.embedder)
    return tweet_controller.post_tweet_semantic(tweet_model.dict())

@router.delete("/tweets/{tweet_id}")
def delete_tweet(request: Request, tweet_id: str):
    tweet_controller = TweetsControllers(request.app.state.db)
    return tweet_controller.delete_tweet(tweet_id)

@router.put("/tweets/{tweet_id}")
def update_tweet(request: Request, tweet_id: str, tweet_model: TweetModel = Body(...)):
    tweet_controller = TweetsControllers(request.app.state.db, request.app.state.embedder)
    return tweet_controller.update_tweet(tweet_id, tweet_model.dict())

@router.get("/tweet_responses")
async def get_tweet_responses(request: Request, tweet_id: str):
    tweet_controller = TweetsControllers(request.app.state.db)
    return await tweet_controller.get_tweet_responses(tweet_id)

@router.get("/tweets/by_hashtag")
async def get_tweets_by_hashtag(request: Request, hashtag: str):
    tweet_controller = TweetsControllers(request.app.state.db)
    return await tweet_controller.get_tweets_by_hashtag(hashtag)

@router.get("/interactions/by_hashtag")
async def get_interactions_by_hashtag(request: Request, hashtag: str):
    tweet_controller = TweetsControllers(request.app.state.db)
    return await tweet_controller.get_interactions_by_hashtag(hashtag)