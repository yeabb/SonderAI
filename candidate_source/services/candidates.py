# from .models import TweetNode
from openai import OpenAI
import os

class Candidates:
    def __init__():
        pass
    
    def get_all_candidates():
        # tweets = TweetNode.objects.all()   
        # return tweets
        pass
    
    def initOpenAI():
        client = OpenAI()
        OpenAI.api_key = os.environ["OPENAI_API_KEY"]
        return client