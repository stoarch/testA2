"""Validate Gherkin syntax and Markdown/feature scenario parity."""

from pathlib import Path
import re

from gherkin.parser import Parser


BDD_ROOT = Path(__file__).resolve().parent
FEATURE_DIR = BDD_ROOT / "features"
SCENARIO_DIR = BDD_ROOT / "scenarios"
SCENARIO_ID = re.compile(r"\bSCN-\d{3}\b")


def main() -> int:
    parser = Parser()
    feature_files = sorted(FEATURE_DIR.glob("*.feature"))
    if not feature_files:
        raise SystemExit("No .feature files found")

    parsed_ids: list[str] = []
    for feature_file in feature_files:
        document = parser.parse(feature_file.read_text(encoding="utf-8"))
        scenarios = [
            child["scenario"]
            for child in document["feature"]["children"]
            if "scenario" in child
        ]
        for scenario in scenarios:
            match = SCENARIO_ID.search(scenario["name"])
            if not match:
                raise SystemExit(
                    f"Scenario without SCN-### identifier: {feature_file}: "
                    f"{scenario['name']}"
                )
            parsed_ids.append(match.group())
        print(f"PASS {feature_file.relative_to(BDD_ROOT)}: {len(scenarios)} scenarios")

    markdown_ids = sorted(path.stem for path in SCENARIO_DIR.glob("SCN-*.md"))
    if len(parsed_ids) != len(set(parsed_ids)):
        raise SystemExit("Duplicate scenario identifiers found in .feature files")
    if sorted(parsed_ids) != markdown_ids:
        missing_features = sorted(set(markdown_ids) - set(parsed_ids))
        missing_markdown = sorted(set(parsed_ids) - set(markdown_ids))
        raise SystemExit(
            "Markdown/feature scenario mismatch: "
            f"missing feature={missing_features}, missing markdown={missing_markdown}"
        )

    print(
        f"Gherkin validation passed: {len(feature_files)} feature files, "
        f"{len(parsed_ids)} unique scenarios, Markdown parity confirmed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

