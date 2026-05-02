#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import shutil

RUNNER_SOURCE = '#!/usr/bin/env python3\n\nfrom __future__ import annotations\n\nimport argparse\nimport os\nimport sys\nfrom pathlib import Path\nfrom datetime import datetime\n\nimport yaml\nfrom dotenv import load_dotenv\n\n\nREPO_ROOT = Path(__file__).resolve().parents[1]\nCONFIG_PATH = REPO_ROOT / "config" / "agent_map.yaml"\n\n\ndef read_text(path: Path) -> str:\n    if not path.exists():\n        raise FileNotFoundError(f"Missing file: {path}")\n    return path.read_text(encoding="utf-8")\n\n\ndef write_text(path: Path, content: str) -> None:\n    path.parent.mkdir(parents=True, exist_ok=True)\n    path.write_text(content, encoding="utf-8")\n\n\ndef load_config() -> dict:\n    return yaml.safe_load(read_text(CONFIG_PATH))\n\n\ndef repo_path(relative_path: str) -> Path:\n    return REPO_ROOT / relative_path\n\n\ndef build_input_packet(run_id: str, agent_name: str, config: dict) -> tuple[str, Path, Path]:\n    agents = config.get("agents", {})\n\n    if agent_name not in agents:\n        available = ", ".join(sorted(agents.keys()))\n        raise ValueError(f"Unknown agent \'{agent_name}\'. Available agents: {available}")\n\n    agent_config = agents[agent_name]\n\n    agent_file = repo_path(agent_config["agent_file"])\n    prompt_file = repo_path(agent_config["prompt_file"]) if agent_config.get("prompt_file") else None\n\n    run_dir = REPO_ROOT / "runs" / run_id\n    output_path = run_dir / agent_config["output_file"]\n    task_path = run_dir / agent_config.get("task_file", f"{agent_name}-task.md")\n\n    if not run_dir.exists():\n        raise FileNotFoundError(f"Run folder does not exist: {run_dir}")\n\n    agent_definition = read_text(agent_file)\n\n    prompt_section = ""\n    if prompt_file:\n        prompt_text = read_text(prompt_file)\n        prompt_section = f\'\'\'\n--- AGENT TASK PROMPT START ---\n\n{prompt_text}\n\n--- AGENT TASK PROMPT END ---\n\'\'\'\n\n    input_sections = []\n    for input_file in agent_config.get("required_inputs", []):\n        input_path = run_dir / input_file\n        input_content = read_text(input_path)\n        input_sections.append(\n            f"\\n\\n---\\n\\n# Input file: {input_file}\\n\\n{input_content}"\n        )\n\n    packet = f\'\'\'\n# KevOS Agent Bench Task Packet\n\n## Run\n\n- Run ID: {run_id}\n- Agent: {agent_name}\n- Generated: {datetime.now().isoformat(timespec=\'seconds\')}\n\nYou are running as part of the KevOS Agent Bench.\n\nYour agent definition is below.\n\n--- AGENT DEFINITION START ---\n\n{agent_definition}\n\n--- AGENT DEFINITION END ---\n{prompt_section}\nYou will now receive the run inputs.\n\n## Execution rules\n\n- Follow your agent definition.\n- Follow the agent task prompt if one is supplied.\n- Use only the supplied inputs unless you clearly flag that more research is needed.\n- Produce the standard output format defined in your agent file or task prompt.\n- Be practical, grounded, and useful.\n- Do not include fake citations or invented source details.\n- If evidence is missing, say so clearly.\n- Write in Markdown.\n\n--- RUN INPUTS START ---\n{\'\'.join(input_sections)}\n--- RUN INPUTS END ---\n\'\'\'.strip()\n\n    return packet, output_path, task_path\n\n\ndef call_openai(prompt: str, model: str) -> str:\n    try:\n        from openai import OpenAI\n    except ImportError as exc:\n        raise RuntimeError(\n            "OpenAI package is not installed. Run: pip install -r requirements.txt"\n        ) from exc\n\n    client = OpenAI()\n\n    response = client.responses.create(\n        model=model,\n        input=prompt,\n    )\n\n    return response.output_text\n\n\ndef print_available_agents(config: dict) -> None:\n    print("Available agents:")\n    for agent_name in sorted(config.get("agents", {}).keys()):\n        print(f"- {agent_name}")\n\n\ndef main() -> int:\n    parser = argparse.ArgumentParser(description="Run a KevOS agent against a work packet.")\n    parser.add_argument("run_id", nargs="?", help="Run folder ID, e.g. 001-attention-debt")\n    parser.add_argument("agent", nargs="?", help="Agent name, e.g. strategist, builder, qa-auditor, operator")\n    parser.add_argument("--dry-run", action="store_true", help="Build prompt but do not call API")\n    parser.add_argument("--task-only", action="store_true", help="Write task packet to the run folder and do not call API")\n    parser.add_argument("--overwrite", action="store_true", help="Overwrite output file if it already exists")\n    parser.add_argument("--model", default=None, help="Override model name")\n    parser.add_argument("--list-agents", action="store_true", help="List configured agents and exit")\n\n    args = parser.parse_args()\n\n    load_dotenv(REPO_ROOT / ".env")\n\n    config = load_config()\n\n    if args.list_agents:\n        print_available_agents(config)\n        return 0\n\n    if not args.run_id or not args.agent:\n        parser.print_help()\n        print("\\nExamples:")\n        print("  python scripts/agent_runner.py 001-attention-debt qa-auditor --task-only")\n        print("  python scripts/agent_runner.py 001-attention-debt qa-auditor --dry-run")\n        print("  python scripts/agent_runner.py 001-attention-debt qa-auditor --overwrite")\n        print("  python scripts/agent_runner.py --list-agents")\n        return 1\n\n    prompt, output_path, task_path = build_input_packet(args.run_id, args.agent, config)\n\n    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")\n    logs_dir = REPO_ROOT / "logs"\n    logs_dir.mkdir(exist_ok=True)\n\n    prompt_log = logs_dir / f"{timestamp}-{args.run_id}-{args.agent}-prompt.md"\n    write_text(prompt_log, prompt)\n\n    write_text(task_path, prompt)\n\n    if args.task_only:\n        print("Task packet created. No API call made.")\n        print("\\nTask packet written to:")\n        print(task_path)\n        print("\\nPrompt log written to:")\n        print(prompt_log)\n        print("\\nExpected output path:")\n        print(output_path)\n        return 0\n\n    if args.dry_run:\n        print("Dry run complete. No API call made.")\n        print("\\nTask packet written to:")\n        print(task_path)\n        print("\\nPrompt log written to:")\n        print(prompt_log)\n        print("\\nOutput would be written to:")\n        print(output_path)\n        return 0\n\n    if output_path.exists() and not args.overwrite:\n        print(f"Output already exists: {output_path}")\n        print("Use --overwrite if you want to replace it.")\n        return 1\n\n    model = args.model or os.environ.get("OPENAI_MODEL", "gpt-5.5")\n\n    if not os.environ.get("OPENAI_API_KEY"):\n        print("Missing OPENAI_API_KEY.")\n        print("Create a .env file from .env.example, or set the environment variable.")\n        print("\\nNo API call made, but the task packet was created here:")\n        print(task_path)\n        return 1\n\n    print(f"Running agent \'{args.agent}\' on run \'{args.run_id}\' using model \'{model}\'...")\n    result = call_openai(prompt, model)\n\n    header = f"<!-- Generated by KevOS Agent Bench on {datetime.now().isoformat(timespec=\'seconds\')} -->\\n\\n"\n    write_text(output_path, header + result)\n\n    print("Done. Output written to:")\n    print(output_path)\n    return 0\n\n\nif __name__ == "__main__":\n    try:\n        raise SystemExit(main())\n    except Exception as exc:\n        print(f"ERROR: {exc}", file=sys.stderr)\n        raise SystemExit(1)\n'
QA_PROMPT = '# QA Prompt — Research-to-Article Package\n\nYou are the QA / Auditor agent for the KevOS Agent Bench.\n\nReview the Builder output package for the selected run.\n\n## Review stance\n\nBe sceptical but useful.\n\nDo not rewrite the article by default.\n\nFocus on issues that materially affect clarity, credibility, usefulness, audience fit, publishability, reputational safety, and voice fit.\n\n## Checks\n\nReview the package against these dimensions:\n\n1. Argument clarity\n2. Audience value\n3. Evidence strength\n4. Practical usefulness\n5. Voice fit\n6. AI-slop risk\n7. Structure and readability\n8. Artefact usefulness\n9. Reputational safety\n10. Approval readiness\n\n## Special instructions\n\n- Treat specialist concepts as working concepts unless sources are supplied.\n- Flag unsupported factual claims.\n- Flag overclaiming.\n- Flag anything that sounds too much like generic LinkedIn content.\n- Check whether the article sounds balanced rather than anti-AI.\n- Check whether the supporting artefact is practical enough as a standalone asset.\n- Check whether the blog article should be shortened.\n- Check whether the LinkedIn post has enough bite.\n- Check whether the package is strong enough to proceed to an approval pack.\n\n## Output format\n\nProduce a QA report in Markdown with:\n\n# QA Report\n\n## Recommendation\n\nChoose one: Publish-ready, Minor revision, Major revision, Park / reject.\n\n## Executive summary\n\n## Quality scorecard\n\n| Dimension | Score / 5 | Notes |\n|---|---:|---|\n| Argument clarity |  |  |\n| Audience value |  |  |\n| Evidence strength |  |  |\n| Practicality |  |  |\n| Voice fit |  |  |\n| Reputational safety |  |  |\n| Structure and readability |  |  |\n| Distinctiveness |  |  |\n| Artefact usefulness |  |  |\n| Approval readiness |  |  |\n\n## Key strengths\n\n## Material issues\n\n| Issue | Severity | Why it matters | Suggested fix |\n|---|---|---|---|\n\n## Claim and evidence review\n\n| Claim / concept | Status | Notes |\n|---|---|---|\n\n## Voice and tone review\n\n## Structure review\n\n### LinkedIn post\n\n### Blog article\n\n### Supporting artefact\n\n## Reputational risk review\n\n## Recommended edits\n\n## Handoff to Operator / Chief of Staff\n'
QA_AGENT = '# Agent: QA / Auditor\n\n## Purpose\n\nProtect quality, credibility, usefulness, and professional judgement.\n\nThe QA / Auditor assesses the output, identifies risks, recommends improvements, and decides whether the work is ready for approval, revision, or rejection.\n\n## Core responsibilities\n\nThe QA / Auditor checks:\n\n- clarity of argument\n- audience fit\n- practical usefulness\n- source and claim support\n- tone and voice\n- reputational risk\n- AI-slop risk\n- overclaiming\n- structure and flow\n- completeness against the original work packet\n- suitability for approval\n\n## Operating principle\n\nThe QA / Auditor is deliberately sceptical but not obstructive.\n\nIt should not nitpick for the sake of it. It should focus on issues that would materially affect usefulness, credibility, clarity, or publishability.\n\n## Output contract\n\nThe QA / Auditor must produce:\n\n1. Overall recommendation\n2. Executive summary\n3. Quality scorecard\n4. Key strengths\n5. Material issues\n6. Suggested fixes\n7. Claim and evidence review\n8. Voice and tone review\n9. Publishability recommendation\n10. Final action list\n\n## Recommendation options\n\nUse one of:\n\n- Publish-ready\n- Minor revision\n- Major revision\n- Park / reject\n'
DEFAULT_CONFIG = 'agents:\n  qa-auditor:\n    agent_file: agents/qa-auditor.md\n    prompt_file: prompts/qa_prompt.md\n    required_inputs:\n    - intake.md\n    - strategy-pack.md\n    - draft-output.md\n    output_file: qa-report.md\n    task_file: qa-task.md\n'


def ensure_repo_root(root: Path) -> None:
    if not (root / ".git").exists():
        raise SystemExit(
            "ERROR: This does not look like the repo root. No .git folder found.\n"
            "Run this from C:\\Projects\\KevOS-agent-bench, not inside .git or scripts."
        )


def backup(path: Path) -> None:
    if path.exists():
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_path = path.with_name(path.name + f".bak-{stamp}")
        shutil.copy2(path, backup_path)
        print(f"Backed up {path} -> {backup_path}")


def update_config(config_path: Path) -> None:
    try:
        import yaml
    except ImportError:
        print("PyYAML not found. Writing a minimal config/agent_map.yaml with qa-auditor only.")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(DEFAULT_CONFIG, encoding="utf-8")
        return

    if config_path.exists():
        data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    else:
        data = {}

    agents = data.setdefault("agents", {})
    agents["qa-auditor"] = {
        "agent_file": "agents/qa-auditor.md",
        "prompt_file": "prompts/qa_prompt.md",
        "required_inputs": ["intake.md", "strategy-pack.md", "draft-output.md"],
        "output_file": "qa-report.md",
        "task_file": "qa-task.md",
    }

    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def main() -> int:
    root = Path.cwd()
    ensure_repo_root(root)

    print("Updating KevOS Agent Bench runner to v0.4 with QA task support...")

    scripts_dir = root / "scripts"
    prompts_dir = root / "prompts"
    agents_dir = root / "agents"
    run_dir = root / "runs" / "001-attention-debt"

    scripts_dir.mkdir(exist_ok=True)
    prompts_dir.mkdir(exist_ok=True)
    agents_dir.mkdir(exist_ok=True)
    run_dir.mkdir(parents=True, exist_ok=True)

    runner_path = scripts_dir / "agent_runner.py"
    backup(runner_path)
    runner_path.write_text(RUNNER_SOURCE, encoding="utf-8", newline="\n")
    print(f"Wrote {runner_path}")

    config_path = root / "config" / "agent_map.yaml"
    backup(config_path)
    update_config(config_path)
    print(f"Updated {config_path}")

    qa_prompt_path = prompts_dir / "qa_prompt.md"
    if not qa_prompt_path.exists():
        qa_prompt_path.write_text(QA_PROMPT, encoding="utf-8", newline="\n")
        print(f"Created {qa_prompt_path}")
    else:
        print(f"Left existing {qa_prompt_path} unchanged")

    qa_agent_path = agents_dir / "qa-auditor.md"
    if not qa_agent_path.exists():
        qa_agent_path.write_text(QA_AGENT, encoding="utf-8", newline="\n")
        print(f"Created {qa_agent_path}")
    else:
        print(f"Left existing {qa_agent_path} unchanged")

    qa_report_path = run_dir / "qa-report.md"
    if not qa_report_path.exists():
        qa_report_path.write_text("# QA Report — Use Case 001: Attention Debt\n\nStatus: Pending QA run.\n", encoding="utf-8", newline="\n")
        print(f"Created {qa_report_path}")

    print("\nDone.")
    print("\nTest commands:")
    print("  python scripts/agent_runner.py --list-agents")
    print("  python scripts/agent_runner.py 001-attention-debt qa-auditor --task-only")
    print("\nExpected output:")
    print("  runs/001-attention-debt/qa-task.md")
    print("\nCommit:")
    print("  git status")
    print("  git add .")
    print("  git commit -m \"Extend runner with QA task support\"")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
