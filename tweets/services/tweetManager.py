from tweets.models import TweetNode
from .embedding import Embedding

class TweetManager:
    
    def __init__(self):
        self.embedding = Embedding()
    
    def persist_tweet(self, tweet):
        tweet_node = TweetNode.objects.create(
            user=tweet["users"], 
            title=tweet["title"], 
            content=tweet["content"], 
            created_at=tweet["created_at"], 
            updated_at=tweet["updated_at"],
        )
        
        embedding_doc = self.embedding.generate_embedding(tweet_node)
        return(tweet_node, embedding_doc)