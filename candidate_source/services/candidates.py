from tweets.models import TweetNode
from ...tweets.services.openAIClientProvider import OpenAIClientProvider
from ...tweets.services.pineConeClientProvider import PineConeClientProvider
from ...tweets.services.embedding import Embedding
class Candidates:
    def __init__(self):
        self.tweets = TweetNode.objects.all()  
        self.embeddings = Embedding().query_embeddings()
        self.sorted_embeddings = None
    
    def get_all_tweets(self):
        return self.tweets
    
    def get_unsorted_embeddings(self):
        return self.embeddings 
    
    def get_sorted_embeddings_list(self):
        pass
    
    def get_tweetId_embedding_map(self):
        pass