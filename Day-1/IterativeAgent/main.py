from google.adk.runners import InMemoryRunner
from RootAgent import root_agent
import asyncio


runner = InMemoryRunner(agent=root_agent)

async def main():
    response = await runner.run_debug(
        "Write a short story about a lighthouse keeper who discovers a mysterious, glowing map"
    )


if __name__=="__main__":
    asyncio.run(main())


