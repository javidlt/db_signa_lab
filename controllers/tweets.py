from utils.embeddings import dotProduct
from schemas.schema import TweetModel
from bson import ObjectId
import pydgraph

class TweetsControllers:
    def __init__(self, db, embedder=None):
        self.db = db
        self.embedder = embedder
        self.mongo = db.get_db('mongo')
        self.cassandra = db.get_db('cassandra')
        self.dgraph = db.get_db('dgraph')
        self.TweetMongoSchema = TweetModel

    def get_tweets(self):
        # TODO: Implement get_tweets method with cassandra
        pass

    def get_tweets_semantic(self, query: str, limit: int = 10, page: int = 1):
        data = self.mongo.tweets
        queryEmbedding = self.embedder.encode(query).tolist()

        tweets = list(data.find({}, {"Embedding": 1, "text": 1}))

        similarities = []
        for tweet in tweets:
            tweet_embedding = tweet.get("Embedding", [])
            if tweet_embedding:
                similarity = dotProduct(queryEmbedding, tweet_embedding)
                similarities.append((similarity, tweet["text"]))

        similarities.sort(reverse=True, key=lambda x: x[0])

        start = (page - 1) * limit
        end = start + limit
        paginated_similarities = similarities[start:end]

        return [text for _, text in paginated_similarities]

    def post_tweet_semantic(self, tweet_data: dict):
        tweet = self.TweetMongoSchema(**tweet_data)
        tweet.Embedding = self.embedder.encode(tweet.text).tolist()
        result = self.mongo.tweets.insert_one(tweet.dict(exclude_unset=True))
        created_tweet = self.mongo.tweets.find_one({"_id": result.inserted_id})

        # Add tweet to Dgraph
        dgraph_tweet = {
            "uid": "_:new_tweet",
            "text": tweet.text,
            "Embedding": tweet.Embedding,
            "created_at": tweet.created_at,
            "source": tweet.source,
            "retweet_count": tweet.retweet_count,
            "reply_count": tweet.reply_count,
            "like_count": tweet.like_count,
            "quote_count": tweet.quote_count,
            "author_id": tweet.author_id,
            "user_name": tweet.user_name,
            "user_username": tweet.user_username,
            "user_created_at": tweet.user_created_at,
            "user_followers_count": tweet.user_followers_count,
            "user_tweet_count": tweet.user_tweet_count,
            "hashtags": tweet.hashtags,
            "mentions": tweet.mentions,
            "urls": tweet.urls,
            "sentiment": tweet.sentiment,
            "embeddingsReducidos": tweet.embeddingsReducidos
        }
        txn = self.dgraph.txn()
        try:
            txn.mutate(set_obj=dgraph_tweet)
            txn.commit()
        finally:
            txn.discard()

        # TODO: Add tweet to Cassandra
        return created_tweet

    def get_tweet_by_id(self, tweet_id: str):
        tweet = self.mongo.tweets.find_one({"_id": ObjectId(tweet_id)})
        if tweet:
            return tweet
        else:
            return {"message": "Tweet not found"}

    def update_tweet(self, tweet_id: str, tweet_data: dict):
        update_fields = {}
        if 'text' in tweet_data:
            update_fields['text'] = tweet_data['text']
            update_fields['Embedding'] = self.embedder.encode(tweet_data['text']).tolist()
        if 'created_at' in tweet_data:
            update_fields['created_at'] = tweet_data['created_at']
        if 'source' in tweet_data:
            update_fields['source'] = tweet_data['source']
        if 'retweet_count' in tweet_data:
            update_fields['retweet_count'] = tweet_data['retweet_count']
        if 'reply_count' in tweet_data:
            update_fields['reply_count'] = tweet_data['reply_count']
        if 'like_count' in tweet_data:
            update_fields['like_count'] = tweet_data['like_count']
        if 'quote_count' in tweet_data:
            update_fields['quote_count'] = tweet_data['quote_count']
        if 'author_id' in tweet_data:
            update_fields['author_id'] = tweet_data['author_id']
        if 'user_name' in tweet_data:
            update_fields['user_name'] = tweet_data['user_name']
        if 'user_username' in tweet_data:
            update_fields['user_username'] = tweet_data['user_username']
        if 'user_created_at' in tweet_data:
            update_fields['user_created_at'] = tweet_data['user_created_at']
        if 'user_followers_count' in tweet_data:
            update_fields['user_followers_count'] = tweet_data['user_followers_count']
        if 'user_tweet_count' in tweet_data:
            update_fields['user_tweet_count'] = tweet_data['user_tweet_count']
        if 'hashtags' in tweet_data:
            update_fields['hashtags'] = tweet_data['hashtags']
        if 'mentions' in tweet_data:
            update_fields['mentions'] = tweet_data['mentions']
        if 'urls' in tweet_data:
            update_fields['urls'] = tweet_data['urls']
        if 'sentiment' in tweet_data:
            update_fields['sentiment'] = tweet_data['sentiment']
        if 'embeddingsReducidos' in tweet_data:
            update_fields['embeddingsReducidos'] = tweet_data['embeddingsReducidos']

        result = self.mongo.tweets.update_one({"_id": ObjectId(tweet_id)}, {"$set": update_fields})
        
        txn = self.dgraph.txn()
        try:
            nquads = f'<_:tweet> <tweet_id> "{tweet_id}" .\n'
            for key, value in update_fields.items():
                if isinstance(value, list):
                    for item in value:
                        nquads += f'<_:tweet> <{key}> "{item}" .\n'
                else:
                    nquads += f'<_:tweet> <{key}> "{value}" .\n'
            mutation = pydgraph.Mutation(set_nquads=nquads)
            txn.mutate(mutation=mutation, commit_now=True)
        finally:
            txn.discard()
        
        
        # TODO: Update tweet in Cassandra
        if result.matched_count:
            return {"message": "Tweet updated successfully"}
        else:
            return {"message": "Tweet not found"}

    def delete_tweet(self, tweet_id: str):
        result = self.mongo.tweets.delete_one({"_id": ObjectId(tweet_id)})
        # TODO: Delete tweet in Dgraph
        # TODO: Delete tweet in Cassandra
        if result.deleted_count:
            txn = self.dgraph.txn()
            try:
                query = f"""
                {{
                    tweet as var(func: eq(tweet_id, "{tweet_id}"))
                }}
                """
                mutation = pydgraph.Mutation(del_nquads=f"uid(tweet) * * .")
                txn.mutate(mutation=mutation, commit_now=True)
            finally:
                txn.discard()
            
            return {"message": "Tweet deleted successfully"}
        else:
            return {"message": "Tweet not found"}

    def get_tweet_relation_with_hashtags(self, tweet_id: str):
        txn = self.dgraph.txn(read_only=True)
        try:
            query = f"""
            {{
                tweet(func: eq(tweet_id, "{tweet_id}")) {{
                    tweet_id
                    text
                    hashtags {{
                        hashtag_id
                        name
                    }}
                }}
            }}
            """
            response = txn.query(query)
            result = response.json()
            return result.get('tweet', [])
        finally:
            txn.discard()