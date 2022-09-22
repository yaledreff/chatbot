"""Flight booking dialog."""

from datatypes_date_time.timex import Timex

from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, BotTelemetryClient, NullTelemetryClient
from .cancel_and_help_dialog import CancelAndHelpDialog
from .date_aller_resolver_dialog import DateAllerResolverDialog
from .date_retour_resolver_dialog import DateRetourResolverDialog
from .budget_resolver_dialog import BudgetResolverDialog

class BookingDialog(CancelAndHelpDialog):
    """Flight booking implementation."""

    def __init__(
        self,
        dialog_id: str = None,
        telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(BookingDialog, self).__init__(
            dialog_id or BookingDialog.__name__, telemetry_client
        )
        self.telemetry_client = telemetry_client
        text_prompt = TextPrompt(TextPrompt.__name__)
        text_prompt.telemetry_client = telemetry_client

        waterfall_dialog = WaterfallDialog(
            WaterfallDialog.__name__,
            [
                self.destination_step,
                self.origin_step,
                self.aller_date_step,
                self.retour_date_step,
                self.budget_step,
                self.confirm_step,
                self.final_step,
            ],
        )
        waterfall_dialog.telemetry_client = telemetry_client

        self.add_dialog(text_prompt)
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            DateAllerResolverDialog(DateAllerResolverDialog.__name__, self.telemetry_client)
        )
        self.add_dialog(
            DateRetourResolverDialog(DateRetourResolverDialog.__name__, self.telemetry_client)
        )
        self.add_dialog(
            BudgetResolverDialog(BudgetResolverDialog.__name__, self.telemetry_client)
        )
        self.add_dialog(waterfall_dialog)

        self.initial_dialog_id = WaterfallDialog.__name__

    async def destination_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for destination."""
        booking_details = step_context.options

        if booking_details.destination is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("To what city would you like to travel?")
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.destination)

    async def origin_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Prompt for origin city."""
        booking_details = step_context.options

        # Capture the response to the previous step's prompt
        booking_details.destination = step_context.result
        if booking_details.origine is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("From what city will you be travelling?")
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.origine)

    async def aller_date_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for travel date.
        This will use the DATE_RESOLVER_DIALOG."""

        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.origine = step_context.result

        if not booking_details.aller or self.is_date_ambiguous(
            booking_details.aller
        ):
            return await step_context.begin_dialog(
                DateAllerResolverDialog.__name__, booking_details.aller
            )  # pylint: disable=line-too-long

        return await step_context.next(booking_details.aller)

    async def retour_date_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for travel date.
        This will use the DATE_RESOLVER_DIALOG."""

        booking_details = step_context.options

       # Capture the results of the previous step
        booking_details.aller = step_context.result

        if not booking_details.retour or self.is_date_ambiguous(
            booking_details.retour
        ):
            return await step_context.begin_dialog(
                DateRetourResolverDialog.__name__, booking_details.retour
            )  # pylint: disable=line-too-long


        return await step_context.next(booking_details.retour)

    async def budget_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for budget.
        This will use the DATE_RESOLVER_DIALOG."""

        booking_details = step_context.options

       # Capture the results of the previous step
        booking_details.retour = step_context.result

        if booking_details.budget is None:
            return await step_context.begin_dialog(
                BudgetResolverDialog.__name__, booking_details.budget
            )  # pylint: disable=line-too-long

    
        # # Capture the results of the previous step
        # booking_details.retour = step_context.result
        # if booking_details.budget is None:
        #     return await step_context.prompt(
        #         TextPrompt.__name__,
        #         PromptOptions(
        #             prompt=MessageFactory.text("What would be your maximum budget for the flight?")
        #         ),
        #     )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.budget)

    async def confirm_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Confirm the information the user has provided."""
        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.budget = step_context.result
        msg = (
            f"Please confirm, I have you traveling to: { booking_details.destination }"
            f" from: { booking_details.origine } starting from: { booking_details.aller} to: { booking_details.retour}"
            f" for a maximum budget of: { booking_details.budget }"
        )

        # Offer a YES/NO prompt.
        return await step_context.prompt(
            ConfirmPrompt.__name__, PromptOptions(prompt=MessageFactory.text(msg))
        )

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Complete the interaction and end the dialog."""
        if step_context.result:
            booking_details = step_context.options
            booking_details.travel_date = step_context.result

            return await step_context.end_dialog(booking_details)

        return await step_context.end_dialog()

    def is_date_ambiguous(self, timex: str) -> bool:
        """Ensure time is correct."""
        timex_property = Timex(timex)
        return "definite" not in timex_property.types
