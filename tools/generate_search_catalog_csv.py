#!/usr/bin/env python3

"""Generate SCRIPTS_CATALOG.csv from the curated SCRIPTS_CATALOG.txt catalog."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_TXT = ROOT / "SCRIPTS_CATALOG.txt"
CATALOG_CSV = ROOT / "SCRIPTS_CATALOG.csv"
SEPARATOR = "=" * 80


def parse_catalog(text: str) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    mode: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()

        if line == SEPARATOR:
            if current and current.get("script"):
                entries.append(current)
            current = None
            mode = None
            continue

        if line.startswith("SCRIPT: "):
            if current and current.get("script"):
                entries.append(current)
            current = {
                "script": line.removeprefix("SCRIPT: ").strip(),
                "category": "",
                "keywords": "",
                "purpose": "",
                "syntax": "",
                "examples": [],
            }
            mode = None
            continue

        if current is None:
            continue

        if line.startswith("CATEGORY: "):
            current["category"] = line.removeprefix("CATEGORY: ").strip()
            mode = None
        elif line.startswith("KEYWORDS: "):
            current["keywords"] = line.removeprefix("KEYWORDS: ").strip()
            mode = None
        elif line.startswith("PURPOSE: "):
            current["purpose"] = line.removeprefix("PURPOSE: ").strip()
            mode = None
        elif line.startswith("SYNTAX: "):
            current["syntax"] = line.removeprefix("SYNTAX: ").strip()
            mode = None
        elif line == "EXAMPLES:":
            mode = "examples"
        elif line == "PARAMETERS:":
            mode = "parameters"
        elif mode == "examples" and line.startswith("  "):
            example = line.strip()
            if example:
                current["examples"].append(example)
        elif mode == "parameters":
            continue

    if current and current.get("script"):
        entries.append(current)

    return entries


def write_csv(entries: list[dict[str, object]]) -> None:
    with CATALOG_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="|", lineterminator="\n")
        writer.writerow(
            [
                "Script",
                "Category",
                "Keywords",
                "Purpose",
                "Syntax",
                "Example1",
                "Example2",
                "Example3",
            ]
        )

        for entry in entries:
            examples = list(entry["examples"])[:3]
            while len(examples) < 3:
                examples.append("")
            writer.writerow(
                [
                    entry["script"],
                    entry["category"],
                    entry["keywords"],
                    entry["purpose"],
                    entry["syntax"],
                    *examples,
                ]
            )


def main() -> None:
    entries = parse_catalog(CATALOG_TXT.read_text(encoding="utf-8"))
    write_csv(entries)
    print(f"Wrote {len(entries)} entries to {CATALOG_CSV}")


if __name__ == "__main__":
    main()
