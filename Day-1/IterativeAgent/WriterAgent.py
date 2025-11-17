from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from config import Config

writing_agent = Agent(
    name="InitialWritingAgent",
    model = Gemini(
        model = 'gemini-2.5-flash',
        retry_options = Config.retry_config,
        api_key = Config.api_key
    ),
    instruction = """Based on the user's prompt, write the first draft of a short story (around 100-150 words).
    Output only the story text, with no introduction or explanation.""",
    output_key = "current_story"

)
