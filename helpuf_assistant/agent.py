# from google.adk.agents import Agent
#
# Mock tool implementation
# def get_current_time(city: str) -> dict:
    # """Returns the current time in a specified city."""
    # return {"status": "success", "city": city, "time": "10:30 AM"}
#
# root_agent = Agent(
    # model='gemini-2.5-flash',
    # name='helpful_assistant',
    # description="Tells the current time in a specified city.",
    # instruction="You are a helpful assistant that tells the current time in cities. Use the 'get_current_time' tool for this purpose.",
    # tools=[get_current_time],
# )
import asyncio
from google.adk.agents import Agent
import google.generativeai as genai
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types
from dotenv import load_dotenv
import os
load_dotenv()

print("✅ ADK components imported successfully.")

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1, # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504] # Retry on these HTTP errors
)
root_agent = Agent(
    name="helpful_assistant",
    model= Gemini(
        api_key= os.getenv('GOOGLE_API_KEY'),
        model = "gemini-2.5-flash",
        retry_options = retry_config,
    ),
    description = "A simple agent that can answer general questions.",
    instruction="You are a helpful assistant. Use Google Search for current info or if unsure.",
    tools=[google_search]
)

runner = InMemoryRunner(agent=root_agent)

async def main():
    response = await runner.run_debug(
    "what is the Agent Development kit from Google? what language is the  SDK available in? "
    )

asyncio.run(main())
