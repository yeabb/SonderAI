from tweets.models import TweetNode
from ...tweets.services.openAIClientProvider import OpenAIClientProvider
from ...tweets.services.pineConeClientProvider import PineConeClientProvider
class Candidates:
    def __init__(self):
        self.pineConeClientProvider = PineConeClientProvider()
        self.tweets = TweetNode.objects.all()  
        self.embeddings = None
    
    def get_all_tweets(self):
        return self.tweets
    
    def get_all_embeddings(self):
        return self.embeddings #TODO add logic to retrieve data from the pine index
    
    def get_sorted_embeddings_list(self):
        pass
    
    def get_tweetId_embedding_map(self):
        pass