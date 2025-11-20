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

LARGE_ORDER_THRESHOLD =5

def place_shipping_order(
    num_containers:int,
    destination:str,
    tool_context:ToolContext
)-> dict:
    if num_containers <= LARGE_ORDER_THRESHOLD:
        return {
            "status":"approved",
            "order_id":f"ORD-{num_containers}-AUTO",
            "destination":destination,
            "message":f"Order approved: {num_containers} containers to {destination}",
        }

    if not tool_context.tool_confirmation:
        tool_context.request_confirmation(
            hint=f"Large order: {num_containers} containers to {destination}.\nDo you want to approve? ",
            payload={"num_containers":num_containers,"destination":destination},
        )

        return {  # This is sent to the Agent
            "status": "pending",
            "message": f"Order for {num_containers} containers requires approval",
        }

    if tool_context.tool_confirmation.confirmed:
        return {
            "status": "approved",
            "order_id": f"ORD-{num_containers}-HUMAN",
            "num_containers": num_containers,
            "destination": destination,
            "message": f"Order approved: {num_containers} containers to {destination}",
        }
    else:
        return {
            "status": "rejected",
            "message": f"Order rejected: {num_containers} containers to {destination}",
        }

shipping_agent = LlmAgent(
    name="ShippingAgent",
    model=Gemini(
        model='gemini-2.5-flash',
        retry_options=Config.retry_config,
        api_key = Config.api_key
    ),
    instruction="""You are a shipping coordinator assistant.

    When users request to ship containers:
    1. Use the place_shipping_order tool with the number of containers and destination
    2. If the order status is 'pending', inform the user that approval is required
    3. After receiving the final result, provide a clear summary including:
        - Order status (approved/rejected)
        - Order ID (if available)
        - Number of containers and destination
    4. Keep responses concise but informative
    """,
    tools=[FunctionTool(func=place_shipping_order)]
)

shipping_app = App(
    name="shipping_coordinator",
    root_agent=shipping_agent,
    resumability_config=ResumabilityConfig(is_resumable=True)
)
session_service = InMemorySessionService()
shipping_runner = Runner(
    app=shipping_app,
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

async def run_shipping_workflow(query: str, auto_approve: bool = True):
    """Runs a shipping workflow with approval handling.

    Args:
        query: User's shipping request
        auto_approve: Whether to auto-approve large orders (simulates human decision)
    """

    print(f"\n{'='*20}")
    print(f"User > {query}\n")

    # Generate unique session ID
    session_id = f"order_{uuid.uuid4().hex[:8]}"

    # Create session
    await session_service.create_session(
        app_name="shipping_coordinator", user_id="test_user", session_id=session_id
    )

    query_content = types.Content(role="user", parts=[types.Part(text=query)])
    events = []

    # STEP 1: Send initial request to the Agent. If num_containers > 5, the Agent returns the special `adk_request_confirmation` event
    async for event in shipping_runner.run_async(
        user_id="test_user", session_id=session_id, new_message=query_content
    ):
        events.append(event)

    # STEP 2: Loop through all the events generated and check if `adk_request_confirmation` is present.
    approval_info = check_for_approval(events)

    # STEP 3: If the event is present, it's a large order - HANDLE APPROVAL WORKFLOW
    if approval_info:
        print(f"⏸️  Pausing for approval...")
        print(f"🤔 Human Decision: {'APPROVE ✅' if auto_approve else 'REJECT ❌'}\n")

        # PATH A: Resume the agent by calling run_async() again with the approval decision
        async for event in shipping_runner.run_async(
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

"""
async def main():
    demo_inputs:list[dict] = [
        {"query":"Ship 3 containers to Singapore"},
        {"query":"Ship 10 containers to Rotterdam","approve":True},
        {"query":"Ship 8 containers to Los Angeles","approve":False}
    ]

    for i in range(len(demo_inputs)):
        await run_shipping_workflow(
                demo_inputs[i].get("query",""),
                demo_inputs[i].get("approve",True)
        )

asyncio.run(main())
"""
"or you can run it like this:"
"""
async def main():
    tasks = [
        run_shipping_workflow("Ship 3 containers to Singapore"),
        run_shipping_workflow("Ship 10 containers to Rotterdam", True),
        run_shipping_workflow("Ship 8 containers to Los Angeles", False),
    ]

    await asyncio.run(*tasks)

asyncio.run(main())
"""

# asyncio.run(run_shipping_workflow("Ship 3 containers to Singapore"))

# asyncio.run(run_shipping_workflow("Ship 10 containers to Rotterdam",auto_approve=True))

# asyncio.run(run_shipping_workflow("Ship 8 containers to Los Angeles",auto_approve=False))

asyncio.gather(
    run_shipping_workflow("Ship 3 containers to Singapore"),
    run_shipping_workflow("Ship 10 containers to Rotterdam",auto_approve=True),
    run_shipping_workflow("Ship 8 containers to Los Angeles",auto_approve=False)
)
