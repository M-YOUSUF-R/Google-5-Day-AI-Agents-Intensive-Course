from google.adk.runners import Runner

# from AgentUtils import AgentUtils

# USER_ID = AgentUtils.USER_ID
# APP_NAME = AgentUtils.APP_NAME
# MODEL_NAME = AgentUtils.MODEL_NAME

APP_NAME = "default"
USER_ID = "default"
MODEL_NAME = "gemini-2.5-flash"

async def run_session(
    runner_instance: Runner,
    user_queries:list[str] or str =None,
    session_name:str="default",
    session_service=None,
    ):
    print(f"\n ### Session: {session_name}")

    app_name = runner_instance.app_name or APP_NAME

    try:
        session = await session_service.create_session(
            app_name=app_name, user_id= USER_ID,session_id = session_name
        )
        print("session created...")
    except:
        session = await session_service.get_session(
            app_name=app_name,user_id=USER_ID,session_id=session_name
        )
        print("session found...")

    if user_queries:
        if type(user_queries) == str:
            user_queries = [user_queries]

        for query in user_queries:
            print("\nUser > ",query);
            query = types.Content(role='user',parts=[types.Part(text=query)])

            async for event in runner_instance.run_async(
                user_id=USER_ID,session_id=session.id,new_message=query
            ):
                if event.content and event.content.parts:
                    if(
                        str((event.content.parts[0].text)).lower() != "None".lower() and
                        event.content.parts[0].text
                    ):
                        print(f"{MODEL_NAME}> ",event.content.parts[0].text)
    else:
        print("no queries")
