# KevOS Agent Runner

This repo has a basic programmatic agent runner.

The first goal:

Given a run folder and an agent name, read the relevant inputs and generate the next output file.

## Setup

From the repo root:

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and add your OpenAI API key.

## Dry run first

```bash
python scripts/agent_runner.py 001-attention-debt strategist --dry-run
```

The prompt will be written to `/logs`.

## Run Strategist

```bash
python scripts/agent_runner.py 001-attention-debt strategist --overwrite
```

This reads:

- `agents/strategist.md`
- `runs/001-attention-debt/intake.md`

And writes:

- `runs/001-attention-debt/strategy-pack.md`

## Run Builder

```bash
python scripts/agent_runner.py 001-attention-debt builder --overwrite
```

This reads:

- `agents/builder.md`
- `runs/001-attention-debt/intake.md`
- `runs/001-attention-debt/strategy-pack.md`

And writes:

- `runs/001-attention-debt/draft-output.md`

## Create a new run

```bash
python scripts/create_run.py 002-job-opportunity-analysis
```

## Commit changes

```bash
git status
git add .
git commit -m "Add programmatic agent runner skeleton"
git push
```
