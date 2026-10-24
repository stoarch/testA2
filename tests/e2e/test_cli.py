import os
import subprocess
import sys
from pathlib import Path

from support_copilot.audit import AuditableProcessingResult
from support_copilot.contracts import ProcessingResult
from support_copilot.evaluation import EvaluationReport

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_cli_returns_schema_valid_classification_json() -> None:
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(PROJECT_ROOT / "src")

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "support_copilot",
            "--ticket-id",
            "TICKET-004",
            "--text",
            "I am frustrated because my withdrawal is still pending.",
        ],
        cwd=PROJECT_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    result = ProcessingResult.model_validate_json(completed.stdout)
    assert result.model_dump(mode="json") == {
        "ticket_id": "TICKET-004",
        "category": "withdrawal",
        "urgency": "normal",
        "language": "en",
        "sentiment": "negative",
    }


def test_cli_offline_mode_returns_auditable_draft_json() -> None:
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(PROJECT_ROOT / "src")
    snapshot_path = PROJECT_ROOT / "tests" / "fixtures" / "kb" / "synthetic_snapshot.json"

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "support_copilot",
            "--ticket-id",
            "TICKET-INTERFACE-E2E-001",
            "--text",
            "How do I make a deposit?",
            "--kb-snapshot",
            str(snapshot_path),
        ],
        cwd=PROJECT_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    result = AuditableProcessingResult.model_validate_json(completed.stdout)
    assert result.ticket_id == "TICKET-INTERFACE-E2E-001"
    assert result.answer_status == "drafted"
    assert result.answer_text
    assert result.citations[0].source_id == "KB-001"
    assert result.human_review_required is False


def test_cli_evaluation_mode_returns_schema_valid_aggregate_report() -> None:
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(PROJECT_ROOT / "src")
    evaluation_set = (
        PROJECT_ROOT / "tests" / "fixtures" / "evaluation" / "synthetic_evaluation_set.json"
    )
    snapshot_path = PROJECT_ROOT / "tests" / "fixtures" / "kb" / "synthetic_snapshot.json"

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "support_copilot",
            "--evaluation-set",
            str(evaluation_set),
            "--kb-snapshot",
            str(snapshot_path),
        ],
        cwd=PROJECT_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    report = EvaluationReport.model_validate_json(completed.stdout)
    assert report.case_count == 4
    assert report.cost.status == "unavailable"
    assert "text" not in completed.stdout
