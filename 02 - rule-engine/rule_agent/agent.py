from .tools.tools import get_value
from google.adk.agents import Agent

root_agent = Agent(
    name="rule_agent",
    model="gemini-2.0-flash",
    description="Manager agent",
    instruction="""
    You are a rule engine agent. You will receive a list of sources and you have to 
    retrieve their current values.

    Based on the values you retrieve, you will have to choose the source with the highest value
    and, based on that value, you must return the action to take.
    The action can be either 'proceed' or 'stop'.
    
    The action will be 'proceed' only if the value is greater than 500, otherwise the action will be stop.
    You should return only a json like this
    {
        "action": "proceed" or "stop",
        "source_id": source_id,
        "value": value
    }
    
    You have access to the following tools to get the value of each source:
    - get_value    
    """,    
    tools=[get_value],
    output_key="outcome"
)