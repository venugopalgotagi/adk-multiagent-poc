# Create a summary agent to gather and format results
import google.adk.agents
from google.adk.agents import LlmAgent

import agents.sub_agents.construction_risk_analyser.construction_risk_agent
import agents.sub_agents.fire_risk_analyser.fire_risk_agent
from utils.vra_util import logger_before_agent_callback, logger_after_agent_callback

parallel_planner = google.adk.agents.ParallelAgent(
    name="parallel_planner",
    description="parallel_planner who handles overall video risk assessment."
                "Forwards request to subagents"
                "Importantly do not forward request to subagents if the user query is a greeting message",
    sub_agents=[agents.sub_agents.fire_risk_analyser.fire_risk_agent.fire_risk_agent,
                agents.sub_agents.construction_risk_analyser.construction_risk_agent.construction_risk_agent],
    before_agent_callback=[logger_before_agent_callback],
    after_agent_callback=[logger_after_agent_callback],
)