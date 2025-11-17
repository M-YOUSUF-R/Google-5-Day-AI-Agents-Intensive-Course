from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from config import Config

health_researcher = Agent(
    name="HealthResearcher",
    model=Gemini(
        model='gemini-2.5-flash',
        retry_options = Config.retry_config,
        api_key = Config.api_key
    ),
    instruction = """Research recent medical breakthroughs. Include 3 significant advances,their practical applications, and estimated timelines. Keep the report concise (100 words).""",
    tools=[google_search],
    output_key = "health_research",
)
