import sys
from pathlib import Path

from behave import given, then, when

SRC_DIR = Path(__file__).resolve().parents[3] / "src"
sys.path.insert(0, str(SRC_DIR))


@given("a ticket asks how to withdraw funds")
def step_ticket_asks_how_to_withdraw(context) -> None:
    context.ticket_id = "TICKET-002"
    context.ticket_text = "How do I withdraw funds?"


@given("a ticket does not match deposit, withdrawal, account opening, or verification")
def step_ticket_has_unsupported_topic(context) -> None:
    context.ticket_id = "TICKET-003"
    context.ticket_text = "Can I receive a paper account statement?"


@given("a ticket is written in a detectable language and expresses frustration")
def step_ticket_is_detectable_and_frustrated(context) -> None:
    context.ticket_id = "TICKET-004"
    context.ticket_text = "I am frustrated because my withdrawal is still pending."


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


@then('the category is "other" or "unknown"')
def step_category_is_other_or_unknown(context) -> None:
    assert context.result.category in {"other", "unknown"}


@then("the category is not forced into a supported topic")
def step_category_is_not_forced(context) -> None:
    assert context.result.category not in {
        "deposit",
        "withdrawal",
        "account_opening",
        "verification",
    }


@then("category, urgency, language, and sentiment are all present")
def step_all_classifications_are_present(context) -> None:
    assert context.result.category
    assert context.result.urgency
    assert context.result.language
    assert context.result.sentiment
