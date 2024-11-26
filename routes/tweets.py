from fastapi import APIRouter, Request
from controllers.tweets import TweetsControllers

router = APIRouter()

@router.get("/tweets")
def get_tweets(request: Request):
    tweet_controller = TweetsControllers(request.app.state.db)
    return tweet_controller.get_tweets()

@router.get("/tweets/{tweet_id}")
def get_tweet(request: Request, tweet_id: str):
    tweet_controller = TweetsControllers(request.app.state.db)
    return tweet_controller.get_tweet(tweet_id)

@router.post("/tweets")
def create_tweet(request: Request):
    tweet_controller = TweetsControllers(request.app.state.db)
    return tweet_controller.create_tweet()

@router.delete("/tweets/{tweet_id}")
def delete_tweet(request: Request, tweet_id: str):
    tweet_controller = TweetsControllers(request.app.state.db)
    return tweet_controller.delete_tweet(tweet_id)

@router.put("/tweets/{tweet_id}")
def update_tweet(request: Request, tweet_id: str):
    tweet_controller = TweetsControllers(request.app.state.db)
    return tweet_controller.update_tweet(tweet_id)