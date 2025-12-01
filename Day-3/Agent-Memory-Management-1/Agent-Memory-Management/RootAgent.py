from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from config import Config

root_agent = LlmAgent(
    name='TextChatBot',
    model= Gemini(
        model='gemini-2.5-flash',
        retry_options=Config.retry_config,
        api_key=Config.api_key,
    ),
    description="A text Chatbot",
)
