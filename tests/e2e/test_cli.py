import os
import subprocess
import sys
from pathlib import Path

from support_copilot.contracts import ProcessingResult

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
