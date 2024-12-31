from sonderPyvis.network import Network
import json
from scipy.spatial.distance import cosine
from candidate_source.services.candidates import Candidates

class ConstructNetworkGraph:
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.candidates = Candidates(self.user_id)
        self.network_graph = Network(neighborhood_highlight=True)
        self.tweet_id_to_tweetNode_map = None
        self.values_already_fetched = False    
         
        #This is cyclic, which means if we have 2 nodes A and B, self.edges will have both [A:[(A, B, W)], B:[(B, A, W)]]
        self.edges = {}  
    
        self._tweets_with_embeddings = None   
        
    '''
    To help in lazy initialization to save compute and avoid repetitive 
    value fetching if it was already fetched recently
    '''
    @property
    def tweets_with_embeddings(self):
        if self.values_already_fetched == False:
            self._tweets_with_embeddings = self.candidates.get_all_tweets_with_embeddings()
            self.tweet_id_to_tweetNode_map = self.candidates.tweet_id_to_tweetNode_map
            self.values_already_fetched = True
        return self._tweets_with_embeddings

    def constructHomePageGraph(self):
        self.build_edges()
        # for tweet in self.tweets:
        #     print(tweet.id)
        #     self.network_graph.add_node(tweet.id, tweet.title)
            
        # self.network_graph.add_edges(self.edges)
        
        print(self.edges)
        self.add_nodes()
        self.add_edges()
        
        nodes, edges, heading, height, width, options = self.network_graph.get_network_data()
        print("ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
        print(nodes)
        print("")
        print("")
        print(edges)
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
        tweets_with_embeddings = self.tweets_with_embeddings   #call the lazy initialization @property function
        cosine_similarity_threshold = 0.1
        visited_nodes = set()
        
        
        for i in range (len(tweets_with_embeddings)):
            if i+1 < len(tweets_with_embeddings):
                for j in range (i+1, len(tweets_with_embeddings)):
                    origin_node_id = tweets_with_embeddings[i]["embedding"]["id"]
                    destination_node_id = tweets_with_embeddings[j]["embedding"]["id"]
                    origin_node_vector_embedding = tweets_with_embeddings[i]["embedding"]["values"]
                    destination_node_vector_embedding = tweets_with_embeddings[j]["embedding"]["values"]
                    
                    cosine_similarity = self.cosine_similarity(origin_node_vector_embedding, destination_node_vector_embedding)

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
                            if destination_node_id not in self.edges:
                                self.edges[destination_node_id] = [
                                    (
                                        destination_node_id, #tweet_id of the destination tweet node
                                        origin_node_id, #tweet_id of the origin tweet node
                                        self.edge_weight(cosine_similarity)
                                    )
                                ]
                                
                            else:
                                self.edges[destination_node_id].append(
                                    (
                                        destination_node_id, 
                                        origin_node_id, 
                                        self.edge_weight(cosine_similarity)
                                    )
                                )
                            
                        else:
                            self.edges[origin_node_id].append(
                                (
                                    origin_node_id, 
                                    destination_node_id, 
                                    self.edge_weight(cosine_similarity)
                                )
                            )
                            
                            if destination_node_id not in self.edges:
                                self.edges[destination_node_id] = [
                                    (
                                        destination_node_id, 
                                        origin_node_id, 
                                        self.edge_weight(cosine_similarity)
                                    )
                                ]
                                
                            else:
                                self.edges[destination_node_id].append(
                                    (
                                        destination_node_id, 
                                        origin_node_id, 
                                        self.edge_weight(cosine_similarity)
                                    )
                                )
        return self.edges     
                                         
    def cosine_similarity(self, vector1, vector2):
        '''
        Params:
            vector1, vector2 (embedding vectors)
            
        Returns: 
            cosine similarity
            cosine similarity =  1 - cosine distance
        ''' 
        return 1 - cosine(vector1, vector2)
        
    def edge_weight(self, cosine_distance):
        return 3

    def add_nodes(self):
        for tweet_id, tweet_node in self.tweet_id_to_tweetNode_map.items():
            self.network_graph.add_node(tweet_id, tweet_node.title)
        
    def add_edges(self):
        list_edges = [item for sublist in self.edges.values() for item in sublist]
        self.network_graph.add_edges(list_edges)
        
    
    
    