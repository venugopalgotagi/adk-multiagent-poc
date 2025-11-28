import dotenv

import agents.sub_agents.summarizer_agent.summariser_agent
import utils.vra_util

dotenv.load_dotenv()

# Define the root agent as a sequence
from google.adk.agents import SequentialAgent

root_agent = SequentialAgent(
    name="root_agent",
    sub_agents=[
        agents.sub_agents.parallel_planner.parallel_planner_agent.parallel_planner,
        agents.sub_agents.summarizer_agent.summariser_agent.summary_agent
    ],
    before_agent_callback=[utils.vra_util.logger_before_agent_callback],
    after_agent_callback=[utils.vra_util.logger_after_agent_callback],
)
