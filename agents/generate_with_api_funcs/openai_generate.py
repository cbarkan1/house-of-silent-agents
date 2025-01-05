"""
OpenAI API key must be stored in a .env file in the generate_with_api_funcs directory
.env file should contain:
OPENAI_API_KEY = "<insert api key here>"
"""

import os
import openai
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

def create_generate(model):
    def generate(message_record):
        response = client.chat.completions.create(
            model=model, messages=message_record)
        return response.choices[0].message.content
    return generate