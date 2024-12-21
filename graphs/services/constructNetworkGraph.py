from sonderPyvis.network import Network
import json
from scipy.spatial.distance import cosine

class ConstructNetworkGraph:
    def __init__(self):
        pass
    
    def constructGraph(self):
        tweets = self.candidate_source()
        edges = self.build_edges(tweets)
        network_graph = Network(neighborhood_highlight=True)
        for tweet in tweets:
            print(tweet.id)
            network_graph.add_node(tweet.id, tweet.title)
        
        print(edges)
        
        nodes, edges, heading, height, width, options = network_graph.get_network_data()
        serializedNodes = json.dumps(nodes)
        serializedEdges = json.dumps(edges)
        nodesCount = network_graph.num_nodes()
        edgesCount = network_graph.num_edges()
        
    

    def build_edges(self, tweets):
        tweets = tweets
        sorted_embeddings = []
        dict_embeddings = {}
        edges = {}
        connection_threeshold = 5
        threshold = 0
        for tweet in tweets:
            target_embedding = dict_embeddings[tweet.id]
            target_index = -1
            left = 0 
            right = len(sorted_embeddings) - 1
            while left <= right:
                mid = (left + right)//2
                if sorted_embeddings[mid] == target_embedding:
                    target_index = mid
                elif sorted_embeddings[mid] < target_embedding:
                    left = mid + 1
                else:
                    right = mid - 1
                    
            if target_index == -1:
                print(f"target embedding was not found in sorted_embeddings for {tweet.id}")        
            
            while (
                left >= 0 
                and threshold <= self.cosine_distance(sorted_embeddings[left][1], target_embedding)
            ):
                if tweet.id not in edges:
                    edges[tweet.id] = [
                        (
                            tweet.id, 
                            sorted_embeddings[mid][0], 
                            self.edge_weight(self.cosine_distance(sorted_embeddings[left][1], target_embedding))
                        )
                    ]
                else:
                    edges[tweet.id].append(
                        (
                            tweet.id, 
                            sorted_embeddings[mid][0], 
                            self.edge_weight(self.cosine_distance(sorted_embeddings[left][1], target_embedding))
                        )
                    )
                
            while (
                right < len(sorted_embeddings) 
                and threshold <= self.cosine_distance(sorted_embeddings[right][1], target_embedding)
            ):
                if tweet.id not in edges:
                    edges[tweet.id] = [
                        (
                            tweet.id, 
                            sorted_embeddings[mid][0], 
                            self.edge_weight(self.cosine_distance(sorted_embeddings[right][1], target_embedding))
                        )
                    ]
                else:
                    edges[tweet.id].append(
                        (
                            tweet.id, 
                            sorted_embeddings[mid][0], 
                            self.edge_weight(self.cosine_distance(sorted_embeddings[right][1], target_embedding))
                        )
                    )
        
                    
        return edges           
                    
    def constructNetwork(networkSetting):
        return Network(networkSetting)

    def addNode(net, node):
        return net.add_node(node) 

    def addEdge(net, edge):
        return net.add_edge(edge)

    def addNodes(net, nodes):
        return net.add_nodes(nodes)
        
    def addEdges(net, edges):
        return net.add_edges(edges)
                    
    def cosine_distance(vector1, vector2):
        return cosine(vector1, vector2)
        
    def edge_weight(cosine_distance):
        return 3

    