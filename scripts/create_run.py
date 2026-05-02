#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


RUN_FILES = {
    "intake.md": """# Intake

## Work packet name

## Source material

## Initial reaction

## Target audience

## Desired output

## Constraints

## Definition of done

""",
    "research-pack.md": "# Research Pack\n\n",
    "strategy-pack.md": "# Strategy Pack\n\n",
    "draft-output.md": "# Draft Output\n\n",
    "artefacts.md": "# Artefacts\n\n",
    "qa-report.md": "# QA Report\n\n",
    "approval-pack.md": "# Approval Pack\n\n",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a new run folder.")
    parser.add_argument("run_id", help="Run ID, e.g. 002-job-ad-analysis")
    args = parser.parse_args()

    run_dir = REPO_ROOT / "runs" / args.run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    for filename, content in RUN_FILES.items():
        path = run_dir / filename
        if not path.exists():
            path.write_text(content, encoding="utf-8")

    print(f"Created run folder: {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
