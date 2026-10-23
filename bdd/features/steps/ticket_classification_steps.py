from pathlib import Path
import sys

from behave import given, then, when


SRC_DIR = Path(__file__).resolve().parents[3] / "src"
sys.path.insert(0, str(SRC_DIR))


@given("a ticket asks how to withdraw funds")
def step_ticket_asks_how_to_withdraw(context) -> None:
    context.ticket_id = "TICKET-002"
    context.ticket_text = "How do I withdraw funds?"


@when("it is classified")
def step_ticket_is_classified(context) -> None:
    from support_copilot.ticket_processing import process_ticket

    context.result = process_ticket(
        ticket_id=context.ticket_id,
        text=context.ticket_text,
    )


@then('the category is "withdrawal"')
def step_category_is_withdrawal(context) -> None:
    assert context.result.category == "withdrawal"
