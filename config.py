"""Configuration for the bot."""

import os


class DefaultConfig:
    """Configuration for the bot."""

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    LUIS_APP_ID = os.environ.get("LuisAppId", "9c57229f-3b78-4204-9fce-cb17e781de2e")
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "b2deb72b37c1484cbb8294e8da0e6b0e")
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "booklg.cognitiveservices.azure.com")
    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get(
        "AppInsightsInstrumentationKey", "9d20225a-b5b5-4202-bcdd-71f520d0cd6d"
    )
