from google.adk.tools.tool_context import ToolContext
from typing import Dict,Any

class AgentSessionState:
    def save_info(tool_context:ToolContext,info:dict)->Dict[str,Any]:
        # Write to session state
        for key,value in info.items():
            tool_context.state[key] = value
        return {"status":"success"}

    def retrieve_info(tool_context,status:bool=True)->Dict[str,Any]:
        return {
            "status":"success" if status else "failed",
        }


