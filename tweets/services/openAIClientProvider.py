from openai import OpenAI
import os

class OpenAIClientProvider:
    def __init__(self):
        self.client = OpenAI()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.dimensions = 1024
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not set in environment variables.")
        
        self.client.api_key = self.api_key
    
    #TODO: add a try: catch here to catch service call failures, errors and timeouts
    def generate_embedding(self, tweet_content):
        return self.client.embeddings.create(
            input = tweet_content,
            model = "text-embedding-3-small",
            dimensions = self.dimensions
            )