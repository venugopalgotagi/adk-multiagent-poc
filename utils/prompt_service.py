"""Service for interacting with prompts in the database."""

from sqlalchemy.orm import Session
from utils.models import Prompt, SessionLocal
from typing import List, Optional

class PromptService:
    """Service class for managing prompts."""

    @staticmethod
    def get_latest_prompt(name: str, app_name: str, region: str) -> str:
        """Fetches the latest version of a prompt by name, app_name, and region.

        Args:
            name: The name of the prompt.
            app_name: The application name.
            region: The region.

        Returns:
            The content of the prompt.

        Raises:
            ValueError: If the prompt is not found.
        """
        session: Session = SessionLocal()
        try:
            prompt = session.query(Prompt).filter(
                Prompt.name == name,
                Prompt.app_name == app_name,
                Prompt.region == region
            ).first()
            if prompt:
                return prompt.content
            else:
                raise ValueError(f"Prompt with name '{name}', app_name '{app_name}', region '{region}' not found.")
        finally:
            session.close()

    @staticmethod
    def add_prompt(name: str, content: str, app_name: str, region: str):
        """Adds a new prompt or updates an existing one.

        Args:
            name: The name of the prompt.
            content: The content of the prompt.
            app_name: The application name.
            region: The region.
        """
        session: Session = SessionLocal()
        try:
            prompt = session.query(Prompt).filter(
                Prompt.name == name,
                Prompt.app_name == app_name,
                Prompt.region == region
            ).first()
            if prompt:
                prompt.content = content
                prompt.version += 1
            else:
                prompt = Prompt(name=name, content=content, app_name=app_name, region=region)
                session.add(prompt)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_all_prompts(app_name: Optional[str] = None, region: Optional[str] = None) -> List[Prompt]:
        """Fetches all prompts, optionally filtered by app_name and/or region.

        Args:
            app_name: Optional application name filter.
            region: Optional region filter.

        Returns:
            List of Prompt objects.
        """
        session: Session = SessionLocal()
        try:
            query = session.query(Prompt)
            if app_name:
                query = query.filter(Prompt.app_name == app_name)
            if region:
                query = query.filter(Prompt.region == region)
            return query.all()
        finally:
            session.close()

    @staticmethod
    def get_prompt_by_id(prompt_id: int) -> Optional[Prompt]:
        """Fetches a prompt by its ID.

        Args:
            prompt_id: The ID of the prompt to fetch.

        Returns:
            Prompt object if found, None otherwise.
        """
        session: Session = SessionLocal()
        try:
            return session.query(Prompt).filter(Prompt.id == prompt_id).first()
        finally:
            session.close()

    @staticmethod
    def get_prompt_by_name(name: str, app_name: str, region: str) -> Optional[Prompt]:
        """Fetches a prompt by name, app_name, and region.

        Args:
            name: The name of the prompt.
            app_name: The application name.
            region: The region.

        Returns:
            Prompt object if found, None otherwise.
        """
        session: Session = SessionLocal()
        try:
            return session.query(Prompt).filter(
                Prompt.name == name,
                Prompt.app_name == app_name,
                Prompt.region == region
            ).first()
        finally:
            session.close()

    @staticmethod
    def update_prompt(prompt_id: int, content: str) -> Optional[Prompt]:
        """Updates an existing prompt's content and increments version.

        Args:
            prompt_id: The ID of the prompt to update.
            content: The new content for the prompt.

        Returns:
            Updated Prompt object if found, None otherwise.

        Raises:
            Exception: If database operation fails.
        """
        session: Session = SessionLocal()
        try:
            prompt = session.query(Prompt).filter(Prompt.id == prompt_id).first()
            if prompt:
                prompt.content = content
                prompt.version += 1
                session.commit()
                session.refresh(prompt)
                return prompt
            return None
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def delete_prompt(prompt_id: int) -> bool:
        """Deletes a prompt by its ID.

        Args:
            prompt_id: The ID of the prompt to delete.

        Returns:
            True if deleted successfully, False if not found.

        Raises:
            Exception: If database operation fails.
        """
        session: Session = SessionLocal()
        try:
            prompt = session.query(Prompt).filter(Prompt.id == prompt_id).first()
            if prompt:
                session.delete(prompt)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

