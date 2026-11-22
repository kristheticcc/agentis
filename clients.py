# Imports
import os
from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI

# Loading environment variables
load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

# Models
gpt_model = "gpt-6.1-terra"                            # replaced gpt-5-mini after the model deprecation notice
groq_model = "openai/gpt-oss-120b"

# Clients
openai = OpenAI()
groq = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=groq_api_key)
openai_async = AsyncOpenAI()

