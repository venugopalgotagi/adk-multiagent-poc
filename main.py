"""FastAPI application for Video Risk Assessment.

This module defines the main entry point for the Video Risk Assessment (VRA) service.
It sets up the FastAPI application, initializes the ADK runner with necessary services
(database, memory, artifacts), and defines the API endpoints.
"""
import os
import fastapi
import google.adk.artifacts
import google.adk.memory
import google.adk.sessions.database_session_service
import google.adk.sessions.sqlite_session_service
import google.genai.types
import typing
import uuid
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List

from vra_app.app import app  # import code from agent.py
from utils.prompt_service import PromptService
from utils.models import init_db

load_dotenv()  # load API keys and settings
# Set a Runner using the imported application object

rest_api_app = FastAPI()

# Initialize database tables
init_db()

session_service = google.adk.sessions.database_session_service.DatabaseSessionService(
    db_url=os.getenv("DATABASE_URL"))
memory_service = google.adk.memory.InMemoryMemoryService()
runner = google.adk.Runner(
    app=app,
    session_service=session_service,
    memory_service=memory_service,
    artifact_service=google.adk.artifacts.FileArtifactService(root_dir="artifacts"),
)


# Pydantic Models for Prompt CRUD
class PromptCreate(BaseModel):
    """Schema for creating a new prompt."""
    name: str
    content: str
    app_name: Optional[str] = None  # Will use env variable if not provided
    region: Optional[str] = None  # Will use env variable if not provided


class PromptUpdate(BaseModel):
    """Schema for updating an existing prompt."""
    content: str


class PromptResponse(BaseModel):
    """Schema for prompt response."""
    id: int
    name: str
    app_name: str
    region: str
    version: int
    content: str
    created_at: str

    class Config:
        from_attributes = True


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
        state = {
            "mime_type": file.content_type,
            "risk_type": risk_type
        }
        session = await session_service.create_session(app_name=app.name,
                                                       user_id=user_id,
                                                       state=state,
                                                       session_id=str(uuid.uuid4()))
        response: typing.AsyncGenerator[google.adk.events.Event] = runner.run_async(user_id=session.user_id,
                                                                                    session_id=session.id,
                                                                                    state_delta=state,
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


# ==================== Prompt Management APIs ====================

@rest_api_app.post("/prompts", response_model=PromptResponse, status_code=201)
async def create_prompt(prompt: PromptCreate):
    """Create a new prompt in the database.

    Args:
        prompt: The prompt data to create.

    Returns:
        The created prompt object.

    Raises:
        HTTPException: If a prompt with the same name, app_name, and region already exists.
    """
    try:
        app_name = prompt.app_name or os.getenv("APP_NAME", "Video_Risk_Assessment")
        region = prompt.region or os.getenv("REGION", "us-central1")

        # Check if prompt already exists
        existing_prompt = PromptService.get_prompt_by_name(prompt.name, app_name, region)
        if existing_prompt:
            raise HTTPException(
                status_code=400,
                detail=f"Prompt with name '{prompt.name}', app_name '{app_name}', and region '{region}' already exists. Use PUT to update."
            )

        # Create new prompt
        PromptService.add_prompt(prompt.name, prompt.content, app_name, region)
        
        # Fetch and return the created prompt
        created_prompt = PromptService.get_prompt_by_name(prompt.name, app_name, region)
        return PromptResponse(
            id=created_prompt.id,
            name=created_prompt.name,
            app_name=created_prompt.app_name,
            region=created_prompt.region,
            version=created_prompt.version,
            content=created_prompt.content,
            created_at=str(created_prompt.created_at)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create prompt: {str(e)}")


@rest_api_app.get("/prompts", response_model=List[PromptResponse])
async def get_all_prompts(
    app_name: Optional[str] = Query(None, description="Filter by application name"),
    region: Optional[str] = Query(None, description="Filter by region")
):
    """Get all prompts, optionally filtered by app_name and/or region.

    Args:
        app_name: Optional filter for application name.
        region: Optional filter for region.

    Returns:
        List of all prompts matching the filters.
    """
    try:
        prompts = PromptService.get_all_prompts(app_name, region)
        return [
            PromptResponse(
                id=p.id,
                name=p.name,
                app_name=p.app_name,
                region=p.region,
                version=p.version,
                content=p.content,
                created_at=str(p.created_at)
            )
            for p in prompts
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch prompts: {str(e)}")


@rest_api_app.get("/prompts/{prompt_id}", response_model=PromptResponse)
async def get_prompt_by_id(prompt_id: int):
    """Get a specific prompt by its ID.

    Args:
        prompt_id: The ID of the prompt to retrieve.

    Returns:
        The prompt object.

    Raises:
        HTTPException: If the prompt is not found.
    """
    try:
        prompt = PromptService.get_prompt_by_id(prompt_id)
        if not prompt:
            raise HTTPException(status_code=404, detail=f"Prompt with ID {prompt_id} not found")
        
        return PromptResponse(
            id=prompt.id,
            name=prompt.name,
            app_name=prompt.app_name,
            region=prompt.region,
            version=prompt.version,
            content=prompt.content,
            created_at=str(prompt.created_at)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch prompt: {str(e)}")


@rest_api_app.put("/prompts/{prompt_id}", response_model=PromptResponse)
async def update_prompt(prompt_id: int, prompt_update: PromptUpdate):
    """Update an existing prompt's content.

    Args:
        prompt_id: The ID of the prompt to update.
        prompt_update: The updated content for the prompt.

    Returns:
        The updated prompt object.

    Raises:
        HTTPException: If the prompt is not found.
    """
    try:
        updated_prompt = PromptService.update_prompt(prompt_id, prompt_update.content)
        if not updated_prompt:
            raise HTTPException(status_code=404, detail=f"Prompt with ID {prompt_id} not found")
        
        return PromptResponse(
            id=updated_prompt.id,
            name=updated_prompt.name,
            app_name=updated_prompt.app_name,
            region=updated_prompt.region,
            version=updated_prompt.version,
            content=updated_prompt.content,
            created_at=str(updated_prompt.created_at)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update prompt: {str(e)}")


@rest_api_app.delete("/prompts/{prompt_id}", status_code=204)
async def delete_prompt(prompt_id: int):
    """Delete a prompt by its ID.

    Args:
        prompt_id: The ID of the prompt to delete.

    Raises:
        HTTPException: If the prompt is not found.
    """
    try:
        deleted = PromptService.delete_prompt(prompt_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"Prompt with ID {prompt_id} not found")
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete prompt: {str(e)}")

