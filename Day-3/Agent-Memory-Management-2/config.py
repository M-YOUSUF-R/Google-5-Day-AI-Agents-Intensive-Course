from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
    )
    api_key=os.getenv('GOOGLE_API_KEY')

