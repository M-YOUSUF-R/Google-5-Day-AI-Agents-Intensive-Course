from google.adk.agents import SequentialAgent
from WriterAgent import writing_agent
from LoopAgent import story_refined_loop

root_agent = SequentialAgent(
    name="StoryPipeline",
    sub_agents=[writing_agent,story_refined_loop],
)
