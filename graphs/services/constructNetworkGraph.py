from sonderPyvis.network import Network
import json
from scipy.spatial.distance import cosine
from candidate_source.services.candidates import Candidates

class ConstructNetworkGraph:
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.candidates = Candidates(self.user_id)
        self.network_graph = Network(neighborhood_highlight=True)
        self.values_already_fetched = False     
        self.edges = {}
    
        self._tweets_with_embeddings = None   
        
    '''
    To help in lazy initialization to save compute and avoid repetitive value fetching if it was already fetched recently
    '''
    @property
    def tweets_with_embeddings(self):
        if not self.values_already_fetched:
            self._tweets_with_embeddings = self.candidates.get_all_tweets_with_embeddings(self.user_id)
            self.values_already_fetched = True
        return self._tweets_with_embeddings


    def constructHomePageGraph(self):
        self.build_edges()
        # for tweet in self.tweets:
        #     print(tweet.id)
        #     self.network_graph.add_node(tweet.id, tweet.title)
            
        # self.network_graph.add_edges(self.edges)
        
        print(self.edges)
        
        # nodes, edges, heading, height, width, options = self.network_graph.get_network_data()
        # serializedNodes = json.dumps(nodes)
        # serializedEdges = json.dumps(edges)
        # nodesCount = self.network_graph.num_nodes()
        # edgesCount = self.network_graph.num_edges()
        
    def build_edges(self):
        '''
        Params: 
        tweets_with_embeddings: A list of dictionary where each dictionary is -
                                composed of unique tweetnode(tweetNode) and the vector embedding(embedding) associated to the tweet
        
        [
            {   
                "tweet_node": <TweetNode Object>
                "embedding: {
                                'id': 'tweet-id1',
                                'metadata': {'text': 'The tech company Apple is known for its '
                                                    'innovative products like the iPhone.'},
                                'score': 0.8727808,
                                'sparse_values': {'indices': [], 'values': []},
                                'values': [-0.006929283495992422,-0.005336422007530928, -4.547132266452536e-05,-0.024047505110502243]
                            }
            }, 
            
            {
                "tweet_node": <TweetNode Object>
                "embedding: {
                                'id': 'tweet-id2',
                                'metadata': {'text': 'Apple Inc. has revolutionized the tech '
                                                    'industry with its sleek designs and '
                                                    'user-friendly interfaces'},
                                'score': 0.8727808,
                                'sparse_values': {'indices': [], 'values': []},
                                'values': [-0.006929283495992422,-0.005336422007530928, -4.547132266452536e-05,-0.024047505110502243]
                            }
            }
        ] 
        
       '''
        tweets_with_embeddings = self.tweets_with_embeddings   #call the lazy initialization property function
        cosine_similarity_threshold = 0.1
        visited_nodes = set()
        
        '''
        TODO: I guess we can find the mid point and end the for loop there 
              since the mid point mean technically every combination has been explored??
        '''
        for i in range (len(tweets_with_embeddings)):
            if i+1 < len(tweets_with_embeddings) - 1:
                for j in range (i+1, len(tweets_with_embeddings)):
                    origin_node_id = tweets_with_embeddings[i]["embedding"]["values"]
                    destination_node_id = tweets_with_embeddings[j]["embedding"]["values"]
                    cosine_similarity = self.cosine_similarity(origin_node_id, destination_node_id)
                    
                    #check if the cosine similarity is large enough to connect the nodes
                    if cosine_similarity_threshold >= cosine_similarity: 
                        if  origin_node_id not in self.edges:
                            self.edges[origin_node_id] = [
                                (
                                    origin_node_id, #tweet_id of the origin tweet node
                                    destination_node_id, #tweet_id of the destination tweet node
                                    self.edge_weight(cosine_similarity)
                                )
                            ]
                            self.edges[destination_node_id] = [
                                (
                                    destination_node_id, #tweet_id of the destination tweet node
                                    origin_node_id, #tweet_id of the origin tweet node
                                    self.edge_weight(cosine_similarity)
                                )
                            ]
                            
                        else:
                            self.edges[origin_node_id].append(
                                (
                                    origin_node_id, 
                                    destination_node_id, 
                                    self.edge_weight(cosine_similarity)
                                )
                            )
                            
                            self.edges[destination_node_id].append(
                                (
                                    destination_node_id, 
                                    origin_node_id, 
                                    self.edge_weight(cosine_similarity)
                                )
                            )
                            
    '''
    Params:
        vector1, vector2 (embedding vectors)
        
    Returns: 
        cosine similarity
        cosine similarity =  1 - cosine distance
    '''                       
    def cosine_similarity(vector1, vector2):
        return 1 - cosine(vector1, vector2)
        
    def edge_weight(cosine_distance):
        return 3

    
    
    
    
    
    
    
    
    

    
    
    
    
    # threshold = 0
        # for tweet in self.tweets:
        #     # for each tweet do a binary search to find the 
        #     # index of it's embeddings in the sorted embedding list
        #     target_embedding = self.tweetId_embedding_map[tweet.id]
        #     target_index = -1
        #     left = 0 
        #     right = len(self.sorted_embeddings) - 1
        #     while left <= right:
        #         mid = (left + right)//2
        #         if self.sorted_embeddings[mid] == target_embedding:
        #             target_index = mid
        #         elif self.sorted_embeddings[mid] < target_embedding:
        #             left = mid + 1
        #         else:
        #             right = mid - 1
                    
        #     if target_index == -1:
        #         print(f"target embedding was not found in sorted_embeddings for {tweet.id}")        
            
        #     # after finding the target index, slide scan to the left
        #     while (
        #         left >= 0 
        #         and threshold <= self.cosine_distance(self.sorted_embeddings[left][1], target_embedding)
        #     ):
        #         if tweet.id not in self.edges:
        #             self.edges[tweet.id] = [
        #                 (
        #                     tweet.id, #tweet_id of the origin tweet node
        #                     self.sorted_embeddings[left][0], #tweet_id of the destination tweet node
        #                     self.edge_weight(self.cosine_distance(self.sorted_embeddings[left][1], target_embedding))
        #                 )
        #             ]
        #         else:
        #             self.edges[tweet.id].append(
        #                 (
        #                     tweet.id, 
        #                     self.sorted_embeddings[left][0], 
        #                     self.edge_weight(self.cosine_distance(self.sorted_embeddings[left][1], target_embedding))
        #                 )
        #             )
                    
        #         left-=1
            
        #     # slide scan to the right    
        #     while (
        #         right < len(self.sorted_embeddings) 
        #         and threshold <= self.cosine_distance(self.sorted_embeddings[right][1], target_embedding)
        #     ):
        #         if tweet.id not in self.edges:
        #             self.edges[tweet.id] = [
        #                 (
        #                     tweet.id, 
        #                     self.sorted_embeddings[right][0], 
        #                     self.edge_weight(self.cosine_distance(self.sorted_embeddings[right][1], target_embedding))
        #                 )
        #             ]
        #         else:
        #             self.edges[tweet.id].append(
        #                 (
        #                     tweet.id, 
        #                     self.sorted_embeddings[right][0], 
        #                     self.edge_weight(self.cosine_distance(self.sorted_embeddings[right][1], target_embedding))
        #                 )
        #             )
                    
        #         right+=1