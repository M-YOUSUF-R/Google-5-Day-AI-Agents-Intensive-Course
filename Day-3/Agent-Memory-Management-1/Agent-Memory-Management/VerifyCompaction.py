from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService

from AgentUtils import AgentUtils

USER_ID = AgentUtils.USER_ID

async def verify_compaction(runner:Runner=None,
    session_service:DatabaseSessionService=None,
    session_id:str='default'
    ):
    final_session = await session_service.get_session(
        app_name=runner.app_name,
        user_id=USER_ID,
        session_id=session_id,
    )

    print("--- Searching for Compaction Summary Event ---")
    found_summary = False
    for event in final_session.events:
        # Compaction events have a 'compaction' attribute
        if event.actions and event.actions.compaction:
            print("\n✅ SUCCESS! Found the Compaction Event:")
            print(f"  Author: {event.author}")
            print(f"\n Compacted information: {event}")
            found_summary = True
            break

    if not found_summary:
        print(
            "\n❌ No compaction event found. Try increasing the number of turns in the demo."
        )
