import argparse
from collections.abc import Sequence
from pathlib import Path

from support_copilot.application import DEFAULT_CONFIGURATION_ID, process_offline_ticket
from support_copilot.ticket_processing import process_ticket


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Process a support ticket for agent review.")
    parser.add_argument("--ticket-id", required=True)
    parser.add_argument("--text", required=True)
    parser.add_argument("--kb-snapshot", type=Path)
    parser.add_argument("--configuration-id", default=DEFAULT_CONFIGURATION_ID)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
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
