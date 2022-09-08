"""Configuration for the bot."""

import os


class DefaultConfig:
    """Configuration for the bot."""

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "bd5930ee-1a86-48d8-b694-b4dbd6defbd9")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "GsK8Q~Sv2Z~IJ8Y1WaXjGLmLZQcAZnsgDCf7BcHj")
    LUIS_APP_ID = os.environ.get("LuisAppId", "")
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "")
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "")
    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get(
        "AppInsightsInstrumentationKey", ""
    )