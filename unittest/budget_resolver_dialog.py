"""Handle date/time resolution for booking dialog."""

from datatypes_date_time.timex import Timex

from botbuilder.core import MessageFactory, BotTelemetryClient, NullTelemetryClient
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext
from botbuilder.dialogs.prompts import (
    NumberPrompt,
    PromptValidatorContext,
    PromptOptions,
    DateTimeResolution,
)
from cancel_and_help_dialog import CancelAndHelpDialog

from botbuilder.community.dialogs.prompts import NumberWithUnitPrompt, NumberWithUnitPromptType


class BudgetResolverDialog(CancelAndHelpDialog):
    """Resolve the budget"""

    def __init__(
        self,
        dialog_id: str = None,
        telemetry_client: BotTelemetryClient = NullTelemetryClient()        
    ):
        super(BudgetResolverDialog, self).__init__(
            dialog_id or BudgetResolverDialog.__name__, telemetry_client
        )
        self.telemetry_client = telemetry_client

        budget_prompt = NumberWithUnitPrompt(
            NumberWithUnitPrompt.__name__, NumberWithUnitPromptType.Currency, BudgetResolverDialog.budget_prompt_validator
        )
        budget_prompt.telemetry_client = telemetry_client

        waterfall_dialog = WaterfallDialog(
            WaterfallDialog.__name__ + "2", [self.initial_step, self.final_step]
        )
        waterfall_dialog.telemetry_client = telemetry_client

        self.add_dialog(budget_prompt)
        self.add_dialog(waterfall_dialog)

        self.initial_dialog_id = WaterfallDialog.__name__ + "2"

    async def initial_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for the budget."""
        budget = step_context.options

        prompt_msg = "What would be your budget for the flight"
        reprompt_msg = (
            "I'm sorry, for best results, please enter your budget amount with currency"
        )

        if budget is None:
            # We were not given any date at all so prompt the user.
            return await step_context.prompt(
                NumberWithUnitPrompt.__name__,
                PromptOptions(  # pylint: disable=bad-continuation
                    prompt=MessageFactory.text(prompt_msg),
                    retry_prompt=MessageFactory.text(reprompt_msg),
                ),
            )

        # # We have a Date we just need to check it is unambiguous.
        # if "definite" in Timex(timex).types:
        #     # This is essentially a "reprompt" of the data we were given up front.
        #     return await step_context.prompt(
        #         NumberWithUnitPrompt.__name__, PromptOptions(prompt=reprompt_msg)
        #     )

        return await step_context.next(NumberWithUnitPrompt(budget=budget))

    async def final_step(self, step_context: WaterfallStepContext):
        """Cleanup - set final return value and end dialog."""
        value = step_context.result.value 
        unit = step_context.result.unit
        budget = value + ' ' + unit
        return await step_context.end_dialog(budget)

    @staticmethod
    async def budget_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        """ Validate the date provided is in proper form. """

        return prompt_context.recognized.succeeded

