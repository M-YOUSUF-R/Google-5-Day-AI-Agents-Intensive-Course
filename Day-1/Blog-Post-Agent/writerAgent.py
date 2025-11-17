from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types
from config import Config


writter_agent = Agent(
    name="WritterAgent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_config = Config.retry_config,
        api_key=Config.api_key
    ),
    instruction = """Following this outline strictly: {blog_outline}
    Write a brief, 200 to 300-word blog post with an engaging and informative tone.""",
    output_key = "blog_draft",
)
