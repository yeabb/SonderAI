from tweets.models import TweetNode
from .openAIClientProvider import OpenAIClientProvider
class Candidates:
    def __init__(self):
        self.openAIClientProvider = OpenAIClientProvider()
        self.tweets = TweetNode.objects.all()  
        self.embeddings = None
    
    def get_all_tweets(self):
        return self.tweets
    
    def get_all_embeddings(self):
        return self.embeddings
    
    def get_sorted_embeddings_list(self):
        pass
    
    def get_tweetId_embedding_map(self):
        pass