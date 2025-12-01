from google.adk.runners import InMemoryRunner
from google.adk.plugins.logging_plugin import (
        LoggingPlugin
)

from RootAgent import root_agent

import asyncio

runner = InMemoryRunner(agent=root_agent)
plugin_runner = InMemoryRunner(agent=root_agent,plugins=[LoggingPlugin()])

async def main():
    response = await plugin_runner.run_debug(
        "Find latest quantum computing papers"
    )


if __name__=='__main__':
    asyncio.run(main())
