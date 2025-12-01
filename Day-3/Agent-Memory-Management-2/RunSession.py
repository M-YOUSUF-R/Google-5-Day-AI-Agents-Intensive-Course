from google.adk.runners import Runner
from google.genai import types



async def run_session(
    APP_NAME:str,
    USER_ID:str,
    MODEL_NAME:str,
    runner_instance:Runner,
    user_queries:list[str] or str,
    session_id:str='default',
    session_service=None,
):
    print(f"\n### Session: {session_id}")

    # crete or retrieve session
    app_name = runner_instance.app_name or APP_NAME
    try:
        session = await session_service.create_session(
            app_name=app_name,user_id=USER_ID,session_id=session_id
        )
        print('session created...')

    except Exception:
        session = await session_service.get_session(
            app_name=APP_NAME,user_id=USER_ID,session_id=session_id
        )
        print('session found...')

    # convert `user_queries` to `list`
    if type(user_queries) == str:
        user_queries = [user_queries]

    # process each queries
    for query in user_queries:
        print(f"\nuser > {query}")

        query_content = types.Content(role='user',parts=[types.Part(text=query)])

        # Stream agent response
        async for event in runner_instance.run_async(
            user_id=USER_ID,session_id=session_id,new_message=query_content
        ):
            if event.is_final_response() and event.content and event.content.parts:
                text = event.content.parts[0].text
                if text and text != 'None':
                    print(f"{MODEL_NAME} > {text}")
