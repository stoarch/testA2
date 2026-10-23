from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "doc"
ADR_DIR = DOCS / "adr"
UML_DIR = DOCS / "uml"

REQUIRED_PUML = {
    "component-overview.puml",
    "domain-class.puml",
    "processing-sequence.puml",
    "processing-activity.puml",
}
REQUIRED_ADR_SECTIONS = (
    "## Context",
    "## Options considered",
    "## Decision",
    "## Consequences",
    "## Validation",
)
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def validate_plantuml(errors: list[str]) -> None:
    sources = {path.name for path in UML_DIR.glob("*.puml")}
    missing = REQUIRED_PUML - sources
    if missing:
        errors.append(f"Missing required PlantUML sources: {sorted(missing)}")

    for path in UML_DIR.glob("*.puml"):
        text = path.read_text(encoding="utf-8").strip()
        if not text.startswith("@startuml") or not text.endswith("@enduml"):
            errors.append(f"Invalid PlantUML envelope: {path.relative_to(ROOT)}")

    for path in UML_DIR.glob("*.md"):
        if "```mermaid" in path.read_text(encoding="utf-8").casefold():
            errors.append(f"Mermaid remains in authoritative UML docs: {path.relative_to(ROOT)}")


def validate_adrs(errors: list[str]) -> None:
    accepted = 0
    for path in ADR_DIR.glob("[0-9][0-9][0-9][0-9]-*.md"):
        if path.name == "0000-template.md":
            continue
        text = path.read_text(encoding="utf-8")
        if "- Status: Accepted" in text:
            accepted += 1
        for section in REQUIRED_ADR_SECTIONS:
            if section not in text:
                errors.append(f"{path.relative_to(ROOT)} lacks {section}")
    if accepted < 5:
        errors.append(f"Expected at least 5 accepted ADRs, found {accepted}")


def validate_relative_links(errors: list[str]) -> None:
    roots = [ROOT / "README.md", DOCS, ROOT / "bdd", ROOT / "DASHBOARD", ROOT / "reports"]
    markdown_files: list[Path] = []
    for candidate in roots:
        if candidate.is_file():
            markdown_files.append(candidate)
        elif candidate.exists():
            markdown_files.extend(candidate.rglob("*.md"))

    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        for raw_target in LINK_PATTERN.findall(text):
            target = raw_target.strip().strip("<>").split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(
                    f"Broken link in {path.relative_to(ROOT)}: {raw_target}"
                )


def main() -> int:
    errors: list[str] = []
    validate_plantuml(errors)
    validate_adrs(errors)
    validate_relative_links(errors)

    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1

    accepted = sum(
        "- Status: Accepted" in path.read_text(encoding="utf-8")
        for path in ADR_DIR.glob("[0-9][0-9][0-9][0-9]-*.md")
        if path.name != "0000-template.md"
    )
    print(
        "Architecture documentation validation passed: "
        f"{accepted} accepted ADRs, "
        f"{len(list(UML_DIR.glob('*.puml')))} PlantUML sources, relative links valid"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
