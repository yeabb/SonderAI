from .openAIClientProvider import OpenAIClientProvider
from .pineConeClientProvider import PineConeClientProvider

class Embedding:
    
    def __init__(self):
        self.OpenAIClient = OpenAIClientProvider()
        self.pineConeClient = PineConeClientProvider()
    
    def generate_embedding(self, tweet_node):
        metadata = f"{tweet_node.title} {tweet_node.content}"
        embedding_response = self.OpenAIClient.generate_embedding(metadata)
        
        embedding_doc = {
            "tweet_id": tweet_node.id,
            "embedding": embedding_response.data[0].embedding,
            "metadata": metadata
        }
        
        self.persist_embedding(embedding_doc)  # TODO we need a try - catch here to ensure persisting worked
        return embedding_doc    
    
    def persist_embedding(self, embedding_doc):
        self.pineConeClient.persist_embedding(embedding_doc)
        
    def query_vector_embeddings(self, input_query_vector):
        return self.pineConeClient.query_embeddings(input_query_vector)