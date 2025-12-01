import logging
from google.adk.agents.base_agent import BaseAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.plugins.base_plugin import BasePlugin

class CountInversePlugin(BasePlugin):
    def __init__(self)->None:
        super().__init__(name='count_invocation')
        self.agent_count:int = 0;
        self.tool_count:int = 0;
        self.llm_request_count:int = 0;
    # Callback-1: Runs before an Agent Calls.
    async def before_agent_callback(self,*,agent:BaseAgent,callback_context:CallbackContext)->None:
        self.agent_count +=1;
        logging.info(f"[plugin] Agent Run Count: {self.agent_count}")
    async def before_model_callback(self,*,callback_context:CallbackContext,
                                    llm_request:LlmRequest)->None:
        self.llm_request += 1;
        logging.info("[plugin] LLM Request Count: {self.llm_request}")

