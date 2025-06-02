from google.adk.agents import Agent
from google.adk.tools import google_search

web_searcher = Agent(
    name="web_searcher",
    model="gemini-2.0-flash",
    description="Technical articles analyst agent",
    instruction="""
    You are a helpful assistant that can analyze technical articles about software architecture
    available on the web.

    When asked about, you should use the google_search tool to search for technical articles that
    are useful to solve a problem.    
    """,
    tools=[google_search],
)