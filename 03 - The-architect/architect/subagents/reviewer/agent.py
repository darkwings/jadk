"""
Architecture Reviewer Agent

This agent reviews the architecture design provided by the initial architecture agent.
"""

from google.adk.agents.llm_agent import LlmAgent

# Constants
GEMINI_MODEL = "gemini-2.0-flash"

architecture_reviewer_agent = LlmAgent(
    name="architecture_reviewer_agent",
    model=GEMINI_MODEL,
    description="Software architecture reviewer agent",
    instruction="""
    You are an architecture reviewer agent. 
    
    Your task is to review the architecture design provided by the initial architecture agent.

    Analyze the design for completeness, scalability, maintainability, and adherence to best practices.
    Identify any potential issues or areas for improvement, and provide constructive feedback.

    Provide feedback on the design, including any potential issues or improvements.

    ## ARCHITECTURE TO REVIEW
    {architecture_design}
    """,
    output_key="review_feedback"
)