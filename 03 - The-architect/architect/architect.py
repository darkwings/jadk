# Gemini LLM agent and supporting services from Google’s ADK:
from google.adk.agents.llm_agent import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner
from google.adk.agents import LoopAgent, SequentialAgent

# Gemini types for wrapping messages
from google.genai import types

import logging
from dotenv import load_dotenv   

from .subagents.initial.agent import initial_architecture_agent
from .subagents.reviewer.agent import architecture_reviewer_agent
from .subagents.refiner.agent import architecture_refiner


load_dotenv()

# Create a module-level logger using this file’s name
logger = logging.getLogger(__name__)

class ArchitectAgent:

    # Declare which content types this agent accepts by default
    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]   
    APP_NAME = "architectin'"

    def __init__(self):
        """
        🏗️ Constructor: build the internal orchestrator LLM, runner, discovery client.
        """
        self.agent = self._build_agent()        

        self.runner = Runner(
            app_name=self.APP_NAME,
            agent=self.agent,
            artifact_service=InMemoryArtifactService(),       # file blobs, unused here
            session_service=InMemorySessionService(),         # in-memory sessions
            memory_service=InMemoryMemoryService(),           # conversation memory
        )      


    def _build_agent(self) -> SequentialAgent:
        refinement_loop = LoopAgent(
            name="PostRefinementLoop",
            max_iterations=5,
            sub_agents=[
                architecture_reviewer_agent,
                architecture_refiner,
            ],
            description="Iteratively reviews and refines a LinkedIn post until quality requirements are met",
        )
        ag = SequentialAgent(
            name="SoftwareArchitecturePipeline",
            sub_agents=[
                initial_architecture_agent,  # Step 1: Generate initial post
                refinement_loop,             # Step 2: Review and refine in a loop
            ],
            description="Generates and refines a LinkedIn post through an iterative review process",
        )
        return ag

    def invoke(self, query: str, session_id: str, user_id: str) -> str:
        """
        🔄 Public: send a user query through the orchestrator LLM pipeline,
        ensuring session reuse or creation, and return the final text reply.
        """
        # 1) Try to fetch an existing session
        session = self.runner.session_service.get_session(
            app_name=self.APP_NAME,
            user_id=user_id,
            session_id=session_id,
        )

        # 2) If not found, create a new session with empty state
        if session is None:
            session = self.runner.session_service.create_session(
                app_name=self.APP_NAME,
                user_id=user_id,
                session_id=session_id,
                state={},  # you could prefill memory here if desired
            )

        # 3) Wrap the user’s text in a Gemini Content object
        content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=query)]
        )

        # 4) Run the orchestrator and collect all response “events”
        events = list(self.runner.run(
            user_id=user_id,
            session_id=session.id,
            new_message=content
        ))

        # 5) If no events or no content parts, bail out with empty string
        if not events or not events[-1].content.parts:
            return ""

        # 6) Otherwise, join all text parts of the final event and return
        return "\n".join(p.text for p in events[-1].content.parts if p.text)