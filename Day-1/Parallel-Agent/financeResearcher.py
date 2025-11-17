from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from config import Config

finance_researcher = Agent(
    name="FinanceResearcher",
    model=Gemini(
        model='gemini-2.5-flash',
        retry_options = Config.retry_config,
        api_key = Config.api_key
    ),
    instruction = """Research current fintech trends. Include 3 key trends,
    their market implications, and the future outlook. Keep the report concise (100 words).""",
    tools=[google_search],
    output_key = "finance_research",
)
