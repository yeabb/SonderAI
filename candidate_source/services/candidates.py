from tweets.models import TweetNode
from ...tweets.services.embedding import Embedding

class Candidates:
    def __init__(self, user_id):
        self.user_id = user_id 
        self.embedding = Embedding()  
        self.tweet_id_to_tweetNode_map = None
        self.list_of_vector_embeddings_maps = None
        self.recommendation_vector_embedding = None
    
    def get_all_tweets_with_embeddings(self): #TODO: build list of dictionaries with tweetnode and corresponding embeddings are mapped together
        self.recommendation_embedding = self.get_personal_recommendation_vector_embedding()
        self.list_of_vector_embeddings_dict = self.embedding.query_vector_embeddings(self.recommendation_vector_embedding)
        self.tweet_id_to_tweetNode_map = self.get_corresponding_tweets_for_vector_embeddings()
        self.all_tweets_with_embeddings = self.build_tweet_node_and_embeddings_doc()
        return self.all_tweets_with_embeddings
    
    def get_corresponding_tweets_for_vector_embeddings(self):
        list_of_tweet_id = []
        for vector_embedding_dict in self.list_of_vector_embeddings_dict:
            list_of_tweet_id.append(vector_embedding_dict["id"])
        
        tweets = TweetNode.objects.filter(id__in = list_of_tweet_id)
        tweet_id_to_tweetNode_map = {}
        for tweet in tweets:
            tweet_id_to_tweetNode_map[tweet.id] = tweet
        
        return tweet_id_to_tweetNode_map
    
    def get_personal_recommendation_vector_embedding(self): #this will be replaced later with embedding space, a class that will handle all embedding replated operations
        # return user_recommendation_vector
        pass
    
    def build_tweet_node_and_embeddings_doc(self):
        list_of_maps = []
        tweet_node_embedding_map = {}
        for vector_embedding_map in self.list_of_vector_embeddings_maps:
            tweet_node_embedding_map = {}
            tweet_id = vector_embedding_map["id"]
            tweet_node_embedding_map["tweet_node"] = self.tweet_id_to_tweetNode_map[tweet_id]
            tweet_node_embedding_map["embedding"] = vector_embedding_map
            list_of_maps.append(tweet_node_embedding_map)
            
    