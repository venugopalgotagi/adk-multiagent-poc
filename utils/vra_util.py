"""Utility functions for the Video Risk Assessment application.

This module provides utility functions, primarily for logging agent execution
callbacks (before and after agent execution).
"""

import google.adk.agents.callback_context
import logging
import typing
from google.genai.types import Content

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
)


def logger_before_agent_callback(callback_context: google.adk.agents.callback_context.CallbackContext) -> \
typing.Optional[Content]:
    """Callback function executed before an agent starts.

    Args:
        callback_context: The context of the callback, containing agent and session info.

    Returns:
        None.
    """
    logging.info(f"{callback_context.agent_name} is being called for session {callback_context.session.id} ")


def logger_after_agent_callback(callback_context: google.adk.agents.callback_context.CallbackContext) -> \
        typing.Optional[Content]:
    """Callback function executed after an agent finishes.

    Args:
        callback_context: The context of the callback, containing agent and session info.

    Returns:
        None.
    """
    logging.info(f"{callback_context.agent_name} is executed for session {callback_context.session.id}")
