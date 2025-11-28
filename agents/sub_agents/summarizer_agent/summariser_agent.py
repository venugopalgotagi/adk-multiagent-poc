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

dotenv.load_dotenv()

ollama_llm = google.adk.models.lite_llm.LiteLlm(
    model=os.getenv("LLM_MODEL"),
)

summary_agent = LlmAgent(
    model=ollama_llm,
    name="RiskSummaryAgent",
    instruction="""
    You are a final report generator. Summarize the fire_risks  
    (from state['fire_risk_report']) and the construction risks  
    (from state['construction_risk_report']) into a single, cohesive, and friendly 
    response for the user. Do not include technical keys or formats.
    """,
    before_agent_callback=[utils.vra_util.logger_before_agent_callback],
    after_agent_callback=[utils.vra_util.logger_after_agent_callback],
)
