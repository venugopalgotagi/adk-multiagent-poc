import google.adk
import google.adk.models.lite_llm
from google.adk.agents.parallel_agent import ParallelAgent
import os
import agents.sub_agents.construction_risk_analyser.construction_risk_agent
import agents.sub_agents.fire_risk_analyser.fire_risk_agent
import agents.sub_agents.parallel_planner.parallel_planner_agent
import agents.sub_agents.summarizer_agent.summariser_agent
import utils.vra_util
import dotenv

dotenv.load_dotenv()



# Define the root agent as a sequence
from google.adk.agents import SequentialAgent

root_agent = SequentialAgent(
    name="root_agent",
    sub_agents=[
        agents.sub_agents.parallel_planner.parallel_planner_agent.parallel_planner,  # Executes FlightAgent and HotelAgent
        agents.sub_agents.summarizer_agent.summariser_agent.summary_agent  # Executes after planning is done
    ],
    before_agent_callback=[utils.vra_util.logger_before_agent_callback],
    after_agent_callback=[utils.vra_util.logger_after_agent_callback],
)