from google.adk.runners import InMemoryRunner
import asyncio
# from RootAgent import root_agent
from RootAgent import root_agent_with_calcuation
from helper import show_python_code_and_result

"""
runner = InMemoryRunner(
    agent=root_agent
)
"""
runner = InMemoryRunner(
    agent=root_agent_with_calcuation
)
async def main():
    response = await runner.run_debug(
        # "I want to convert 500 US Dollars to Euros using my Platinum Credit Card. How much will I receive?"
        "Convert 1,250 USD to INR using a Bank Transfer. Show me the precise calculation."
    )
    # let's see the python code also
    show_python_code_and_result(response=response)


if __name__=='__main__':
    asyncio.run(main=main())
