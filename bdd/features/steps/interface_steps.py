import json
import os
import subprocess
import sys
from pathlib import Path

from behave import given, then, when

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SNAPSHOT_PATH = PROJECT_ROOT / "tests" / "fixtures" / "kb" / "synthetic_snapshot.json"


@given("the Phase 1 CLI or web page is running")
def step_phase_one_interface_is_running(context) -> None:
    context.interface_environment = os.environ.copy()
    context.interface_environment["PYTHONPATH"] = str(PROJECT_ROOT / "src")
    assert SNAPSHOT_PATH.is_file()


@when("an agent submits a ticket")
def step_agent_submits_ticket(context) -> None:
    context.interface_completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "support_copilot",
            "--ticket-id",
            "TICKET-BDD-018",
            "--text",
            "How do I make a deposit?",
            "--kb-snapshot",
            str(SNAPSHOT_PATH),
        ],
        cwd=PROJECT_ROOT,
        env=context.interface_environment,
        capture_output=True,
        text=True,
        check=False,
    )


@then(
    "the interface displays the structured classification, draft or abstention, citations, "
    "and review decision"
)
def step_interface_displays_structured_result(context) -> None:
    assert context.interface_completed.returncode == 0, context.interface_completed.stderr
    payload = json.loads(context.interface_completed.stdout)

    assert {"category", "urgency", "language", "sentiment"} <= payload.keys()
    assert payload["answer_status"] in {"drafted", "abstained"}
    assert payload["answer_text"]
    assert "citations" in payload
    assert "human_review_required" in payload
    assert "review_reasons" in payload
