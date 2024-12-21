from sonderPyvis.network import Network
import json
from scipy.spatial.distance import cosine
from candidate_source.services.candidates import Candidates

class ConstructNetworkGraph:
    
    def __init__(self):
        self.candidates = Candidates()
        self.network_graph = Network(neighborhood_highlight=True)
        
        self._tweets = None
        self._sorted_embeddings = None   #[(tweet_id1, embedding1), (tweet_id2, embedding2)...]
        self._tweetId_embedding_map = None  #{tweet_id1:embedding1, tweet_id2:embedding2...}
        self.edges = {}

    @property
    def tweets(self):
        if self._tweets is None:
            self._tweets = self.candidates.get_all_tweets()
        return self._tweets

    @property
    def sorted_embeddings(self):
        if self._sorted_embeddings is None:
            self._sorted_embeddings = self.candidates.get_sorted_embeddings_list()
        return self._sorted_embeddings

    @property
    def tweetId_embedding_map(self):
        if self._tweetId_embedding_map is None:
            self._tweetId_embedding_map = self.candidates.get_tweetId_embedding_map()
        return self._tweetId_embedding_map

    def constructGraph(self):
        self.build_edges()
        for tweet in self.tweets:
            print(tweet.id)
            self.network_graph.add_node(tweet.id, tweet.title)
            
        self.network_graph.add_edges(self.edges)
        
        print(self.edges)
        
        nodes, edges, heading, height, width, options = self.network_graph.get_network_data()
        serializedNodes = json.dumps(nodes)
        serializedEdges = json.dumps(edges)
        nodesCount = self.network_graph.num_nodes()
        edgesCount = self.network_graph.num_edges()
        
    def build_edges(self):
        connection_threeshold = 5
        threshold = 0
        for tweet in self.tweets:
            target_embedding = self.tweetId_embedding_map[tweet.id]
            target_index = -1
            left = 0 
            right = len(self.sorted_embeddings) - 1
            while left <= right:
                mid = (left + right)//2
                if self.sorted_embeddings[mid] == target_embedding:
                    target_index = mid
                elif self.sorted_embeddings[mid] < target_embedding:
                    left = mid + 1
                else:
                    right = mid - 1
                    
            if target_index == -1:
                print(f"target embedding was not found in sorted_embeddings for {tweet.id}")        
            
            while (
                left >= 0 
                and threshold <= self.cosine_distance(self.sorted_embeddings[left][1], target_embedding)
            ):
                if tweet.id not in self.edges:
                    self.edges[tweet.id] = [
                        (
                            tweet.id, #tweet_id of the origin tweet node
                            self.sorted_embeddings[left][0], #tweet_id of the destination tweet node
                            self.edge_weight(self.cosine_distance(self.sorted_embeddings[left][1], target_embedding))
                        )
                    ]
                else:
                    self.edges[tweet.id].append(
                        (
                            tweet.id, 
                            self.sorted_embeddings[left][0], 
                            self.edge_weight(self.cosine_distance(self.sorted_embeddings[left][1], target_embedding))
                        )
                    )
                    
                left-=1
                
            while (
                right < len(self.sorted_embeddings) 
                and threshold <= self.cosine_distance(self.sorted_embeddings[right][1], target_embedding)
            ):
                if tweet.id not in self.edges:
                    self.edges[tweet.id] = [
                        (
                            tweet.id, 
                            self.sorted_embeddings[right][0], 
                            self.edge_weight(self.cosine_distance(self.sorted_embeddings[right][1], target_embedding))
                        )
                    ]
                else:
                    self.edges[tweet.id].append(
                        (
                            tweet.id, 
                            self.sorted_embeddings[right][0], 
                            self.edge_weight(self.cosine_distance(self.sorted_embeddings[right][1], target_embedding))
                        )
                    )
                    
                right+=1
                    
    def cosine_distance(vector1, vector2):
        return cosine(vector1, vector2)
        
    def edge_weight(cosine_distance):
        return 3

    