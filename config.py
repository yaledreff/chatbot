"""Configuration for the bot."""

import os


class DefaultConfig:
    """Configuration for the bot."""

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "acaf63a6-d3c6-49cc-b943-cab77be92e6c")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "Ui4ce7BPF7s.LXNVy8JDGiI04spjVSXsSwGKS6yQd3qNAwnTtdbR-ic")
    LUIS_APP_ID = os.environ.get("LuisAppId", "")
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "")
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "")
    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get(
        "AppInsightsInstrumentationKey", ""
    )