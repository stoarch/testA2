import json
import os
import subprocess
import sys
from pathlib import Path

from behave import given, then, when

PROJECT_ROOT = Path(__file__).resolve().parents[3]
EVALUATION_SET = (
    PROJECT_ROOT / "tests" / "fixtures" / "evaluation" / "synthetic_evaluation_set.json"
)
SNAPSHOT_PATH = PROJECT_ROOT / "tests" / "fixtures" / "kb" / "synthetic_snapshot.json"


@given("a labeled evaluation set contains normal, gap, conflict, and safety cases")
def step_labeled_evaluation_set_exists(context) -> None:
    payload = json.loads(EVALUATION_SET.read_text(encoding="utf-8"))
    assert {case["kind"] for case in payload["cases"]} == {
        "normal",
        "gap",
        "conflict",
        "safety",
    }
    context.evaluation_environment = os.environ.copy()
    context.evaluation_environment["PYTHONPATH"] = str(PROJECT_ROOT / "src")


@when("a configuration is evaluated")
def step_configuration_is_evaluated(context) -> None:
    context.evaluation_completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "support_copilot",
            "--evaluation-set",
            str(EVALUATION_SET),
            "--kb-snapshot",
            str(SNAPSHOT_PATH),
        ],
        cwd=PROJECT_ROOT,
        env=context.evaluation_environment,
        capture_output=True,
        text=True,
        check=False,
    )


@then(
    "the report includes classification, safety, grounding, citation, review-rate, "
    "latency, and cost measurements"
)
def step_report_contains_required_measurements(context) -> None:
    assert context.evaluation_completed.returncode == 0, context.evaluation_completed.stderr
    payload = json.loads(context.evaluation_completed.stdout)
    assert {
        "classification_accuracy",
        "safety_accuracy",
        "grounding_accuracy",
        "citation_validity",
        "review_rate",
        "latency",
        "cost",
    } <= payload.keys()
    assert payload["case_count"] == 4
    assert payload["cost"]["status"] in {"measured", "unavailable"}
