from google.genai import types
from dotenv import load_dotenv
import os
load_dotenv()

class Config:
    retry_option=types.HttpRetryOptions(
        attempts=5,
        exp_base=7,
        initial_delay=1,
        http_status_codes=[429,500,503,504]
    )
    api_key = os.getenv("GOOGLE_API_KEY")
    
