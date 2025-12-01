from google.adk.agents import LlmAgent,Agent
from google.adk.tools import load_memory,preload_memory
from google.adk.models.google_llm import Gemini

from config import Config
from memory import Memory

root_agent = LlmAgent(
    model = Gemini(
        model='gemini-2.5-flash',
        api_key=Config.api_key,
        retry_options = Config.retry_config
    ),
    name='MemoryDemoAgent',
    instruction = 'Answer user questions in simple words.',
)

new_root_agent = LlmAgent(
    model = Gemini(
        model='gemini-2.5-flash',
        api_key=Config.api_key,
        retry_options = Config.retry_config
    ),
    name='MemoryDemoAgent',
    instruction = 'Answer user questions in simple words. Use `load_memory` tool if you need to recall past conversations.',
    tools=[
        preload_memory # Agent now has access to Memory and can search it whenever it decides to!
    ]
)

auto_memory_agent = LlmAgent(
    model=Gemini(
        model='gemini-2.5-flash',
        api_key=Config.api_key,
        retry_options=Config.retry_config
    ),
    name='AutoMemoryAgent',
    tools=[preload_memory],
    after_agent_callback=Memory.auto_save_to_memory,
)
