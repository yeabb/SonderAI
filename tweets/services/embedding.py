from openAIClientProvider import OpenAIClientProvider
from pineConeClientProvider import PineConeClientProvider

class Embedding:
    
    def __init__(self):
        self.OpenAIClient = OpenAIClientProvider().getOpenAIClient
        self.pineConeClient = PineConeClientProvider()
    
    def generate_embedding(self, tweet):
        embedding_response = self.OpenAIClient.embeddings.create(
            input = tweet.content,
            model = "text-embedding-3-small"
        )
        
        embedding_doc = {
            "tweet_id": tweet.id,
            "embedding":embedding_response["data"][0]["embedding"],
            "tweet_metadata": tweet.metadata
        }
        
        self.persist_embedding(embedding_doc)  # TODO we need a try - catch here to ensure persisting worked
        return embedding_doc    
    
    def persist_embedding(self, embedding_doc):
        self.pineConeClient.persist_embedding(embedding_doc)