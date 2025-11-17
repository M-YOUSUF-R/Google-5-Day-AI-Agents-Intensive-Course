from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types
from config import Config


outline_agent = Agent(
    name="OutlineAgent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_config = Config.retry_config,
        api_key=Config.api_key
    ),
    instruction = """
    Create a blog outline for the given topic with:
    1. A catchy headline like: (Headline- The Headline)
    2. An introduction hook
    3. 3-5 main sections with 2-3 bullet points for each
    4. A concluding thought
    """,
    output_key = "blog_outline"

)


