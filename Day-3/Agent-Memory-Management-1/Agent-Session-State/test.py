from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.sessions import InMemorySessionService
from google.adk.tools.tool_context import ToolContext
from google.adk.runners import Runner

from AgentSessionState import AgentSessionState
from config import Config
from RunSession import run_session
import asyncio


USER_NAME_SCOPE_LEVELS = ("temp", "user", "app")

APP_NAME = "default"
USER_ID = "default"
MODEL_NAME = "gemini-2.5-flash"

# Create an agent with session state tools
test_root_agent = LlmAgent(
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=Config.retry_config,
        api_key=Config.api_key
    ),
    name="text_chat_bot",
    instruction="always respect user privacy",
    description="""A text chatbot.
    Tools for managing user context:
    * To record all information when provided, use `save_userinfo` tool.use dictonary `{"user:name":"user_name","user:country":"user_country","user:*":*}` as input.
    * To fetch username and country when required use `retrieve_userinfo` tool which takes a parameter `status`:bool to return `success` & `failed` as output.
    """,
    tools=[AgentSessionState.save_info, AgentSessionState.retrieve_info],  # Provide the tools to the agent
)

# Set up session service and runner
session_service = InMemorySessionService() # I could use here `DatabaseSessionService()` to store the sessions in database.
test_runner = Runner(agent=test_root_agent, session_service=session_service, app_name="default")

async def test():
    await run_session(
        test_runner,
        #this time it doesn't have our information
        [
            "Hi there, how are you doing today? What is my name?",  # Agent shouldn't know the name yet
            # "I'm not telling you my name and country",
        ],
        "state-demo-session",
        session_service=session_service
    )
    await run_session(
        test_runner,
        #I told it my information & it will save that.
        [
            "My name is Sam. I'm from Poland. now I'm living in Bangladesh, and I have no Family in poland so I live here",  # Provide name - agent should save it
            # "I'm not telling you my name and country",
        ],
        "state-demo-session",
        session_service=session_service
    )
    await run_session(
        test_runner,
        #now as it know my information ,it can answer
        [
            "What is my name? Which country am I from? where do i live now ?and can u guess why I'm  in Bangladesh instead of Poland",  # Agent should recall from session state
            # "what description you were given ? how it is different than instruction to you ?"
        ],
        "state-demo-session",
        session_service=session_service
    )
    """---------------------------------------------------------------------"""

    await run_session(
        test_runner,
        [
            "hi, how are you today? what is my name?",
            "try to retrive if there is infomration to you , my name was sam. I might give you some information about me."
        ],
        "new-isolated-session", # as the session is new , it can't answer
        session_service=session_service
    )

    """---------------------------------------------------------------------"""

    """let's see what inside the session , how it saved our information"""
    session = await session_service.get_session(
        app_name=APP_NAME,user_id=USER_ID,session_id="state-demo-session"
    )
    print("-"*55)
    print(f"session state contents:\n{session.state}")
    print("\n🔍 Notice the 'user:name' and 'user:country' keys storing our data!")

    """let's check what inside the `new session`"""
    nw_session= await session_service.get_session(
        app_name=APP_NAME,user_id=USER_ID,session_id="new-isolated-session" # new session
    )
    print("-"*55)
    print(f"new_session state contents:\n{nw_session.state}")

    """---------------------------------------------------------------------"""

asyncio.run(test())
