"""
Architecture Refiner Agent

This agent refine the architecture design provided by the initial architecture agent
and reviewed by the refiner.
"""

from google.adk.agents.llm_agent import LlmAgent

# Constants
GEMINI_MODEL = "gemini-2.0-flash"

architecture_refiner = LlmAgent(
    name="ArchitectureRefinerAgent",
    model=GEMINI_MODEL,
    instruction="""You are a LinkedIn Post Refiner.

    Your task is to refine the software architecture based on the given feedbacl.
    
    ## INPUTS
    **Current Post:**
    {architecture_design}
    
    **Review Feedback:**
    {review_feedback}
    
    ## TASK
    Refine the architecture design based on the review feedback provided.
    Ensure that the refined design addresses all the feedback points and improves the overall quality of the architecture.
    Focus on enhancing the design's clarity, completeness, and adherence to best practices.
    Provide a clear and concise refined architecture design that incorporates the feedback.

    ## OUTPUT INSTRUCTIONS
    - Output ONLY the refined post content in markdown format.    
    """,
    description="Refines the proposed software architecture to improve quality",
    output_key="architecture_design",
)