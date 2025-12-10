from google.adk.agents import Agent,SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.genai import types
from google.adk.tools import AgentTool, FunctionTool,google_search

retry_config=types.HttpRetryOptions(
    attempts=5,  
    exp_base = 7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

#-----Research Agent-----#
research_agent=Agent(
    name = "ResearchAgent",
    model = Gemini(
        model = "gemini-2.5-flash-lite",
        retry_options = retry_config
    ),
    instruction="""You are a specialized research agent. Your only job is to use the google_search tool to find 2-3 pieces of relevant information on the given topic and present the findings with citations.""",
    tools=[google_search],
    output_key="research_findings", 
)


#------Summarizer Agent------#
summarizer_agent = Agent(
    name="SummarizerAgent",
    model = Gemini(
        model = "gemini-2.5-flash-lite",
        retry_options = retry_config
    ),
    instruction = """Read the provided research findings : {research_findings}. Create a Concise summary as a bulleted list of not more than 5 points.""",
    output_key = "final_summary",
)
print("Summarizer Agent created")




#------Root Agent------#
root_agent = Agent(
    name = "Research_Coordinator",
    model = Gemini(
        model = "gemini-2.5-flash-lite",
        retry_options = retry_config,
    ),
    instruction = """You are a research coordinator. Your goeal is to answer the user's query by orchestrating a workflow.
    1. First, you MUST call 'ResearchAgent' tool to find relevant information about the topic provided by the User.
    2. Next, after receiving the research findings, you MUST call the 'SummarizerAgent' tool to create a concise summary
    3. Finally, present the summary clearly to the user as your response.""",
    tools = [AgentTool(research_agent), AgentTool(summarizer_agent)],
)
print("Root Agent Defined")



