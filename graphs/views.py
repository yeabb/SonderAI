from django.shortcuts import render
from django.http import HttpResponse
from sonderPyvis.network import Network
from .models import TweetNode
from openai import OpenAI
import os
import json

from django.contrib.auth.models import User
from random import choice, randint, sample
from datetime import datetime, timedelta
from scipy.spatial.distance import cosine
    
def constructGraph(request):
    client = initOpenAI()
    tweets, edges = candidate_source()
    network_graph = Network(neighborhood_highlight=True)
    for tweet in tweets:
        print(tweet.id)
        network_graph.add_node(tweet.id, tweet.title)
    
    network_graph.add_edges(edges)
        
    # response = client.embeddings.create(
    #     model="text-embedding-3-small",
    #     input=x
    # )
    # print(response)
    
    
    
    nodes, edges, heading, height, width, options = network_graph.get_network_data()
    serializedNodes = json.dumps(nodes)
    serializedEdges = json.dumps(edges)
    nodesCount = network_graph.num_nodes()
    edgesCount = network_graph.num_edges()
    
    return render(request, "template.html", {
        "height": "100vh",
        "width": width,
        "nodes": serializedNodes,
        "edges": serializedEdges,
        "nodesCount": nodesCount,
        "edgesCount": edgesCount,
        "heading": heading,
        "options": options,
        "physics_enabled": True,
        "use_DOT": net.use_DOT,
        "dot_lang": net.dot_lang,
        "widget": net.widget,
        "bgcolor": "#2a2239",
        "conf": net.conf,
        "tooltip_link": True,
        "neighborhood_highlight": net.neighborhood_highlight,
        "select_menu": net.select_menu,
        "filter_menu": net.filter_menu,
        "notebook": False,
        "cdn_resources": net.cdn_resources
        }
    )
    
def initOpenAI():
    client = OpenAI()
    OpenAI.api_key = os.environ["OPENAI_API_KEY"]
    return client

def candidate_source():
    tweets = TweetNode.objects.all()
    for tweet in tweets:
        x = tweet
    edges = build_edges(tweets)
        
    return tweets, edges

def build_edges(tweets):
    tweets = tweets
    sorted_embeddings = []
    dict_embeddings = {}
    edges = {}
    connection_threeshold = 5
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
        
        while (left >= 0) and (threshold <= cosine_distance(sorted_embeddings[left][1], target_embedding)):
            if tweet.id not in edges:
                edges[tweet.id] = [(tweet.id, sorted_embeddings[mid][0], edge_weight(cosine_distance(sorted_embeddings[left][1], target_embedding)))]
            else:
                edges[tweet.id].append((tweet.id, sorted_embeddings[mid][0], edge_weight(cosine_distance(sorted_embeddings[left][1], target_embedding))))
            
        while (right < len(sorted_embeddings)) and (threshold <= cosine_distance(sorted_embeddings[right][1], target_embedding)):
            if tweet.id not in edges:
                edges[tweet.id] = [(tweet.id, sorted_embeddings[mid][0], edge_weight(cosine_distance(sorted_embeddings[right][1], target_embedding)))]
            else:
                edges[tweet.id].append((tweet.id, sorted_embeddings[mid][0], edge_weight(cosine_distance(sorted_embeddings[right][1], target_embedding))))
       
                
    return edges           
                
def cosine_distance(vector1, vector2):
    return cosine(vector1, vector2)
    
def edge_weight(cosine_distance):
    return 3

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
    
    
    
    
    




def experiment():
    
    net = Network(neighborhood_highlight=True)
    
    # Add clusters of nodes
    for i in range(5):  # Create 5 clusters
        cluster_start = i * 20
        for j in range(20):
            net.add_node(cluster_start + j, f"Node {cluster_start + j}")

        # Interconnect nodes within the cluster
        for j in range(20):
            for k in range(j + 1, 20):
                if j % 3 == 0:  # Add edges to create a dense but not complete graph
                    net.add_edge(cluster_start + j, cluster_start + k)

    # Add inter-cluster connections
    for i in range(5):
        for j in range(i + 1, 5):
            net.add_edge(i * 20, j * 20)  # Connect the first node of each cluster
            net.add_edge(i * 20 + 10, j * 20 + 10)  # Connect a mid-node of each cluster

    # Add random nodes at the periphery to mimic an outer network
    for i in range(100, 120):  # Create 20 outer nodes
        net.add_node(i, f"Outer {i}")
        net.add_edge(i, i - 100)  # Connect each outer node to a node in the first cluster
    
    # net.hrepulsion()
    return net

   