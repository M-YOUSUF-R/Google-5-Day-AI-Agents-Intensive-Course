# research agent; it's job is to use google_search tool and present findings
from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search,AgentTool,FunctionTool
from cod2_1 import retry_config

import asyncio


research_agent = Agent(
    name="ResearchAgent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options = retry_config
    ),
    instruction="""You are a specialized research agent. Your only job is to use the
    google_search tool to find 2-3 pieces of relevant information on the given topic and present the findings with citations.""",
    tools=[google_search],
    output_key="research_findings"
)

summarizer_agent = Agent(
    name="SummerizeAgent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    instruction="""Read the provided research findings: {research_findings}
    Create a concise summary as a bulleted list with 3-5 key points.""",
    output_key="final_summary"
)

root_agent = Agent(
    name="ResearchCoordinator",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options = retry_config
    ),
    instruction="""You are a research coordinator. Your goal is to answer the user's query by orchestrating a workflow.
    1. First, you MUST call the `ResearchAgent` tool to find relevant information on the topic provided by the user.
    2. Next, after receiving the research findings, you MUST call the `SummarizerAgent` tool to create a concise summary.
    3. Finally, present the final summary clearly to the user as your response.""",
    tools=[AgentTool(research_agent), AgentTool(summarizer_agent)],
)

runner = InMemoryRunner(agent=root_agent)

async def main():
    response = await runner.run_debug(
        "What are the latest advancements in quantum computing and what do they mean for AI?"
    )

asyncio.run(main())

