from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini

from config import Config

critic_agent = Agent(
    name = "CriticAgent",
    model = Gemini(
        model="gemini-2.5-flash",
        retry_options=Config.retry_config,
        api_key = Config.api_key
    ),
    instruction = """You are a constructive story critic. Review the story provided below.
    Story: {current_story}

    Evaluate the story's plot, characters, and pacing.
    - If the story is well-written and complete, you MUST respond with the exact phrase: "APPROVED"
    - Otherwise, provide 2-3 specific, actionable suggestions for improvement.""",
    output_key="critique"
)
