from google.adk.apps import App

import agents.root_agent

app = App(
    name="Video_Risk_Assessment",
    root_agent=agents.root_agent.root_agent,
    # plugins=[SaveFilesAsArtifactsPlugin()]
)
