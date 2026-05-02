#!/usr/bin/env bash

set -e

echo "Updating repo with programmatic agent runner skeleton..."

mkdir -p scripts
mkdir -p config
mkdir -p prompts
mkdir -p logs

cat > requirements.txt <<'REQ'
openai>=2.0.0
python-dotenv>=1.0.1
PyYAML>=6.0.2
REQ

cat > .env.example <<'ENV'
# Copy this file to .env and add your key.
# Do not commit .env to GitHub.

OPENAI_API_KEY=your_api_key_here

# Default model used by the agent runner.
OPENAI_MODEL=gpt-5.5
ENV

cat > .gitignore <<'GIT'
# Python
__pycache__/
*.pyc
.venv/
venv/

# Environment / secrets
.env

# Logs
logs/
*.log

# OS/editor junk
.DS_Store
Thumbs.db
.vscode/
.idea/
GIT

cat > config/agent_map.yaml <<'YAML'
agents:
  strategist:
    agent_file: agents/strategist.md
    output_file: strategy-pack.md
    required_inputs:
      - intake.md

  builder:
    agent_file: agents/builder.md
    output_file: draft-output.md
    required_inputs:
      - intake.md
      - strategy-pack.md

  qa-auditor:
    agent_file: agents/qa-auditor.md
    output_file: qa-report.md
    required_inputs:
      - intake.md
      - strategy-pack.md
      - draft-output.md

  operator:
    agent_file: agents/operator-chief-of-staff.md
    output_file: approval-pack.md
    required_inputs:
      - intake.md
      - strategy-pack.md
      - draft-output.md
      - qa-report.md
YAML

cat > scripts/agent_runner.py <<'PY'
#!/usr/bin/env python3

"""
KevOS Agent Bench - Agent Runner v0.1

Usage examples:

    python scripts/agent_runner.py 001-attention-debt strategist
    python scripts/agent_runner.py 001-attention-debt builder
    python scripts/agent_runner.py 001-attention-debt qa-auditor
    python scripts/agent_runner.py 001-attention-debt operator

Dry run, no API call:

    python scripts/agent_runner.py 001-attention-debt strategist --dry-run

The runner:
1. Reads the selected agent definition from /agents
2. Reads required run inputs from /runs/<run-id>
3. Sends the work packet to the model
4. Writes the output back to /runs/<run-id>
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime

import yaml
from dotenv import load_dotenv


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / "config" / "agent_map.yaml"


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def load_config() -> dict:
    return yaml.safe_load(read_text(CONFIG_PATH))


def build_input_packet(run_id: str, agent_name: str, config: dict) -> tuple[str, Path]:
    agents = config.get("agents", {})

    if agent_name not in agents:
        available = ", ".join(sorted(agents.keys()))
        raise ValueError(f"Unknown agent '{agent_name}'. Available agents: {available}")

    agent_config = agents[agent_name]

    agent_file = REPO_ROOT / agent_config["agent_file"]
    run_dir = REPO_ROOT / "runs" / run_id
    output_path = run_dir / agent_config["output_file"]

    if not run_dir.exists():
        raise FileNotFoundError(f"Run folder does not exist: {run_dir}")

    agent_definition = read_text(agent_file)

    input_sections = []
    for input_file in agent_config.get("required_inputs", []):
        input_path = run_dir / input_file
        input_content = read_text(input_path)
        input_sections.append(
            f"\n\n---\n\n# Input file: {input_file}\n\n{input_content}"
        )

    packet = f"""
You are running as part of the KevOS Agent Bench.

Your agent definition is below.

--- AGENT DEFINITION START ---

{agent_definition}

--- AGENT DEFINITION END ---

You will now receive the run inputs.

Your task:
- Follow your agent definition.
- Use only the supplied inputs unless you clearly flag that more research is needed.
- Produce the standard output format defined in your agent file.
- Be practical, grounded, and useful.
- Do not include fake citations or invented source details.
- If evidence is missing, say so clearly.
- Write in Markdown.

--- RUN INPUTS START ---
{''.join(input_sections)}
--- RUN INPUTS END ---
""".strip()

    return packet, output_path


def call_openai(prompt: str, model: str) -> str:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError(
            "OpenAI package is not installed. Run: pip install -r requirements.txt"
        ) from exc

    client = OpenAI()

    response = client.responses.create(
        model=model,
        input=prompt,
    )

    return response.output_text


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a KevOS agent against a work packet.")
    parser.add_argument("run_id", help="Run folder ID, e.g. 001-attention-debt")
    parser.add_argument("agent", help="Agent name, e.g. strategist, builder, qa-auditor, operator")
    parser.add_argument("--dry-run", action="store_true", help="Build prompt but do not call API")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite output file if it already exists")
    parser.add_argument("--model", default=None, help="Override model name")

    args = parser.parse_args()

    load_dotenv(REPO_ROOT / ".env")

    config = load_config()
    prompt, output_path = build_input_packet(args.run_id, args.agent, config)

    if output_path.exists() and not args.overwrite and not args.dry_run:
        print(f"Output already exists: {output_path}")
        print("Use --overwrite if you want to replace it.")
        return 1

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    logs_dir = REPO_ROOT / "logs"
    logs_dir.mkdir(exist_ok=True)

    prompt_log = logs_dir / f"{timestamp}-{args.run_id}-{args.agent}-prompt.md"
    write_text(prompt_log, prompt)

    if args.dry_run:
        print("Dry run complete. Prompt written to:")
        print(prompt_log)
        print("\nOutput would be written to:")
        print(output_path)
        return 0

    model = args.model or os.environ.get("OPENAI_MODEL", "gpt-5.5")

    if not os.environ.get("OPENAI_API_KEY"):
        print("Missing OPENAI_API_KEY.")
        print("Create a .env file from .env.example, or set the environment variable.")
        return 1

    print(f"Running agent '{args.agent}' on run '{args.run_id}' using model '{model}'...")
    result = call_openai(prompt, model)

    header = f"<!-- Generated by KevOS Agent Bench on {datetime.now().isoformat(timespec='seconds')} -->\n\n"
    write_text(output_path, header + result)

    print("Done. Output written to:")
    print(output_path)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
PY

cat > scripts/create_run.py <<'PY'
#!/usr/bin/env python3

"""
Create a new KevOS Agent Bench run folder.

Example:

    python scripts/create_run.py 002-job-ad-analysis
"""

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
PY

cat > RUNNER.md <<'MD'
# KevOS Agent Runner

This repo now has a basic programmatic agent runner.

The first goal is simple:

> Given a run folder and an agent name, read the relevant inputs and generate the next output file.

## Setup

From the repo root:

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env
