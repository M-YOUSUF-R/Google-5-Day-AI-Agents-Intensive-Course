from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from config import Config
from MCP_image_server import mcp_image_server

root_agent = LlmAgent(
    name="image_agent",
    model=Gemini(
        model='gemini-2.5-flash',
        retry_options=Config.retry_config,
        api_key=Config.api_key
    ),
    instruction="Use the MCP Tool to generate images for user queries",
    tools=[mcp_image_server]
)

