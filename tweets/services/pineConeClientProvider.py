import os
from pinecone import Pinecone, ServerlessSpec
import time

class PineConeClientProvider:
    
    def __init__(self):
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            raise ValueError("PINECONE_API_KEY is not set in environment variables.")
        
        self.pc = Pinecone(
            api_key = api_key
        )
        
        self.index_name = "example-index"
        self.dimention = 1024
        self.metric = "cosine"
        
        self._ensure_index()
        
    def _ensure_index(self):
        """
        Ensures the Pinecone index is created if it doesn't already exist
        """
        if not self.pc.list_indexes() or self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name = self.index_name,
                dimension = self.dimention,
                metric = self.metric,
                spec = ServerlessSpec(
                    cloud = 'aws',
                    region = "us-east-1"
                )
            )
            
        while not self.pc.describe_index(self.index_name).status['ready']:
            time.sleep(1)
    
    def persist_embedding(self, embedding_doc):
        """
        Persists an embedding into the Pinecone index.

        Args:
            embedding_doc (dict): A dictionary containing 'tweet_id', 'embedding', and 'tweet_metadata'.
        """
        
        index = self.pc.Index(self.index_name)
        
        vector = {
            "id": str(embedding_doc["tweet_id"]),  # ID must be a string as required by Pinecone
            "values": embedding_doc["embedding"],
            "metadata": {"text": embedding_doc["metadata"]}
            }
        
        index.upsert([vector])   
        
        
    
        