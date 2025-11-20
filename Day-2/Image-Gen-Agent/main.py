import uuid
from google.genai import types

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

from google.adk.apps.app import App, ResumabilityConfig
from google.adk.tools.function_tool import FunctionTool

import asyncio

from config import Config

MAX_IMAGE_COUNT:int = 1

def generate_image(num_image:int,tool_context:ToolContext):
    if num_image <= MAX_IMAGE_COUNT and num_image > 0:
        return {
            "status":"approved",
            "img_id":f"IMG-{num_image}-AUTO",
            "message":f"Generation approved:{num_image} Image Generated"
        }
    if not tool_context.tool_confirmation:
        tool_context.request_confirmation(
            hint=f"Generation Request: {num_image}.\nDo you want to approve? ",
            payload={"num_image":num_image}
        )
        return {
            "status":"pending",
            "message":f"Generation of {num_image} of image requires approval",
        }
    if tool_context.tool_confirmation.confirmed:
        return {
            "status":"approved",
            "img_id":f"IMG-{num_image}-AUTO",
            "message":f"{num_image} Image Generated",
        }
    else:
        return {
            "status":"rejected",
            "message":f"Generation Rejected: {num_image} of image generation rejected"
        }

mcp_image_server = McpToolset(
    connection_params= StdioConnectionParams(
        server_params=StdioServerParameters(
            command='npx',
            args=[
                '-y',
                "@modelcontextprotocol/server-everything",
            ],
            tool_filter=["getTinyImage"],
        ),
        timeout=30,
    )
)
generatior_agent = LlmAgent(
    name="GeneratiorAgent",
    model=Gemini(
        model='gemini-2.5-flash',
        retry_options=Config.retry_config,
        api_key=Config.api_key
    ),
    instruction="""You are an image generator.

    when user request to generate image:
    1. Use generate_image tool with the number of image.
    2. Use the MCP Tool to generate images for user queries
    3. If the generation status is 'pending',inform the user that approval is required.
    4. After receiving the final result, provide a clear summary including:
        - Generation status (approved/rejected)
        - Image id (if available)
    5. Keep response concise but informative
    """,
    tools=[FunctionTool(func=generate_image),mcp_image_server]
)

generation_app = App(
    name='ImageGeneratiorApp',
    root_agent=generatior_agent,
    resumability_config=ResumabilityConfig(is_resumable=True)
)

session_service = InMemorySessionService()

generation_runner = Runner(
    app=generation_app,
    session_service=session_service
)

def check_for_approval(events):
    """Check if events contain an approval request.

    Returns:
        dict with approval details or None
    """
    for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if (
                    part.function_call
                    and part.function_call.name == "adk_request_confirmation"
                ):
                    return {
                        "approval_id": part.function_call.id,
                        "invocation_id": event.invocation_id,
                    }
    return None

def print_agent_response(events):
    """Print agent's text responses from events."""
    for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(f"Agent > {part.text}")

def create_approval_response(approval_info, approved):
    """Create approval response message."""
    confirmation_response = types.FunctionResponse(
        id=approval_info["approval_id"],
        name="adk_request_confirmation",
        response={"confirmed": approved},
    )
    return types.Content(
        role="user", parts=[types.Part(function_response=confirmation_response)]
    )

async def image_gen_workflow(query: str, auto_approve: bool = True):
    """Runs a image generation workflow with approval handling.

    Args:
        query: Image generation request
        auto_approve: Whether to auto-approve large numbers (simulates human decision)
    """

    print(f"\n{'='*20}")
    print(f"User > {query}\n")

    # Generate unique session ID
    session_id = f"order_{uuid.uuid4().hex[:8]}"

    # Create session
    await session_service.create_session(
        app_name="ImageGeneratiorApp", user_id="test_user", session_id=session_id
    )

    query_content = types.Content(role="user", parts=[types.Part(text=query)])
    events = []

    # STEP 1: Send initial request to the Agent. If num_containers > 5, the Agent returns the special `adk_request_confirmation` event
    try:
        async for event in generation_runner.run_async(
            user_id="test_user",
            session_id=session_id,
            new_message=query_content
        ):
            events.append(event)

        # STEP 2: Loop through all the events generated and check if `adk_request_confirmation` is present.
        approval_info = check_for_approval(events)

        # STEP 3: If the event is present, it's a large order - HANDLE APPROVAL WORKFLOW
        if approval_info:
            print(f"⏸️  Pausing for approval...")
            print(f"🤔 Human Decision: {'APPROVE ✅' if auto_approve else 'REJECT ❌'}\n")

            # PATH A: Resume the agent by calling run_async() again with the approval decision
            async for event in generation_runner.run_async(
                user_id="test_user",
                session_id=session_id,
                new_message=create_approval_response(
                    approval_info, auto_approve
                ),  # Send human decision here
                invocation_id=approval_info[
                    "invocation_id"
                ],  # Critical: same invocation_id tells ADK to RESUME
            ):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            print(f"Agent > {part.text}")

        else:
            # PATH B: If the `adk_request_confirmation` is not present - no approval needed - order completed immediately.
            print_agent_response(events)

        print(f"{'='*20}\n")
    finally:
        await generation_runner.close()


# asyncio.run(image_gen_workflow("generate random 1 image"))
# asyncio.run(image_gen_workflow("generate random 4 image",True))
asyncio.run(image_gen_workflow("generate random 4 image",False))
