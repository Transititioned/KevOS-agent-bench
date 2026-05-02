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
