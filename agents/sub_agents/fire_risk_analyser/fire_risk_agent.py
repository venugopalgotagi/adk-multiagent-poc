import google.adk
from google.adk.agents.parallel_agent import ParallelAgent
from utils.vra_util import logger_before_agent_callback,logger_after_agent_callback
import os
from google.adk.agents.llm_agent import LlmAgent

from google.adk.models.lite_llm import LiteLlm

ollama_llm = LiteLlm(
    model=os.getenv("LLM_MODEL"),
)

fire_risk_agent = LlmAgent(
    model=ollama_llm,
    name="fire_risk_agent",
    instruction="Role & Constraint DefinitionRole: Act as a certified Fire Safety Officer and Risk Assessor.Constraint (Anti-Hallucination): "
                "You MUST NOT infer or invent hazards. Your analysis is STRICTLY LIMITED to the information provided (e.g., transcript, "
                "object list, scene description). If a risk is only suspected but not confirmed by the data, classify it as "
                "'Potential Unconfirmed Risk' in the list.Focus: Your sole task is to identify and catalogue elements related to the"
                " Fire Triangle (Fuel, Heat/Ignition, Oxygen/Oxidizer). Do not discuss non-fire related hazards "
                "(e.g., tripping, structural).2. 🔍 Analysis and Prioritization TasksScan the provided video data "
                "(transcript, objects, scenes) "
                "for the following:Ignition Sources (Heat): Open flames, sparks, hot surfaces, smoking, damaged electrical wiring,"
                " high-temperature equipment.Fuel Sources: Flammable liquids/gases, highly combustible materials (e.g., "
                "large amounts of paper, dry vegetation, solvents, gasoline cans, propane tanks).Environmental Factors: "
                "Blocked exits, lack of visible fire extinguishers/suppression systems, or proximity between Fuel and"
                " Ignition sources.3. 📝 Mandatory Output FormatProvide a detailed analysis using the following table structure."
                " For the Confidence Score, use: High (clearly visible/mentioned), Medium (partially obscured or mentioned in passing),"
                " or Low (inferred or potential).IDTime/Scene DescriptionIdentified Fire HazardType (Ignition/Fuel/Environment)"
                "Confidence ScoreRecommended Action1[Specific time or scene][Detailed description, e.g., Exposed wiring near cardboard"
                " boxes][Select one][High/Medium/Low][Brief, practical step, e.g., "
                "Insulate wire/Remove boxes]2...............Summary and Critical FindingsOverall Risk Level:"
                " (State: Immediate/High/Moderate/Low).Top Priority Hazard: Identify the single most dangerous item or combination found.",
    before_agent_callback=[logger_before_agent_callback],
    after_agent_callback=[logger_after_agent_callback],
    output_key="fire_risk_report"
)