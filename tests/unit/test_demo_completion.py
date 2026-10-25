from pathlib import Path

from support_copilot.application import process_offline_ticket
from support_copilot.contracts import SupportTicket
from support_copilot.safety import SafetyFlag, apply_safety_policy
from support_copilot.ticket_processing import classify_category

SNAPSHOT = Path(__file__).resolve().parents[1] / "fixtures" / "kb" / "synthetic_snapshot.json"


def test_four_categories():
    assert classify_category("How do I deposit?") == "deposit"
    assert classify_category("How do I withdraw?") == "withdrawal"
    assert classify_category("How do I open an account?") == "account_opening"
    assert classify_category("How do I verify my account?") == "verification"
    assert classify_category("How do I withdraw and deposit?") == "other"


def test_aml_outcome_escalates():
    ticket = SupportTicket(
        ticket_id="t", text="Should we release this AML-flagged transaction?"
    )
    decision = apply_safety_policy(ticket)
    assert decision is not None
    assert SafetyFlag.AML_DECISION in decision.safety_flags
    assert decision.human_review_required


def test_no_unrelated_deposit_answer_for_other_topics():
    r = process_offline_ticket(
        ticket_id="t", text="How do I open an account?", snapshot_path=SNAPSHOT
    )
    assert r.answer_status == "abstained"
    assert r.human_review_required


def test_fee_query_abstains():
    r = process_offline_ticket(
        ticket_id="t", text="What is the deposit fee?", snapshot_path=SNAPSHOT
    )
    assert r.answer_status == "abstained"
