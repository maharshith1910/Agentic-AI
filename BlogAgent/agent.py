from google.adk.agents import Agent,SequentialAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool,FunctionTool,google_search

retry_config =types.HttpRetryOptions(
    initial_delay = 1,
    attempts = 5,
    exp_base = 7,
    http_status_codes = [429,500,503,503],
)

#------Outline Agent------#
outline_agent = Agent(
    name = "OutlineAgent",
    model = Gemini(
        model = "gemini-2.5-flash-lite",
        retry_options = retry_config,
    ),
    instruction = """Create a blog outline for the given topic with : 
    1. A Catchy Headline,
    2. An Introduction Hook line
    3. 3-5 main sections with 2-3 points each.
    4. Concluding Thought""",
    output_key = "blog_outline",
)



#------Writer Agent------#
writer_agent = Agent(
    name = "WriterAgent",
    model = Gemini(
        model = "gemini-2.5-flash-lite",
        retry_options = retry_config,
    ),
    instruction = """Follow the outline strictly : {blog_outline}
    Write a brief, 200 to 300 words blog post with an engaging and informative tone.""",
    output_key = "blog_draft",
)



#------Editor Agent------#
editor_agent = Agent(
    name = "EditorAgent",
    model = Gemini(
        model = "gemini-2.5-flash-lite",
        retry_options = retry_config,
    ),
    instruction = """"Edit this draft : {blog_draft}
    Your task is to polish the text by fixing any grammatical errors, improving the flow and sentence structure, and enhance the overall clarity""",
    output_key = "final_blog",
)





#------Root Agent------#
root_agent = SequentialAgent(
    name="BlogPipeline",
    sub_agents=[outline_agent, writer_agent, editor_agent],
)
