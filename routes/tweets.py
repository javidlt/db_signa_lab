from fastapi import APIRouter, Request, Body
from controllers.tweets import TweetsControllers
from schemas.schema import TweetModel, QueryModel

router = APIRouter()

@router.get("/tweets-by-date")
def get_tweets_by_date(request: Request, year: int, month: int, day: int, limit: int = 20):
    tweet_controller = TweetsControllers(request.app.state.db)
    return tweet_controller.get_tweets_by_date(year, month, day, limit)

@router.get("/tweets/semantic")
def get_tweets_semantic(request: Request, query_model: QueryModel):
    tweet_controller = TweetsControllers(request.app.state.db, request.app.state.embedder)
    return tweet_controller.get_tweets_semantic(query_model.query, query_model.limit, query_model.page)

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