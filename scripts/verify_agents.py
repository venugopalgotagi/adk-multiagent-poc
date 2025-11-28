"""Script to verify that agents can fetch prompts from the database."""

import sys
import os

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

try:
    print("Importing agents...")
    from agents.sub_agents.construction_risk_analyser.construction_risk_agent import construction_risk_agent
    from agents.sub_agents.fire_risk_analyser.fire_risk_agent import fire_risk_agent
    from agents.sub_agents.summarizer_agent.summariser_agent import summary_agent
    from agents.sub_agents.parallel_planner.parallel_planner_agent import parallel_planner

    print("Verifying construction_risk_agent instruction...")
    if not construction_risk_agent.instruction or "Construction Safety Manager" not in construction_risk_agent.instruction:
        print("FAILED: construction_risk_agent instruction not loaded correctly.")
    else:
        print("PASSED: construction_risk_agent instruction loaded.")

    print("Verifying fire_risk_agent instruction...")
    if not fire_risk_agent.instruction or "Fire Safety Officer" not in fire_risk_agent.instruction:
        print("FAILED: fire_risk_agent instruction not loaded correctly.")
    else:
        print("PASSED: fire_risk_agent instruction loaded.")

    print("Verifying summary_agent instruction...")
    if not summary_agent.instruction or "final report generator" not in summary_agent.instruction:
        print("FAILED: summary_agent instruction not loaded correctly.")
    else:
        print("PASSED: summary_agent instruction loaded.")

    print("Verifying parallel_planner description...")
    if not parallel_planner.description or "parallel_planner who handles" not in parallel_planner.description:
        print("FAILED: parallel_planner description not loaded correctly.")
    else:
        print("PASSED: parallel_planner description loaded.")

except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
