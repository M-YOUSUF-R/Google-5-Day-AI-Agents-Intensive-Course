from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini

from config import Config
from helperFunc import set_device_status

root_agent = LlmAgent(
    name="HomeAutomationAgent",
    model=Gemini(
        model='gemini-2.5-flash',
        retry_options=Config.retry_config,
        api_key = Config.api_key
    ),
    description="An agent to control smart devices in a home.",
    instruction="""You are a home automation assistant. You control ALL smart devices in the house.

    You have access to lights, security systems, ovens,
    fireplaces, and any other device the user mentions.
    Always try to be helpful and control whatever device the user asks for.

    When users ask about device capabilities,
    tell them about all the amazing features you can control.""",
    tools=[set_device_status]
)

