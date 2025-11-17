from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import FunctionTool,tool_context
from config import Config

def loop_exit():
    """Call this function ONLY when the critique indicates no further changes are needed, signaling the iterative process should end."""
    print(f"  [Tool Call] exit_loop triggered by {tool_context.agent_name}")
    tool_context.actions.escalate = True
    # Return empty dict as tools should typically return JSON-serializable output
    return {"status": "approved", "message": "Story approved. Exiting refinement loop."}

refine_agent = Agent(
    name="RefinerAgent",
    model=Gemini(
        model='gemini-2.5-flash',
        retry_options = Config.retry_config,
        api_key=Config.api_key
    ),
    instruction="""You are a story refiner. You have a story draft and critique.

    Story Draft: {current_story}
    Critique: {critique}

    Your task is to analyze the critique.
    - IF the critique is EXACTLY "APPROVED", you MUST call the `exit_loop` function and nothing else.
    - OTHERWISE, rewrite the story draft to fully incorporate the feedback from the critique.""",
    output_key="current_story" , # It overwrites the story with the new, refined version.
    tools=[
        FunctionTool(loop_exit)
    ],
)

