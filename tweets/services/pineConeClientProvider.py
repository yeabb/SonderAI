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
        self.index = None
        self.dimention = 1024
        self.metric = "cosine"
        
        self._ensure_index()
        self.index = self.pc.Index(self.index_name)
        
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
    
    def persist_embedding(self, embedding_doc): #TODO we have to change this from utility(non return type) to a return type function
        """
        Persists an embedding into the Pinecone index.

        Args:
            embedding_doc (dict): A dictionary containing 'tweet_id', 'embedding', and 'tweet_metadata'.
        """
        
        vector = {
            "id": str(embedding_doc["tweet_id"]),  # ID must be a string as required by Pinecone
            "values": embedding_doc["embedding"],
            "metadata": {"text": embedding_doc["metadata"]}
            }
        
        self.index.upsert([vector])   
        
        
    def query_embeddings(self, input_query_vector):
        """ 
        This method queries the index for the top_k most similar vectors
        
        Args:
            input_query_vector: an embedding vector to query the most similar embeddig vectors from the pinecone database
            
        Returns:
            A list of dicts 
            
           Example >>>
           
            [
                {'id': 'vec2',
                'metadata': {'text': 'The tech company Apple is known for its '
                                    'innovative products like the iPhone.'},
                'score': 0.8727808,
                'sparse_values': {'indices': [], 'values': []},
                'values': [-0.006929283495992422,-0.005336422007530928, -4.547132266452536e-05,-0.024047505110502243]
                },
                
                {'id': 'vec4',
                'metadata': {'text': 'Apple Inc. has revolutionized the tech '
                                    'industry with its sleek designs and '
                                    'user-friendly interfaces.'},
                'score': 0.8526099,
                'sparse_values': {'indices': [], 'values': []},
                'values': [-0.006929283495992422,-0.005336422007530928, -4.547132266452536e-05,-0.024047505110502243]
                }
            
            ]
            
        """
        
        results = self.index.query(
            vector = input_query_vector,
            top_k = 25,
            include_values = True,
            include_metadata = True
        ) 
        
        return results["matches"]     
    
    
