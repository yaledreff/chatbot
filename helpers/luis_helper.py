from enum import Enum
from typing import Dict, Tuple
from botbuilder.ai.luis import LuisRecognizer
from botbuilder.core import IntentScore, TopIntent, TurnContext

from booking_details import BookingDetails


class Intent(Enum):
    BOOK_FLIGHT = "booking"
    NONE_INTENT = "NoneIntent"

def top_intent(intents: Dict[Intent, dict]) -> TopIntent:
    max_intent = Intent.NONE_INTENT
    max_value = 0.0

    for intent, value in intents:
        intent_score = IntentScore(value)
        if intent_score.score > max_value:
            max_intent, max_value = intent, intent_score.score

    return TopIntent(max_intent, max_value)


class LuisHelper:
    @staticmethod
    async def execute_luis_query(luis_recognizer: LuisRecognizer, turn_context: TurnContext) -> (Intent, object):
        """
        Returns an object with preformatted LUIS results for the bot's dialogs to consume.
        """
        result = None
        intent = None

        try:
            recognizer_result = await luis_recognizer.recognize(turn_context)

            intent = (
                sorted(
                    recognizer_result.intents,
                    key=recognizer_result.intents.get,
                    reverse=True,
                )[:1][0]
                if recognizer_result.intents
                else None
            )

            if intent == Intent.BOOK_FLIGHT.value:
                result = BookingDetails()

                # We need to get the result from the LUIS JSON which at every level returns an array.
                to_entities = recognizer_result.entities.get("$instance", {}).get(
                    "destination", []
                )

                if len(to_entities) > 0:
                    result.destination = to_entities[0]["text"].capitalize()

                from_entities = recognizer_result.entities.get("$instance", {}).get(
                    "origine", []
                )
                if len(from_entities) > 0:
                    result.origine = from_entities[0]["text"].capitalize()

                aller_entities = recognizer_result.entities.get("$instance", {}).get(
                    "aller", []
                )
                if len(aller_entities) > 0:
                    result.aller = aller_entities[0]["text"].capitalize()
               
                retour_entities = recognizer_result.entities.get("$instance", {}).get(
                    "retour", []
                )
                if len(retour_entities) > 0:
                        result.retour = retour_entities[0]["text"].capitalize()

                budget_entities = recognizer_result.entities.get("$instance", {}).get(
                    "budget", []
                )
                if len(budget_entities) > 0:
                    result.budget = budget_entities[0]["text"].capitalize()

                else:
                    result.travel_date = None

        except Exception as exception:
            print(exception)

        return intent, result