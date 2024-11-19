from pymongo.database import Database
from bson.objectid import ObjectId
from model import TweetsModel
from typing import List, Optional
from fastapi import HTTPException

class TweetsController:
    def __init__(self, db: Database):
        self.db = db
        self.collection = self.db["tweets"]

    def get_tweets(self) -> List[TweetsModel]:
        tweets = list(self.collection.find())
        return [TweetsModel(**tweet) for tweet in tweets]

    def get_tweet(self, tweet_id: str) -> Optional[TweetsModel]:
        tweet = self.collection.find_one({"_id": ObjectId(tweet_id)})
        if not tweet:
            raise HTTPException(status_code=404, detail="Tweet not found")
        return TweetsModel(**tweet)

    def insert_tweet(self, tweet: TweetsModel) -> str:
        tweet_dict = tweet.dict(exclude_unset=True)
        result = self.collection.insert_one(tweet_dict)
        return str(result.inserted_id)

    def update_tweet(self, tweet_id: str, tweet: TweetsModel) -> int:
        try:
            tweet_dict = tweet.dict(exclude_unset=True)
            result = self.collection.update_one(
                {"_id": ObjectId(tweet_id)}, 
                {"$set": tweet_dict}
            )
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Tweet not found")
            return result.modified_count
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def delete_tweet(self, tweet_id: str) -> int:
        try:
            result = self.collection.delete_one({"_id": ObjectId(tweet_id)})
            if result.deleted_count == 0:
                raise HTTPException(status_code=404, detail="Tweet not found")
            return result.deleted_count
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))