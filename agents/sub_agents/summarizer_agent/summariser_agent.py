"""Summarizer agent configuration.

This module defines the summarizer agent, which is responsible for aggregating
the risk reports from the fire and construction risk agents into a single,
cohesive, and user-friendly summary.
"""

# Create a summary agent to gather and format results
import dotenv
import google.adk.models.lite_llm
import os
from google.adk.agents import LlmAgent

import utils.vra_util
from utils.prompt_service import PromptService

dotenv.load_dotenv()

ollama_llm = google.adk.models.lite_llm.LiteLlm(
    model=os.getenv("LLM_MODEL"),
)

summary_agent = LlmAgent(
    model=ollama_llm,
    name="RiskSummaryAgent",
    instruction=PromptService.get_latest_prompt("risk_summary_agent_instruction", app_name=os.getenv("APP_NAME", "Video_Risk_Assessment"), region=os.getenv("REGION", "us-central1")),
    before_agent_callback=[utils.vra_util.logger_before_agent_callback],
    after_agent_callback=[utils.vra_util.logger_after_agent_callback],
)
