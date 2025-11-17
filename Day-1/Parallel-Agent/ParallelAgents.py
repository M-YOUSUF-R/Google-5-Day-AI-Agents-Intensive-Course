from google.adk.agents import ParallelAgent

from techResearcher import tech_researcher
from financeResearcher import finance_researcher
from healthResearcher import health_researcher

from config import Config


parallel_research_team = ParallelAgent(
    name="ParallelResearchTeam",
    sub_agents = [tech_researcher,health_researcher,finance_researcher],
)
