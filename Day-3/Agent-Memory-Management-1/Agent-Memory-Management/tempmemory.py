from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from RootAgent import root_agent
from AgentUtils import AgentUtils
from RunSession import run_session

import asyncio

AgentUtils.session_service = InMemorySessionService() # InMemorySessionService stores conversations in RAM (temporary)

runner = Runner(agent=root_agent,
    app_name=AgentUtils.APP_NAME,
    session_service=AgentUtils.session_service
)

async def main():
    a1:list=[
        "Hi, I am Yousuf! What is the capital of United States?",
        "Hello! What is my name?",  # This time, the agent should remember!
    ]

    a2:list=[
        "What did I ask you about earlier?",
        "And remind me, what's my name?"
    ] # after reseting karnel (notebook) or again running the program will forget the previous conversation

    a3:list = a1.__add__(a2)

    await run_session(
        runner,
        # a1, # it will be forgotten after the program / kernel restart.
        a2, # it has no Idea about `a1`.
        # a3, # it as it reminds , it will answer all questions.
        "stateful-agentic-session",
        session_service=AgentUtils.session_service
    )

asyncio.run(main())
