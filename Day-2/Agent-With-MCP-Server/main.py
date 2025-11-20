import asyncio
from google.adk.runners import InMemoryRunner
from RootAgent import root_agent
import base64

runner = InMemoryRunner(
    agent=root_agent
)

async def main():
    response = await runner.run_debug(
        "Provide a sample tiny image",
        verbose=True
    )
    await runner.close()


if __name__=='__main__':
    asyncio.run(main=main())

