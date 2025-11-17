from google.adk.runners import InMemoryRunner
from rootAgent import root_agent
import asyncio

runner = InMemoryRunner(agent=root_agent)
async def main():
    response = await runner.run_debug(
        "Write a blog post about the benefits of multi-agent systems for software developers"
    )

if __name__ == '__main__':
    asyncio.run(main())
