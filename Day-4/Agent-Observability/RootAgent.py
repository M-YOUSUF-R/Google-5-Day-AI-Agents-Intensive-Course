from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.google_search_tool import google_search

from config import Config
from helperFunc import count_papers
from AgentPlugins import CountInversePlugin

google_search_agent = LlmAgent(
    name="GoogleSearchAgent",
    model=Gemini(
        model='gemini-2.5-flash',
        retry_options=Config.retry_config,
        api_key=Config.api_key
    ),
    description="search for information using google search",
    instruction="""Use the google_search tool to find information on the given topic.
    Return the raw search results.
    If the user asks for a list of papers, 
    then give them the list of research papers you found and not the summary.""",
    tools=[google_search],

)

root_agent = LlmAgent(
    name="ResearchPaperFinderAgent",
    model=Gemini(
        model='gemini-2.5-flash',
        retry_options=Config.retry_config,
        api_key=Config.api_key,
    ),
    instruction="""Your task is to find research papers and count them. 

    You MUST ALWAYS follow these steps:
    1) Find research papers on the user provided topic using the 'google_search_agent'. 
    2) Then, pass the papers to 'count_papers' tool to count the number of papers returned.
    3) Return both the list of research papers and the total number of papers.
    """,
    tools=[AgentTool(agent=google_search_agent),count_papers]
)


