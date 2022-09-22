
import sys
import pathlib
import pytest
import aiounittest
import asyncio

from botbuilder.dialogs.prompts import (
    AttachmentPrompt, 
    PromptOptions, 
    PromptValidatorContext, 
)

from botbuilder.core import (
    TurnContext, 
    ConversationState, 
    MemoryStorage, 
    MessageFactory, 
)
from botbuilder.schema import Activity, ActivityTypes, Attachment
from botbuilder.dialogs import DialogSet, DialogTurnStatus
from botbuilder.core.adapters import TestAdapter

from botbuilder.dialogs.prompts import (
    DateTimePrompt,
    PromptValidatorContext,
    PromptOptions,
    DateTimeResolution,
)

from date_aller_resolver_dialog import DateAllerResolverDialog
from budget_resolver_dialog import BudgetResolverDialog
from date_retour_resolver_dialog import DateRetourResolverDialog

from botbuilder.community.dialogs.prompts import NumberWithUnitPrompt, NumberWithUnitPromptType

class BookingPromptTest(aiounittest.AsyncTestCase):

    async def test_booking_prompt_date_20220423(self):
        async def exec_test(turn_context:TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results = await dialog_context.continue_dialog()
            if (results.status == DialogTurnStatus.Empty):
                options = PromptOptions(
                    prompt = Activity(
                        type = ActivityTypes.message, 
                        text = "On what date would you like to start the travel ?"
                        )
                    )
                await dialog_context.prompt("date-aller", options)

            elif results.status == DialogTurnStatus.Complete:
                reply = results.result
                await turn_context.send_activity(reply[0].timex)

            await conv_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)

        conv_state = ConversationState(MemoryStorage())

        dialogs_state = conv_state.create_property("dialog-state")
        dialogs = DialogSet(dialogs_state)

        date_time_prompt = DateTimePrompt(
            "date-aller", DateAllerResolverDialog.datetime_prompt_validator
        )

        dialogs.add(date_time_prompt)

        step1 = await adapter.test('Hello', 'On what date would you like to start the travel ?')
        step2 = await step1.send('I would like to fly on 23 of April 2022')
        await step2.assert_reply("2022-04-23")

    async def test_booking_prompt_date_20230812(self):
        async def exec_test(turn_context:TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results = await dialog_context.continue_dialog()
            if (results.status == DialogTurnStatus.Empty):
                options = PromptOptions(
                    prompt = Activity(
                        type = ActivityTypes.message, 
                        text = "On what date would you like to start the travel ?"
                        )
                    )
                await dialog_context.prompt("date-retour", options)

            elif results.status == DialogTurnStatus.Complete:
                reply = results.result
                await turn_context.send_activity(reply[0].timex)

            await conv_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)

        conv_state = ConversationState(MemoryStorage())

        dialogs_state = conv_state.create_property("dialog-state")
        dialogs = DialogSet(dialogs_state)

        date_time_prompt = DateTimePrompt(
            "date-retour", DateRetourResolverDialog.datetime_prompt_validator
        )

        dialogs.add(date_time_prompt)

        step1 = await adapter.test('Hello', 'On what date would you like to start the travel ?')
        step2 = await step1.send('I would like to fly on August 12 2023')
        await step2.assert_reply("2023-08-12")

    async def test_booking_prompt_date_XXXX0812(self):
        async def exec_test(turn_context:TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results = await dialog_context.continue_dialog()
            if (results.status == DialogTurnStatus.Empty):
                options = PromptOptions(
                    prompt = Activity(
                        type = ActivityTypes.message, 
                        text = "On what date would you like to start the travel ?"
                        )
                    )
                await dialog_context.prompt("date-aller", options)

            elif results.status == DialogTurnStatus.Complete:
                reply = results.result
                await turn_context.send_activity(reply[0].timex)

            elif results.status == DialogTurnStatus.Waiting:
                reply = "formulation incomplète"
                await turn_context.send_activity(reply)

            await conv_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)

        conv_state = ConversationState(MemoryStorage())

        dialogs_state = conv_state.create_property("dialog-state")
        dialogs = DialogSet(dialogs_state)

        date_time_prompt = DateTimePrompt(
            "date-aller", DateAllerResolverDialog.datetime_prompt_validator
        )

        dialogs.add(date_time_prompt)

        step1 = await adapter.test('Hello', 'On what date would you like to start the travel ?')
        step2 = await step1.send('I would like to fly on August 12th')
        await step2.assert_reply("On what date would you like to start the travel ?")


    async def test_booking_prompt_budget_1500eur(self):
        async def exec_test(turn_context:TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results = await dialog_context.continue_dialog()
            if (results.status == DialogTurnStatus.Empty):
                options = PromptOptions(
                    prompt = Activity(
                        type = ActivityTypes.message, 
                        text = "What is your budget for the flight ?"
                        )
                    )
                await dialog_context.prompt("budget", options)

            elif results.status == DialogTurnStatus.Complete:
                reply = results.result
                budget = reply.value + ' ' + reply.unit
                await turn_context.send_activity(budget)

            elif results.status == DialogTurnStatus.Waiting:
                reply = "formulation incomplète"
                await turn_context.send_activity(reply)

            await conv_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)

        conv_state = ConversationState(MemoryStorage())

        dialogs_state = conv_state.create_property("dialog-state")
        dialogs = DialogSet(dialogs_state)

        budget_prompt = NumberWithUnitPrompt(
            "budget", NumberWithUnitPromptType.Currency, BudgetResolverDialog.budget_prompt_validator
        )

        dialogs.add(budget_prompt)

        step1 = await adapter.test('Hello', 'What is your budget for the flight ?')
        step2 = await step1.send('I could spend 1500 eur maximum')
        await step2.assert_reply("1500 Euro")

    async def test_booking_prompt_budget_2200gbp(self):
        async def exec_test(turn_context:TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results = await dialog_context.continue_dialog()
            if (results.status == DialogTurnStatus.Empty):
                options = PromptOptions(
                    prompt = Activity(
                        type = ActivityTypes.message, 
                        text = "What is your budget for the flight ?"
                        )
                    )
                await dialog_context.prompt("budget", options)

            elif results.status == DialogTurnStatus.Complete:
                reply = results.result
                budget = reply.value + ' ' + reply.unit
                await turn_context.send_activity(budget)

            elif results.status == DialogTurnStatus.Waiting:
                reply = "formulation incomplète"
                await turn_context.send_activity(reply)

            await conv_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)

        conv_state = ConversationState(MemoryStorage())

        dialogs_state = conv_state.create_property("dialog-state")
        dialogs = DialogSet(dialogs_state)

        budget_prompt = NumberWithUnitPrompt(
            "budget", NumberWithUnitPromptType.Currency, BudgetResolverDialog.budget_prompt_validator
        )

        dialogs.add(budget_prompt)

        step1 = await adapter.test('Hello', 'What is your budget for the flight ?')
        step2 = await step1.send('I could spend two thousand gbp maximum')
        await step2.assert_reply("2000 British pound")

    async def test_booking_prompt_budget_1200XXXX(self):
        async def exec_test(turn_context:TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results = await dialog_context.continue_dialog()
            if (results.status == DialogTurnStatus.Empty):
                options = PromptOptions(
                    prompt = Activity(
                        type = ActivityTypes.message, 
                        text = "What is your budget for the flight ?"
                        )
                    )
                await dialog_context.prompt("budget", options)

            elif results.status == DialogTurnStatus.Complete:
                reply = results.result
                budget = reply.value + ' ' + reply.unit
                await turn_context.send_activity(budget)

            elif results.status == DialogTurnStatus.Waiting:
                reply = "formulation incomplète"
                await turn_context.send_activity(reply)

            await conv_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)

        conv_state = ConversationState(MemoryStorage())

        dialogs_state = conv_state.create_property("dialog-state")
        dialogs = DialogSet(dialogs_state)

        budget_prompt = NumberWithUnitPrompt(
            "budget", NumberWithUnitPromptType.Currency, BudgetResolverDialog.budget_prompt_validator
        )

        dialogs.add(budget_prompt)

        step1 = await adapter.test('Hello', 'What is your budget for the flight ?')
        step2 = await step1.send('I could spend 1200')
        # await step2.assert_reply("Force unit test failure for testing")
        await step2.assert_reply("What is your budget for the flight ?")