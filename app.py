"""Entry point for KevOS Agent Bench Gradio Web Application.

Runs locally on Windows at http://127.0.0.1:7860.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Ensure KevOS-agent-bench root is on sys.path
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ui.app_ui import build_app
from ui.styles import WORKBENCH_CSS, WORKBENCH_THEME

app = build_app()

if __name__ == "__main__":
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        theme=WORKBENCH_THEME,
        css=WORKBENCH_CSS,
        allowed_paths=[str(ROOT.resolve()), str((ROOT / "runs").resolve())],
    )
