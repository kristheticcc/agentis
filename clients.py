# Imports
import os
from dotenv import load_dotenv
from openai import OpenAI

# Loading environment variables
load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

# Models
gpt_model = "o4-mini"
groq_model = "llama3.3"

# Clients
openai = OpenAI()
groq = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=groq_api_key)

