import sys
from pathlib import Path

from behave import given, then, when

SRC_DIR = Path(__file__).resolve().parents[3] / "src"
sys.path.insert(0, str(SRC_DIR))


@given("a ticket has an identifier and text")
def step_ticket_has_identifier_and_text(context) -> None:
    context.ticket_id = "TICKET-001"
    context.ticket_text = "How do I withdraw funds?"


@when("the co-pilot processes it")
def step_copilot_processes_ticket(context) -> None:
    from support_copilot.ticket_processing import process_ticket

    context.result = process_ticket(
        ticket_id=context.ticket_id,
        text=context.ticket_text,
    )


@then("the result contains the same ticket identifier")
def step_result_preserves_ticket_identifier(context) -> None:
    assert context.result.ticket_id == context.ticket_id
