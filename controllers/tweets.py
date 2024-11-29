from utils.embeddings import dotProduct
from schemas.schema import TweetModel
from bson import ObjectId
from datetime import datetime

class TweetsControllers:
    def __init__(self, db, embedder=None):
        self.db = db
        self.embedder = embedder
        self.mongo = db.get_db('mongo')
        self.cassandra = db.get_db('cassandra')
        self.dgraph = db.get_db('dgraph')
        self.TweetMongoSchema = TweetModel

    def get_tweets(self, 
        author_id: str = None, 
        start_date: datetime = None, 
        end_date: datetime = None, 
        sentiment: str = None, 
        limit: int = 10, 
        page: int = 1
    ):
        try:
            base_query = "SELECT * FROM tweets"
            where_clauses = []
            params = []

            # Filtros
            if author_id:
                where_clauses.append("author_id = %s")
                params.append(author_id)
            
            if start_date:
                where_clauses.append("created_at >= %s")
                params.append(start_date)
            
            if end_date:
                where_clauses.append("created_at <= %s")
                params.append(end_date)
            
            if sentiment:
                where_clauses.append("sentiment = %s")
                params.append(sentiment)

            # Construir la consulta
            if where_clauses:
                query = f"{base_query} WHERE {' AND '.join(where_clauses)}"
            else:
                query = base_query

            # Límite y paginación
            query += " LIMIT %s"
            params.append(limit)


            print(f"Final Query: {query}")
            print(f"Final Params: {params}")

            # Ejecutar consulta
            results = self.cassandra.execute(query, params)

            # Mapear resultados
            return [
                {
                    'author_id': row.author_id,
                    'created_at': row.created_at,
                    'sentiment': row.sentiment,
                    'id': row.id,
                    'text': row.text,
                    'retweet_count': row.retweet_count,
                    'reply_count': row.reply_count,
                    'like_count': row.like_count,
                    'quote_count': row.quote_count,
                    'source': row.source,
                    'user_username': row.user_username,
                } 
                for row in results
            ]

        except Exception as e:
            print(f"Error retrieving tweets: {e}")
            return [{'error': str(e)}]

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

    # TODO: No funciona el post
    def post_tweet_semantic(self, tweet_data: dict):
        tweet = self.TweetMongoSchema(**tweet_data)
        tweet.Embedding = self.embedder.encode(tweet.text).tolist()
        result = self.mongo.tweets.insert_one(tweet.dict(exclude_unset=True))
        created_tweet = self.mongo.tweets.find_one({"_id": result.inserted_id})
        # TODO: Add tweet to Dgraph
        
        cassandra_stmt = self.cassandra.prepare("""
            INSERT INTO tweets (
                author_id, 
                created_at, 
                sentiment, 
                id, 
                text, 
                retweet_count, 
                reply_count, 
                like_count, 
                quote_count, 
                source, 
                user_username
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """)

        try:
            self.cassandra.execute(cassandra_stmt, (
                str(tweet.author_id or ""),  
                tweet.created_at or datetime.now(),  
                str(tweet.sentiment or "neutral"),  
                str(result.inserted_id),  
                str(tweet.text or ""),  
                tweet.retweet_count or 0,  
                tweet.reply_count or 0,
                tweet.like_count or 0,
                tweet.quote_count or 0,
                str(tweet.source or ""),  
                str(tweet.user_username or "")  
            ))
        except Exception as e:
            print(f"Error inserting tweet into Cassandra: {e}")

        return created_tweet

    def get_tweet_by_id(self, tweet_id: str):
        tweet = self.mongo.tweets.find_one({"_id": ObjectId(tweet_id)})
        if tweet:
            return tweet
        else:
            return {"message": "Tweet not found"}

    # Si jala el post y el delete esto jala 
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
        # TODO: Update tweet in Dgraph

        original_tweet = self.mongo.tweets.find_one({"_id": ObjectId(tweet_id)})
        if not original_tweet:
            return {"message": "Tweet not found"}

        self.delete_tweet(tweet_id)

        adapted_tweet_data = {
            "author_id": original_tweet.get("author_id"),
            "created_at": original_tweet.get("created_at"),
            "sentiment": original_tweet.get("sentiment", "neutral"),
            "id": tweet_id,
            "text": original_tweet.get("text"),
            "retweet_count": original_tweet.get("retweet_count", 0),
            "reply_count": original_tweet.get("reply_count", 0),
            "like_count": original_tweet.get("like_count", 0),
            "quote_count": original_tweet.get("quote_count", 0),
            "source": original_tweet.get("source", ""),
            "user_username": original_tweet.get("user_username", ""),
        }

        insert_query = """
            INSERT INTO tweets (
                author_id, 
                created_at, 
                sentiment, 
                id, 
                text, 
                retweet_count, 
                reply_count, 
                like_count, 
                quote_count, 
                source, 
                user_username
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        try:
            self.cassandra.execute(insert_query, (
                adapted_tweet_data["author_id"],
                adapted_tweet_data["created_at"] or datetime.now(),
                adapted_tweet_data["sentiment"],
                adapted_tweet_data["id"],
                adapted_tweet_data["text"],
                adapted_tweet_data["retweet_count"],
                adapted_tweet_data["reply_count"],
                adapted_tweet_data["like_count"],
                adapted_tweet_data["quote_count"],
                adapted_tweet_data["source"],
                adapted_tweet_data["user_username"],
            ))
        except Exception as e:
            print(f"Error inserting tweet into Cassandra: {e}")
            return {"message": "Error updating tweet"}

        if result.matched_count:
            return {"message": "Tweet updated successfully"}
        else:
            return {"message": "Tweet not found"}
        
    # CREO que funciona
    def delete_tweet(self, tweet_id: str):
        result = self.mongo.tweets.delete_one({"_id": tweet_id})
        # TODO: Delete tweet in Dgraph

        if result.deleted_count:
            try:
                delete_stmt = self.cassandra.prepare("""
                    DELETE FROM tweets 
                    WHERE author_id = ?
                """)
                
                original_tweet = self.mongo.tweets.find_one({"_id": tweet_id})
                
                if original_tweet:
                    self.cassandra.execute(delete_stmt, (
                        str(original_tweet['author_id']),
                        original_tweet['created_at'],
                        str(original_tweet['sentiment'])
                    ))
            except Exception as e:
                print(f"Error deleting tweet from Cassandra: {e}")
                return {"message": "Error deleting tweet"}

            return {"message": "Tweet deleted successfully"}
        else:
            return {"message": "Tweet not found"}

    def get_tweet_relation_with_hashtags(self, tweet_id: str):
        # TODO: Implement get_tweet_relation_with_hashtags method with dgraph
        pass