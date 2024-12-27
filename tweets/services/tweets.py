from tweets.models import TweetNode
from embedding import Embedding

class Tweets:
    
    def __init__(self):
        self.embedding = Embedding()
    
    def persist_tweet(self, tweet):
        tweet = TweetNode.objects.create(
            user=tweet["users"], 
            title=tweet["title"], 
            content=tweet["content"], 
            created_at=tweet["created_at"], 
            updated_at=tweet["updated_at"],
        )
        
        embedding_doc = self.embedding.generate_embedding(tweet)
        return(tweet, embedding_doc)