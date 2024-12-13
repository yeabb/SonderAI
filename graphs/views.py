from django.shortcuts import render
from django.http import HttpResponse
from sonderPyvis.network import Network
from .models import TweetNode
import json

from django.contrib.auth.models import User
from random import choice, randint, sample
from datetime import datetime, timedelta
    
def constructGraph(request):
    # nodes = TweetNode.objects.all()
    # print(nodes)
    
    # net = experiment()
    
    net = exper2()
    
    
    nodes, edges, heading, height, width, options = net.get_network_data()
    serializedNodes = json.dumps(nodes)
    serializedEdges = json.dumps(edges)
    nodesCount = net.num_nodes()
    edgesCount = net.num_edges()
    
    # print(nodes)
    # print("----------------------------------------------------")
    # print(edges)
   
    
    # return render(request, "basic_template.html", {"cdn_resources": "local"})
    
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



def exper2():

    tweets = TweetNode.objects.all()
    net = Network(neighborhood_highlight=True)
    for tweet in tweets:
        print(tweet.id)
        net.add_node(tweet.id, tweet.title)
    return net