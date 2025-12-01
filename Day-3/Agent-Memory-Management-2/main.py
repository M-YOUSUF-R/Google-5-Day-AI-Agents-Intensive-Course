from google.adk.runners import Runner
from google.adk.memory import InMemoryMemoryService
from google.adk.sessions import InMemorySessionService

from RootAgent import root_agent,new_root_agent, auto_memory_agent
from RunSession import run_session

import asyncio


APP_NAME = 'MemoryDemoApp'
USER_ID = "demo_user"
MODEL_NAME='gemini-2.5-flash'
SESSION_ID = "conversation-01"

memory_service = (
    InMemoryMemoryService()
)

session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
    memory_service=memory_service
)

new_runner = Runner(
    agent=new_root_agent,
    app_name=APP_NAME,
    session_service=session_service,
    memory_service=memory_service
)

auto_runner = Runner(
    agent=auto_memory_agent,
    app_name=APP_NAME,
    session_service=session_service,
    memory_service=memory_service
)

async def main():
    await run_session(
        runner_instance=runner,
        user_queries="My favorite color is blue-green. Can you write a Haiku about it?",
        session_id="conversation-01",
        session_service=session_service,
        APP_NAME=APP_NAME,
        MODEL_NAME=MODEL_NAME,
        USER_ID=USER_ID
    )

    # let's see what inside the session
    print("-"*55)
    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id= SESSION_ID
    )
    for event in session.events:
        text:str = (
            event.content.parts[0].text[:60] if event.content and event.content.parts else "empty"
        )
        print(f"{event.content.role}:{text}...")
    # as `session` holds the conversation , let's transfer it to `memory_service`
    await memory_service.add_session_to_memory(session)



async def new_main():
    await run_session(
        runner_instance=new_runner,
        user_queries="My favorite color is blue-green. Can you write a Haiku about it?",
        session_id="conversation-01",
        session_service=session_service,
        APP_NAME=APP_NAME,
        MODEL_NAME=MODEL_NAME,
        USER_ID=USER_ID
    )
    #"--manually save that to the memory--"
    color_session = await session_service.get_session(
        app_name=APP_NAME,user_id=USER_ID,session_id='conversation-01'
    )
    await memory_service.add_session_to_memory(color_session)

    """
    await run_session(
        APP_NAME=APP_NAME,
        USER_ID=USER_ID,
        MODEL_NAME=MODEL_NAME,
        runner_instance=runner,
        user_queries=[
          "my favorite color is green"
        ],
        session_id="color-test",
        session_service=session_service
    )
    #"--manually save that to the memory--"
    color_session = await session_service.get_session(
        app_name=APP_NAME,user_id=USER_ID,session_id='color-test'
    )
    await memory_service.add_session_to_memory(color_session)
    """
    await run_session(
        APP_NAME=APP_NAME,
        USER_ID=USER_ID,
        MODEL_NAME=MODEL_NAME,
        runner_instance=new_runner,
        user_queries=[
            "What is my favorite color?",
        ],
        session_id= "color-test",#conversation-01,
        session_service=session_service
    )

    await run_session(
        APP_NAME=APP_NAME,
        USER_ID=USER_ID,
        MODEL_NAME=MODEL_NAME,
        runner_instance=new_runner,
        user_queries=[
            "My birthday is on 16 May 2003",
        ],
        session_id="birthday-session-01",
        session_service=session_service
    )

    #"--manually save that to the memory--"
    birthday_session = await session_service.get_session(
        app_name=APP_NAME,user_id=USER_ID,session_id='birthday-session-01'
    )
    await memory_service.add_session_to_memory(birthday_session)

    #"--testing the retrieval in new session: `birthday-session-02`--"
    await run_session(
        APP_NAME=APP_NAME,
        USER_ID=USER_ID,
        MODEL_NAME=MODEL_NAME,
        runner_instance=new_runner,
        user_queries=[
            "When I was born?",
        ],
        session_id="birthday-session-02",
        session_service=session_service
    )
    # manual search respose
    search_respose = await memory_service.search_memory(
            app_name=APP_NAME,user_id=USER_ID,
            query="Haiku,birthday,color"
            )
    print("-"*55)
    print("search result:")
    print(f"found {len(search_respose.memories)} relevant memories")
    print("-memoryies-")
    # let's search what inside the `memories`
    for memory in search_respose.memories:
        if memory.content and memory.content.parts:
            text = memory.content.parts[0].text[:80]
            print(f"[{memory.author}]: {text}...")


async def auto_main():
    await run_session(
        APP_NAME=APP_NAME,
        USER_ID=USER_ID,
        MODEL_NAME=MODEL_NAME,
        runner_instance=auto_runner,
        user_queries="I gifted a new toy to my nephew on his 1st birthday!",
        session_id="auto-save-test",
        session_service=session_service

    )
    await run_session(
        APP_NAME=APP_NAME,
        USER_ID=USER_ID,
        MODEL_NAME=MODEL_NAME,
        runner_instance=auto_runner,
        user_queries="What I gifted to my nephew and when?",
        session_id="auto-save-test",
        session_service=session_service

    )

if __name__=='__main__':
    #asyncio.run(main())
    asyncio.run(new_main())
    #asyncio.run(auto_main())
