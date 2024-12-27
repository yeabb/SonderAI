import os
import pinecone
from pinecone import ServerlessSpec
import time

class PineConeClientProvider:
    
    def __init__(self):
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            raise ValueError("PINECONE_API_KEY is not set in environment variables.")
        
        pinecone.init(
            api_key = api_key,
            enviroment = "us-east-1"
        )
        
        self.index_name = "example_index"
        self.dimention = 1024
        self.metric = "cosine"
        
        self._ensure_index()
        
    def _ensure_index(self):
        """
        Ensures the Pinecone index is created if it doesn't already exist
        """
        if not pinecone.list_indexes() or self.index_name not in pinecone.list_indexes():
            pinecone.create_index(
                name = self.index_name,
                dimension = self.dimention,
                metric = self.metric,
                spec = ServerlessSpec(
                    cloud = 'aws',
                    region = "us-east-1"
                )
            )
    
    def persist_embedding(self, embedding_doc):
        """
        Persists an embedding into the Pinecone index.

        Args:
            doc (dict): A dictionary containing 'tweet_id', 'embedding', and 'tweet_metadata'.
        """
        
        index = pinecone.Index(self.index_name)
        
        vector = {
            "id": embedding_doc["tweet_id"],  # ID must be a string as required by Pinecone
            "values": embedding_doc["embedding"],
            "metadata": embedding_doc["tweet_metadata"]
            }
        
        index.upsert(vector)   
    
    
        