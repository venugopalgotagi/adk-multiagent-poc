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
    logging.info(f"{callback_context.agent_name} is being called for session {callback_context.session.id} ")


def logger_after_agent_callback(callback_context: google.adk.agents.callback_context.CallbackContext) -> \
        typing.Optional[Content]:
    logging.info(f"{callback_context.agent_name} is executed for session {callback_context.session.id}")
