"""Database models for the application."""

import os
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import Optional, List

Base = declarative_base()

class Prompt(Base):

# Pydantic models moved to top-level
    """Model for storing agent prompts."""
    __tablename__ = 'prompts'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    app_name = Column(String, nullable=False, default="Video_Risk_Assessment")
    region = Column(String, nullable=False, default="us-central1")
    version = Column(Integer, default=1)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('name', 'app_name', 'region', name='uix_name_app_region'),
    )

# Pydantic models for API payloads

class PromptCreate(BaseModel):
    """Schema for creating a new prompt."""
    name: str
    content: str
    app_name: Optional[str] = None
    region: Optional[str] = None

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

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres")
if "asyncpg" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("asyncpg", "psycopg2")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize the database tables."""
    Base.metadata.create_all(bind=engine)
