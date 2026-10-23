import argparse
from collections.abc import Sequence

from support_copilot.ticket_processing import process_ticket


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Process a support ticket for agent review.")
    parser.add_argument("--ticket-id", required=True)
    parser.add_argument("--text", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    result = process_ticket(ticket_id=arguments.ticket_id, text=arguments.text)
    print(result.model_dump_json())
    return 0
