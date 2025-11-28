"""Parallel planner agent configuration.

This module defines the parallel planner agent, which orchestrates the execution
of risk analysis sub-agents (fire and construction) in parallel. It handles
the distribution of the video assessment task.
"""

# Create a summary agent to gather and format results
import google.adk.agents

import agents.sub_agents.construction_risk_analyser.construction_risk_agent
import agents.sub_agents.fire_risk_analyser.fire_risk_agent
from utils.vra_util import logger_before_agent_callback, logger_after_agent_callback
from utils.prompt_service import PromptService
import os

parallel_planner = google.adk.agents.ParallelAgent(
    name="parallel_planner",
    description=PromptService.get_latest_prompt("parallel_planner_description", app_name=os.getenv("APP_NAME", "Video_Risk_Assessment"), region=os.getenv("REGION", "us-central1")),
    sub_agents=[agents.sub_agents.fire_risk_analyser.fire_risk_agent.fire_risk_agent,
                agents.sub_agents.construction_risk_analyser.construction_risk_agent.construction_risk_agent],
    before_agent_callback=[logger_before_agent_callback],
    after_agent_callback=[logger_after_agent_callback],
)
