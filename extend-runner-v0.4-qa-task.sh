#!/usr/bin/env bash
set -e

echo "Extending KevOS Agent Bench runner with QA task support..."

# Safety check: must be run from repo root
if [ ! -d ".git" ]; then
  echo "ERROR: This does not look like the repo root. No .git folder found."
  echo "Run this from the KevOS-agent-bench folder, not inside .git."
  exit 1
fi

mkdir -p scripts
mkdir -p config
mkdir -p prompts
mkdir -p agents
mkdir -p runs/001-attention-debt

# Backups
timestamp=$(date +"%Y%m%d-%H%M%S")

if [ -f "scripts/agent_runner.py" ]; then
  cp "scripts/agent_runner.py" "scripts/agent_runner.py.bak-$timestamp"
  echo "Backed up scripts/agent_runner.py to scripts/agent_runner.py.bak-$timestamp"
fi

if [ -f "config/agent_map.yaml" ]; then
  cp "config/agent_map.yaml" "config/agent_map.yaml.bak-$timestamp"
  echo "Backed up config/agent_map.yaml to config/agent_map.yaml.bak-$timestamp"
fi

# Install enhanced runner
cat > scripts/agent_runner.py <<'PY'
#!/usr/bin/env python3

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


def resolve_repo_path(relative_path: str) -> Path:
    return REPO_ROOT / relative_path


def build_input_packet(run_id: str, agent_name: str, config: dict) -> tuple[str, Path, Path]:
    """
    Build the full agent task packet.

    Returns:
        packet: assembled Markdown prompt/task
        output_path: where the agent result should be written
        task_path: where the copy/paste-ready task packet should be written
    """
    agents = config.get("agents", {})

    if agent_name not in agents:
        available = ", ".join(sorted(agents.keys()))
        raise ValueError(f"Unknown agent '{agent_name}'. Available agents: {available}")

    agent_config = agents[agent_name]

    agent_file = resolve_repo_path(agent_config["agent_file"])
    prompt_file = resolve_repo_path(agent_config["prompt_file"]) if agent_config.get("prompt_file") else None

    run_dir = REPO_ROOT / "runs" / run_id
    output_path = run_dir / agent_config["output_file"]
    task_path = run_dir / agent_config.get("task_file", f"{agent_name}-task.md")

    if not run_dir.exists():
        raise FileNotFoundError(f"Run folder does not exist: {run_dir}")

    agent_definition = read_text(agent_file)

    prompt_section = ""
    if prompt_file:
        prompt_text = read_text(prompt_file)
        prompt_section = f"""

--- AGENT TASK PROMPT START ---

{prompt_text}

--- AGENT TASK PROMPT END ---
"""

    input_sections = []
    for input_file in agent_config.get("required_inputs", []):
        input_path = run_dir / input_file
        input_content = read_text(input_path)
        input_sections.append(
            f"\n\n---\n\n# Input file: {input_file}\n\n{input_content}"
        )

    packet = f"""
# KevOS Agent Bench Task Packet

## Run

- Run ID: {run_id}
- Agent: {agent_name}
- Generated: {datetime.now().isoformat(timespec='seconds')}

You are running as part of the KevOS Agent Bench.

Your agent definition is below.

--- AGENT DEFINITION START ---

{agent_definition}

--- AGENT DEFINITION END ---
{prompt_section}
You will now receive the run inputs.

## Execution rules

- Follow your agent definition.
- Follow the agent task prompt if one is supplied.
- Use only the supplied inputs unless you clearly flag that more research is needed.
- Produce the standard output format defined in your agent file or task prompt.
- Be practical, grounded, and useful.
- Do not include fake citations or invented source details.
- If evidence is missing, say so clearly.
- Write in Markdown.

--- RUN INPUTS START ---
{''.join(input_sections)}
--- RUN INPUTS END ---
""".strip()

    return packet, output_path, task_path


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


def print_available_agents(config: dict) -> None:
    print("Available agents:")
    for agent_name in sorted(config.get("agents", {}).keys()):
        print(f"- {agent_name}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a KevOS agent against a work packet.")
    parser.add_argument("run_id", nargs="?", help="Run folder ID, e.g. 001-attention-debt")
    parser.add_argument("agent", nargs="?", help="Agent name, e.g. strategist, builder, qa-auditor, operator")
    parser.add_argument("--dry-run", action="store_true", help="Build prompt but do not call API")
    parser.add_argument("--task-only", action="store_true", help="Write task packet to the run folder and do not call API")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite output file if it already exists")
    parser.add_argument("--model", default=None, help="Override model name")
    parser.add_argument("--list-agents", action="store_true", help="List configured agents and exit")

    args = parser.parse_args()

    load_dotenv(REPO_ROOT / ".env")

    config = load_config()

    if args.list_agents:
        print_available_agents(config)
        return 0

    if not args.run_id or not args.agent:
        parser.print_help()
        print("\nExamples:")
        print("  python scripts/agent_runner.py 001-attention-debt qa-auditor --task-only")
        print("  python scripts/agent_runner.py 001-attention-debt qa-auditor --dry-run")
        print("  python scripts/agent_runner.py 001-attention-debt qa-auditor --overwrite")
        print("  python scripts/agent_runner.py --list-agents")
        return 1

    prompt, output_path, task_path = build_input_packet(args.run_id, args.agent, config)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    logs_dir = REPO_ROOT / "logs"
    logs_dir.mkdir(exist_ok=True)

    prompt_log = logs_dir / f"{timestamp}-{args.run_id}-{args.agent}-prompt.md"
    write_text(prompt_log, prompt)

    # Always write the run-local task packet.
    write_text(task_path, prompt)

    if args.task_only:
        print("Task packet created. No API call made.")
        print("\nTask packet written to:")
        print(task_path)
        print("\nPrompt log written to:")
        print(prompt_log)
        print("\nExpected output path:")
        print(output_path)
        return 0

    if args.dry_run:
        print("Dry run complete. No API call made.")
        print("\nTask packet written to:")
        print(task_path)
        print("\nPrompt log written to:")
        print(prompt_log)
        print("\nOutput would be written to:")
        print(output_path)
        return 0

    if output_path.exists() and not args.overwrite:
        print(f"Output already exists: {output_path}")
        print("Use --overwrite if you want to replace it.")
        return 1

    model = args.model or os.environ.get("OPENAI_MODEL", "gpt-5.5")

    if not os.environ.get("OPENAI_API_KEY"):
        print("Missing OPENAI_API_KEY.")
        print("Create a .env file from .env.example, or set the environment variable.")
        print("\nNo API call made, but the task packet was created here:")
        print(task_path)
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

# Make runner executable for Git Bash users
chmod +x scripts/agent_runner.py

# Ensure config exists and contains qa-auditor
python - <<'PY'
from pathlib import Path
import sys

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is not installed. Run: pip install pyyaml")
    sys.exit(1)

config_path = Path("config/agent_map.yaml")

if config_path.exists():
    data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
else:
    data = {}

agents = data.setdefault("agents", {})

agents["qa-auditor"] = {
    "agent_file": "agents/qa-auditor.md",
    "prompt_file": "prompts/qa_prompt.md",
    "required_inputs": [
        "intake.md",
        "strategy-pack.md",
        "draft-output.md",
    ],
    "output_file": "qa-report.md",
    "task_file": "qa-task.md",
}

config_path.parent.mkdir(parents=True, exist_ok=True)
config_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
print("Updated config/agent_map.yaml with qa-auditor.")
PY

# Ensure qa prompt exists. Do not overwrite if user already has it.
if [ ! -f "prompts/qa_prompt.md" ]; then
  cat > prompts/qa_prompt.md <<'EOF'
# QA Prompt — Research-to-Article Package

You are the QA / Auditor agent for the KevOS Agent Bench.

Review the Builder output package for the selected run.

## Review stance

Be sceptical but useful.

Do not rewrite the article by default.

Focus on issues that materially affect:

- clarity
- credibility
- usefulness
- audience fit
- publishability
- reputational safety
- voice fit

## Checks

Review the package against these dimensions:

1. Argument clarity
2. Audience value
3. Evidence strength
4. Practical usefulness
5. Voice fit
6. AI-slop risk
7. Structure and readability
8. Artefact usefulness
9. Reputational safety
10. Approval readiness

## Output format

Produce a QA report in Markdown with:

- Recommendation
- Executive summary
- Quality scorecard
- Key strengths
- Material issues
- Claim and evidence review
- Voice and tone review
- Structure review
- Reputational risk review
- Recommended edits
- Handoff to Operator / Chief of Staff
EOF
  echo "Created prompts/qa_prompt.md"
else
  echo "prompts/qa_prompt.md already exists. Left unchanged."
fi

# Ensure qa-auditor agent exists. Do not overwrite if user already has it.
if [ ! -f "agents/qa-auditor.md" ]; then
  cat > agents/qa-auditor.md <<'EOF'
# Agent: QA / Auditor

## Purpose

Protect quality, credibility, usefulness, and professional judgement.

The QA / Auditor assesses the output, identifies risks, recommends improvements, and decides whether the work is ready for approval, revision, or rejection.

## Output contract

The QA / Auditor must produce:

1. Overall recommendation
2. Executive summary
3. Quality scorecard
4. Key strengths
5. Material issues
6. Suggested fixes
7. Claim and evidence review
8. Voice and tone review
9. Publishability recommendation
10. Final action list

## Recommendation options

Use one of:

- Publish-ready
- Minor revision
- Major revision
- Park / reject
EOF
  echo "Created agents/qa-auditor.md"
else
  echo "agents/qa-auditor.md already exists. Left unchanged."
fi

# Ensure run output placeholder exists. Do not overwrite real report.
if [ ! -f "runs/001-attention-debt/qa-report.md" ]; then
  cat > runs/001-attention-debt/qa-report.md <<'EOF'
# QA Report — Use Case 001: Attention Debt

Status: Pending QA run.
EOF
fi

echo ""
echo "Runner QA task support installed."
echo ""
echo "Try this:"
echo "  python scripts/agent_runner.py --list-agents"
echo "  python scripts/agent_runner.py 001-attention-debt qa-auditor --task-only"
echo ""
echo "This creates:"
echo "  runs/001-attention-debt/qa-task.md"
echo ""
echo "If you have OPENAI_API_KEY configured, run:"
echo "  python scripts/agent_runner.py 001-attention-debt qa-auditor --overwrite"
echo ""
echo "Then commit:"
echo "  git status"
echo "  git add ."
echo "  git commit -m \"Extend runner with QA task support\""
