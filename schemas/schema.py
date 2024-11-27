from pydantic import BaseModel
from typing import List, Optional, Dict

class QueryModel(BaseModel):
    query: str
    limit: int = 10
    page: int = 1

class TweetModel(BaseModel):
    text: Optional[str] = None
    created_at: Optional[str] = None
    source: Optional[str] = None
    retweet_count: Optional[int] = None
    reply_count: Optional[int] = None
    like_count: Optional[int] = None
    quote_count: Optional[int] = None
    author_id: Optional[str] = None
    user_name: Optional[str] = None
    user_username: Optional[str] = None
    user_created_at: Optional[str] = None
    user_followers_count: Optional[int] = None
    user_tweet_count: Optional[int] = None
    hashtags: Optional[List[str]] = None
    mentions: Optional[List[str]] = None
    urls: Optional[List[str]] = None
    sentiment: Optional[str] = None
    Embedding: Optional[List[float]] = None
    embeddingsReducidos: Optional[List[float]] = None

class UserModel(BaseModel):
    created_at: Optional[str] = None
    name: Optional[str] = None
    id: Optional[str] = None
    public_metrics: Optional[Dict[str, int]] = None
    username: Optional[str] = None
    location: Optional[str] = None

class HashtagModel(BaseModel):
    tag: Optional[str] = None
    count: Optional[int] = None