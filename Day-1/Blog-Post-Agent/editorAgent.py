from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types
from config import Config

editor_agent = Agent(
    name="EditorAgent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_config=Config.retry_config,
        api_key=Config.api_key
    ),
    instruction="""Edit this draft: {blog_draft}
    Your task is to polish the text by fixing any grammatical errors, improving the flow and sentence structure, and enhancing overall clarity.""",
    output_key="final_blog"
)
