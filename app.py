from http import HTTPStatus
import logging

from aiohttp import web
from aiohttp.web import Request, Response, json_response

from botbuilder.core import (
    BotFrameworkAdapterSettings,
    ConversationState,
    MemoryStorage,
    UserState,
    TelemetryLoggerMiddleware,
)
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.schema import Activity
from botbuilder.applicationinsights import ApplicationInsightsTelemetryClient
from botbuilder.integration.applicationinsights.aiohttp import (
    AiohttpTelemetryProcessor,
    bot_telemetry_middleware,
)

from config import DefaultConfig

from adapter_with_error_handler import AdapterWithErrorHandler
from flight_booking_recognizer import FlightBookingRecognizer
from bot.dialog_and_welcome_bot import DialogAndWelcomeBot
from dialogs.main_dialog import MainDialog
from dialogs.booking_dialog import BookingDialog

from bot.echobot import EchoBot

#####################################################################################################

CONFIG = DefaultConfig()
SETTINGS = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)

MEMORY = MemoryStorage()
USER_STATE = UserState(MEMORY)
CONVERSATION_STATE = ConversationState(MEMORY)

ADAPTER = AdapterWithErrorHandler(SETTINGS, CONVERSATION_STATE)

INSTRUMENTATION_KEY = CONFIG.APPINSIGHTS_INSTRUMENTATION_KEY
TELEMETRY_CLIENT = ApplicationInsightsTelemetryClient(
    INSTRUMENTATION_KEY, telemetry_processor=AiohttpTelemetryProcessor(), client_queue_size=10
)
RECOGNIZER = FlightBookingRecognizer(CONFIG)
BOOKING_DIALOG = BookingDialog()
DIALOG = MainDialog(RECOGNIZER, BOOKING_DIALOG, telemetry_client=TELEMETRY_CLIENT)
BOT = DialogAndWelcomeBot(CONVERSATION_STATE, USER_STATE, DIALOG, TELEMETRY_CLIENT)
# BOT = EchoBot()

async def messages(req: Request) -> Response:
    # Main bot message handler.
    # if "application/json" in req.headers["Content-Type"]:

    logging.warning("header :" + str(req.headers))
    logging.warning("json :" + str(req.text))

    logging.warning("APP ID :" + CONFIG.APP_ID)
    logging.warning("APP PWD :" + CONFIG.APP_PASSWORD)
    
    body = await req.json()
    # else:
    #    return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)

    if response:
        return json_response(data=response.body, status=response.status)
    return Response(status=HTTPStatus.OK)

def init_func(argv):
  APP = web.Application(middlewares=[bot_telemetry_middleware, aiohttp_error_middleware])
  APP.router.add_post("/api/messages", messages)
  return APP

if __name__ == "__main__":
    APP = init_func(None)
    try:
        web.run_app(APP, host="localhost", port=CONFIG.PORT)
    except Exception as error:
        raise error