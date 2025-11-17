from google.adk.agents import SequentialAgent
from ParallelAgents import parallel_research_team
from AggregatorAgent import aggregator_agent


root_agent = SequentialAgent(
    name='ResearchSystem',
    sub_agents = [parallel_research_team,aggregator_agent]
)
