from django.shortcuts import render
from django.http import HttpResponse
from sonderPyvis.network import Network
from openai import OpenAI
import os
import json

from django.contrib.auth.models import User
from random import choice, randint, sample
from datetime import datetime, timedelta
from scipy.spatial.distance import cosine
    


def experiment(request):
    
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

   