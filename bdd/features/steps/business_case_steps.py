import json
import os
import subprocess
import sys
from pathlib import Path

from behave import given, then, when

PROJECT_ROOT = Path(__file__).resolve().parents[3]
INPUT_PATH = PROJECT_ROOT / "reports" / "business-case-input.json"


@given("measured configuration results and explicit staffing and cost assumptions")
def step_business_case_inputs_exist(context) -> None:
    payload = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    assert payload["monthly_volume"] == 10_000
    assert {item["configuration_id"] for item in payload["configurations"]} == {
        "A",
        "B",
        "C",
    }
    context.business_case_environment = os.environ.copy()
    context.business_case_environment["PYTHONPATH"] = str(PROJECT_ROOT / "src")


@when("the one-page business case is generated")
def step_business_case_is_generated(context) -> None:
    context.business_case_completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "support_copilot",
            "--business-case-input",
            str(INPUT_PATH),
            "--business-case-format",
            "json",
        ],
        cwd=PROJECT_ROOT,
        env=context.business_case_environment,
        capture_output=True,
        text=True,
        check=False,
    )
    assert context.business_case_completed.returncode == 0, context.business_case_completed.stderr
    context.business_case_report = json.loads(context.business_case_completed.stdout)


@then("it estimates monthly cost and benefit at 10,000 tickets")
def step_business_case_estimates_target_volume(context) -> None:
    report = context.business_case_report
    assert report["monthly_volume"] == 10_000
    assert len(report["projections"]) == 9
    assert all(item["projection_kind"] == "estimate" for item in report["projections"])
    assert all("monthly_run_cost" in item for item in report["projections"])
    assert all("monthly_net_value" in item for item in report["projections"])


@then("it identifies the recommended configuration or states that none is justified")
def step_business_case_states_decision(context) -> None:
    report = context.business_case_report
    assert report["conclusion"] in {"go", "conditional_go", "no_go"}
    if report["recommendation_configuration_id"] is None:
        assert report["conclusion"] == "no_go"
        assert report["decision_reasons"]
