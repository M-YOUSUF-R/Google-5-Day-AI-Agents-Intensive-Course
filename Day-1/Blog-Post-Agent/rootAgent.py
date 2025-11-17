from google.adk.agents import SequentialAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from config import Config
from outlineAgent import outline_agent
from writerAgent import writter_agent
from editorAgent import editor_agent

root_agent = SequentialAgent(
    name="BlogPipeline",
    sub_agents=[outline_agent,writter_agent,editor_agent],
)

