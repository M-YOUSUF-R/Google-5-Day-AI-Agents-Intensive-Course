"""
THIS SECTION IS ABOUT 'Context Compaction'

let's create an 'App' that will be for research purpose , it will manage the `compaction` and it will use our chatbot-agent `root_agent` for it's conversation
"""
from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.tools.tool_context import ToolContext
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner

from RootAgent import root_agent
from RunSession import run_session
from VerifyCompaction import verify_compaction

import asyncio

researcher_app_compacting = App(
    name='ResearchAppCompaction',
    root_agent= root_agent,
    events_compaction_config = EventsCompactionConfig(
        compaction_interval=3, # Trigger compaction every 3 invocations
        overlap_size=1, # Keep 1 previous turn for context
    ),
)

db_url = "sqlite:///my_agent_data.db"  # Local SQLite file
session_service = DatabaseSessionService(db_url=db_url)

researcher_runner_compacting = Runner(
    app=researcher_app_compacting,
    session_service=session_service
)

async def main():
    response = await run_session(
        researcher_runner_compacting,
        "What is the latest news about AI in healthcare?",
        "compaction_demo-1",
        session_service=session_service
    )
    print("-"*50)

    # Turn 2
    response = await run_session(
        researcher_runner_compacting,
        "Are there any new developments in drug discovery?",
        "compaction_demo-1",
        session_service=session_service
    )
    print("-"*50)

    # Turn 3 - Compaction should trigger after this turn!
    response = await run_session(
        researcher_runner_compacting,
        "Tell me more about the second development you found.",
        "compaction_demo-1",
        session_service=session_service
    )
    print("-"*50)


    # Turn 4
    response = await run_session(
        researcher_runner_compacting,
        "Who are the main companies involved in that?",
        "compaction_demo-1",
        session_service=session_service
    )
    print("-"*50)

# asyncio.run(main())

asyncio.run(
    verify_compaction(
        runner=researcher_runner_compacting,
        session_service=session_service,
        session_id= "compaction_demo-1"
    )
)
