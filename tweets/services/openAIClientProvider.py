from openai import OpenAI
import os

class OpenAIClientProvider:
    def __init__(self):
        self.client = OpenAI()
        
    def getOpenAIClient(self):
        self.client.api_key = os.environ["OPENAI_API_KEY"]
        return self.client