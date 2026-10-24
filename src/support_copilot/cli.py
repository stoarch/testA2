import argparse
from collections.abc import Sequence
from pathlib import Path

from support_copilot.application import DEFAULT_CONFIGURATION_ID, process_offline_ticket
from support_copilot.business_case import generate_business_case, render_business_case_markdown
from support_copilot.evaluation import run_offline_evaluation
from support_copilot.ticket_processing import process_ticket


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Process a support ticket for agent review.")
    parser.add_argument("--ticket-id")
    parser.add_argument("--text")
    parser.add_argument("--kb-snapshot", type=Path)
    parser.add_argument("--evaluation-set", type=Path)
    parser.add_argument("--business-case-input", type=Path)
    parser.add_argument(
        "--business-case-format",
        choices=("json", "markdown"),
        default="markdown",
    )
    parser.add_argument("--configuration-id", default=DEFAULT_CONFIGURATION_ID)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    arguments = parser.parse_args(argv)
    if arguments.business_case_input is not None:
        result = generate_business_case(arguments.business_case_input)
        if arguments.business_case_format == "json":
            print(result.model_dump_json())
        else:
            print(render_business_case_markdown(result), end="")
        return 0

    if arguments.evaluation_set is not None:
        if arguments.kb_snapshot is None:
            parser.error("--kb-snapshot is required with --evaluation-set")
        result = run_offline_evaluation(
            arguments.evaluation_set,
            arguments.kb_snapshot,
            configuration_id=arguments.configuration_id,
        )
        print(result.model_dump_json())
        return 0

    if arguments.ticket_id is None or arguments.text is None:
        parser.error(
            "--ticket-id and --text are required unless an evaluation or business-case mode is used"
        )
    if arguments.kb_snapshot is None:
        result = process_ticket(ticket_id=arguments.ticket_id, text=arguments.text)
    else:
        result = process_offline_ticket(
            ticket_id=arguments.ticket_id,
            text=arguments.text,
            snapshot_path=arguments.kb_snapshot,
            configuration_id=arguments.configuration_id,
        )
    print(result.model_dump_json())
    return 0
