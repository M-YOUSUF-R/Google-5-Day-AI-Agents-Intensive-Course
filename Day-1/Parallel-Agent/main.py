from google.adk.runners import InMemoryRunner
from rootAgent import root_agent
import asyncio

runner = InMemoryRunner(agent=root_agent)

async def main():
    response = await runner.run_debug(
        "Run the daily executive briefing on Tech, Health, and Finance"
    )

if __name__ == '__main__':
    asyncio.run(main())
