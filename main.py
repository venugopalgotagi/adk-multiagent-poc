"""FastAPI application for Video Risk Assessment.

This module defines the main entry point for the Video Risk Assessment (VRA) service.
It sets up the FastAPI application, initializes the ADK runner with necessary services
(database, memory, artifacts), and defines the API endpoints.
"""

import fastapi
import google.adk.artifacts
import google.adk.memory
import google.adk.sessions.database_session_service
import google.adk.sessions.sqlite_session_service
import google.genai.types
import typing
import uuid
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File

from vra_app.app import app  # import code from agent.py

load_dotenv()  # load API keys and settings
# Set a Runner using the imported application object

rest_api_app = FastAPI()

session_service = google.adk.sessions.database_session_service.DatabaseSessionService(
    db_url="postgresql+asyncpg://postgres:postgres@localhost:5432/postgres")
memory_service = google.adk.memory.InMemoryMemoryService()
runner = google.adk.Runner(
    app=app,
    session_service=session_service,
    memory_service=memory_service,
    artifact_service=google.adk.artifacts.FileArtifactService(root_dir="artifacts"),
)


@rest_api_app.post("/video_risk_assessment")
async def video_risk_assessment(user_id: str, risk_type: str, file: fastapi.UploadFile = File(...)):
    """Performs video risk assessment on an uploaded video file.

    Args:
        user_id: The unique identifier of the user requesting the assessment.
        risk_type: The type of risk to analyze (e.g., 'fire', 'construction').
        file: The uploaded video file to be analyzed.

    Returns:
        The final response from the RiskSummaryAgent containing the assessment results.
    """
    try:  # run_debug() requires ADK Python 1.18 or higher:
        session = await session_service.create_session(app_name=app.name,
                                                       user_id=user_id,
                                                       state={
                                                           "mime_type": file.content_type,
                                                           "risk_type": risk_type,
                                                       },
                                                       session_id=str(uuid.uuid4()))
        response: typing.AsyncGenerator[google.adk.events.Event] = runner.run_async(user_id=session.user_id,
                                                                                    session_id=session.id,
                                                                                    new_message=google.genai.types.Content(
                                                                                        role="user",
                                                                                        parts=[
                                                                                            google.genai.types.Part(
                                                                                                text="Analyse content for risks and hazards",
                                                                                                inline_data=google.genai.types.Blob(
                                                                                                    mime_type=file.content_type,
                                                                                                    data=await get_payload(
                                                                                                        file)
                                                                                                )
                                                                                            )
                                                                                        ])
                                                                                    )

        # 2. Consume the synchronous generator stream safely in a threadpool
        # This loop ensures all sequential steps are completed and state is saved.
        async for event in response:
            if event.author == 'RiskSummaryAgent' and event.is_final_response():
                print(f'final response {event.content.parts}')
                return event.content.parts


    except Exception as e:
        print(f"An error occurred during agent execution: {e}")


async def get_payload(file: UploadFile) -> bytes:
    """Reads the content of an uploaded file.

    Args:
        file: The uploaded file object.

    Returns:
        The content of the file as bytes.
    """
    video_stream = await file.read()
    return video_stream
