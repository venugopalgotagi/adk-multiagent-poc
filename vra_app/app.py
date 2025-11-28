from google.adk.apps import App
from google.adk.plugins.save_files_as_artifacts_plugin import SaveFilesAsArtifactsPlugin

import agents.root_agent

app = App(
    name="Video_Risk_Assessment",
    root_agent=agents.root_agent.root_agent,
    #plugins=[SaveFilesAsArtifactsPlugin()]
)