"""
this will use the Database instead of temporary momory saving
this will make the everything remembered for the rest of the use of those conversation by the 'Agent'
"""
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from AgentUtils import AgentUtils
from RootAgent import root_agent
from RunSession import run_session
import asyncio


db_url = "sqlite:///my_agent_data.db"  # Local SQLite file

AgentUtils.session_service = DatabaseSessionService(db_url=db_url)

"""
 step2:- Switch to the DatabaseSessionService
 for this database will be used 'sqlite' to store datas
"""

db_url = "sqlite:///my_agent_data.db"  # Local SQLite file

session_service = DatabaseSessionService(db_url=db_url)

AgentUtils.session_service = session_service

runner = Runner(
    agent=root_agent,
    app_name=AgentUtils.APP_NAME,
    session_service=AgentUtils.session_service # new session
)

async def main():
    a1:list=[
        "Hi, I am Yousuf! What is the capital of United States?",
        "Hello! What is my name?",  # This time, the agent should remember!
    ]

    a2:list=[
        "What did I ask you about earlier?",
        "And remind me, what is my name?"
    ] # after reseting karnel (notebook) or again running the program will remember the previous conversation

    a3:list = a1.__add__(a2)

    await run_session(
        runner,
        a2,
        "test-db-session-01",
        session_service=AgentUtils.session_service
    )

if __name__=='__main__':
    asyncio.run(main())
