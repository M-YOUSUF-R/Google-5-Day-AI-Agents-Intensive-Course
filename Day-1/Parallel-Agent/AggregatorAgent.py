from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search

from config import Config

aggregator_agent = Agent(
    name="AggeregatorAgent",
    model=Gemini(
        model='gemini-2.5-flash',
        retry_options = Config.retry_config,
        api_key=Config.api_key
    ),
    instruction ="""Combine these three research findings into a single executive summary:
    **Technology Trends:**
    {tech_research}

    **Health Breakthroughs:**
    {health_research}

    **Finance Innovations:**
    {finance_research}

    Your summary should highlight common themes, surprising connections, and the most important key takeaways from all three reports. The final summary should be around 200 words.""",
    tools=[google_search],
    output_key = "executive_summary",
)
