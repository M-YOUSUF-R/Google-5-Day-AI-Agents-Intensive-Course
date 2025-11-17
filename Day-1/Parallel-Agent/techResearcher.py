from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from config import Config

tech_researcher = Agent(
    name="TechResearcher",
    model=Gemini(
        model='gemini-2.5-flash',
        retry_options = Config.retry_config,
        api_key = Config.api_key
    ),
    instruction = """Research the latest AI/ML trends. Include 3 key developments,
    the main companies involved, and the potential impact. Keep the report very concise (100 words).""",
    tools=[google_search],
    output_key = "tech_research",
)
