"""App configuration for the Video Risk Assessment application.

This module defines the ADK App instance, configuring the root agent and
other application-level settings.
"""

from google.adk.apps import App

import agents.root_agent

app = App(
    name="Video_Risk_Assessment",
    root_agent=agents.root_agent.root_agent,
    # plugins=[SaveFilesAsArtifactsPlugin()]
)
