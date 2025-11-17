from google.adk.agents import Agent,LlmAgent
from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.models.google_llm import Gemini
from google.adk.sessions import DatabaseSessionService
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools.tool_context import ToolContext
from google.genai import types

from typing import Any , Dict

async def run_session(
    runner_instance: Runner,
    user_queries:list[str] | str =None,
    session_name:str="default"
    ):
    print(f"\n ### Session: {session_name}")

    app_name = runner_instance.app_name

    try:
        session = await session_service.create_session(
            app_name=app_name, user_id= USER_ID,session_id = session_name
        )
    except:
        session = await session_service.get_session(
            app_name=app_name,user_id=USER_ID,session_id=session_name
        )

    if user_queries:
        if type(user_queries) == str:
            user_queries = [user_queries]

        for query in user_queries:
            print("\nUser > ",query);
            query = types.Content(role='user',parts=[types.Part(text=query)])

            async for event in runner_instance.run_async(
                user=USER_ID,session_id=session.id,new_message=query
            ):
                if event.content and event.content.parts:
                    if(
                        (event.content.parts[0].text).lower() != "None".lower() and
                        event.content.parts[0].text
                    ):
                        print(f"{MODEL_NAME}> ",event.content.parts[0].text)
    else:
        print("no queries")

