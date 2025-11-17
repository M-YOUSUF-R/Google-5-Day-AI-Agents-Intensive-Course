from google.adk.agents import LoopAgent
from CriticAgent import critic_agent
from RefinerAgent import refine_agent

story_refined_loop = LoopAgent(
    name="StoryRefinedLoop",
    sub_agents=[critic_agent,refine_agent],
    max_iterations=2, # prevents infinite loop

)

