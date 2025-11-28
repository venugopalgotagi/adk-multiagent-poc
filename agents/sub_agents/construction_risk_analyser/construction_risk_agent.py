"""Construction risk analysis agent.

This module defines an LLM-based agent responsible for analyzing video content
to identify construction-related risks and hazards. It uses a specific persona
and set of constraints to ensure accurate and relevant safety assessments.
"""

import os
from google.adk.agents.llm_agent import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from utils.vra_util import logger_before_agent_callback, logger_after_agent_callback
from utils.prompt_service import PromptService

ollama_llm = LiteLlm(
    model=os.getenv("LLM_MODEL"),
)

construction_risk_agent = LlmAgent(
    model=ollama_llm,
    name="construction_risk_agent",
    instruction=PromptService.get_latest_prompt("construction_risk_agent_instruction", app_name=os.getenv("APP_NAME", "Video_Risk_Assessment"), region=os.getenv("REGION", "us-central1")),
    before_agent_callback=[logger_before_agent_callback],
    after_agent_callback=[logger_after_agent_callback],
    output_key="construction_risk_report"
)
