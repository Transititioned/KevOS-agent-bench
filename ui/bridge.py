"""Backend bridge for KevOS Agent Bench.
Integrates directly with scripts.kevos_book_harness.
"""
from __future__ import annotations

import os
import re
import sys
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Ensure repository root is on sys.path
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.kevos_book_harness import (
    ROOT,
    get_artifact,
    list_capabilities,
    run_book_mission,
    save_feedback,
)

# Concurrency lock to prevent accidental duplicate paid API requests
_MISSION_LOCK = threading.Lock()


def is_mission_busy() -> bool:
    """Return True if a mission is currently executing."""
    return _MISSION_LOCK.locked()


def get_available_capabilities() -> list[dict[str, str]]:
    """Return configured capability list from backend."""
    try:
        return list_capabilities()
    except Exception:
        return []


def list_saved_runs() -> list[str]:
    """Scan runs directory for existing kevos-book runs, sorted newest first."""
    runs_dir = ROOT / "runs"
    if not runs_dir.is_dir():
        return []
    
    found: list[tuple[float, str]] = []
    for item in runs_dir.iterdir():
        if item.is_dir():
            kevos_dir = item / "kevos-book"
            if kevos_dir.is_dir():
                # Check if it has any markdown artifacts
                md_files = list(kevos_dir.glob("*.md"))
                if md_files:
                    mtime = max(f.stat().st_mtime for f in md_files)
                    found.append((mtime, item.name))
    
    found.sort(key=lambda x: x[0], reverse=True)
    return [name for _, name in found]


def extract_contrarian_perspectives(research_content: str) -> str:
    """Extract contrarian perspectives / practitioner disagreements section from research artifact.
    If not separately sectioned, returns the full research artifact as specified by the contract.
    """
    if not research_content or not research_content.strip():
        return ""

    lines = research_content.splitlines()
    target_start = None
    target_level = None

    for idx, line in enumerate(lines):
        m = re.match(r"^(#{1,4})\s+(.*)$", line.strip())
        if m:
            level = len(m.group(1))
            heading_text = m.group(2).lower()
            if any(term in heading_text for term in [
                "counterargument", "contrarian", "opposing", "disagreement", 
                "edge case", "practitioner viewpoint", "practitioner perspective"
            ]):
                target_start = idx
                target_level = level
                break

    if target_start is not None and target_level is not None:
        extracted = [lines[target_start]]
        for line in lines[target_start + 1:]:
            m = re.match(r"^(#{1,4})\s+(.*)$", line.strip())
            if m and len(m.group(1)) <= target_level:
                break
            extracted.append(line)
        section_text = "\n".join(extracted).strip()
        return (
            "> *Source: Extracted directly from Research Dossier (`research.md`).*\n\n"
            + section_text
        )

    # When not separately available as an isolated section, display the appropriate existing artifact
    return (
        "> *Source: Complete Research Dossier (`research.md`). Contrarian perspectives, edge cases, "
        "and practitioner disagreements are documented within the findings below.*\n\n"
        + research_content
    )


def generate_consolidated_report(run_id: str, artifacts: dict[str, Any], topic: str | None = None) -> str:
    """Combine run artifacts into a single downloadable markdown file in the run directory."""
    run_dir = ROOT / "runs" / run_id / "kevos-book"
    run_dir.mkdir(parents=True, exist_ok=True)
    report_path = run_dir / "full-mission-report.md"

    research_text = artifacts.get("research", {}).get("content", "")
    contrarian_text = extract_contrarian_perspectives(research_text)
    review_text = artifacts.get("adversarial_review", {}).get("content", "")
    editorial_text = artifacts.get("editorial_enrichment", {}).get("content", "")

    feedback_text = ""
    feedback_file = run_dir / "feedback.md"
    if feedback_file.is_file():
        try:
            feedback_text = feedback_file.read_text(encoding="utf-8")
        except Exception:
            feedback_text = ""

    parts = [
        f"# KevOS Agent Bench — Research Mission Report",
        f"\n- **Run ID:** `{run_id}`",
        f"- **Topic:** {topic or 'AI Book Research Section'}",
        f"- **Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        "\n---\n",
        "## 1. Research Dossier\n",
        research_text or "*No research dossier content.*",
        "\n---\n",
        "## 2. Contrarian Perspectives & Practitioner Texture\n",
        contrarian_text or "*No contrarian perspectives content.*",
        "\n---\n",
        "## 3. Adversarial Review\n",
        review_text or "*No adversarial review content.*",
        "\n---\n",
        "## 4. Editorial Recommendations\n",
        editorial_text or "*No editorial recommendations content.*",
    ]

    if feedback_text.strip():
        parts.extend([
            "\n---\n",
            "## 5. Reviewer Feedback Log\n",
            feedback_text.strip(),
        ])

    full_content = "\n".join(parts) + "\n"
    report_path.write_text(full_content, encoding="utf-8")
    return str(report_path)


def run_mission_backend(
    material: str,
    topic: str | None = None,
    additional_directions: str | None = None,
    mock_mode: bool = False,
) -> dict[str, Any]:
    """Execute research mission using backend hooks or test mock mode."""
    # Check concurrency lock
    if not _MISSION_LOCK.acquire(blocking=False):
        return {
            "success": False,
            "error": "A research mission is already in progress. Please wait for it to complete to prevent duplicate paid requests.",
            "run_id": None,
            "mock": False,
        }

    try:
        clean_material = (material or "").strip()
        if not clean_material:
            return {
                "success": False,
                "error": "Book section material is required. Please paste your section or upload a .md/.txt file.",
                "run_id": None,
                "mock": False,
            }

        # Parse research queries if provided
        queries = None
        if additional_directions and additional_directions.strip():
            queries = [q.strip() for q in additional_directions.splitlines() if q.strip()]

        clean_topic = (topic or "").strip() or "AI book section"

        if mock_mode:
            # Simulated offline test execution for UI evaluation
            return _run_mock_mission(clean_material, clean_topic, queries)

        # Real backend invocation
        result = run_book_mission(
            material=clean_material,
            topic=clean_topic,
            research_queries=queries,
        )

        run_id = result.get("run_id", "")
        artifacts = result.get("artifacts", {})

        # Prepare consolidated markdown download file
        download_path = generate_consolidated_report(run_id, artifacts, topic=clean_topic)

        return {
            "success": True,
            "run_id": run_id,
            "artifacts": artifacts,
            "download_path": download_path,
            "status": "complete",
            "mock": False,
        }

    except Exception as exc:
        return {
            "success": False,
            "error": str(exc),
            "run_id": None,
            "mock": False,
        }
    finally:
        _MISSION_LOCK.release()


def load_previous_run(run_id: str) -> dict[str, Any]:
    """Load artifacts from an existing run ID using get_artifact."""
    clean_id = (run_id or "").strip()
    if not clean_id:
        return {"success": False, "error": "Please specify a valid Run ID."}

    artifacts: dict[str, Any] = {}
    errors: list[str] = []

    for cap_id, filename in [
        ("research", "research.md"),
        ("adversarial_review", "adversarial-review.md"),
        ("editorial_enrichment", "editorial-enrichment.md"),
    ]:
        try:
            art = get_artifact(clean_id, cap_id)
            artifacts[cap_id] = art.get("artifact", {})
        except Exception as exc:
            errors.append(f"{cap_id}: {exc}")

    if not artifacts:
        return {
            "success": False,
            "error": f"Could not load artifacts for run '{clean_id}': {'; '.join(errors)}",
        }

    # Generate or locate consolidated report
    download_path = generate_consolidated_report(clean_id, artifacts)

    return {
        "success": True,
        "run_id": clean_id,
        "artifacts": artifacts,
        "download_path": download_path,
    }


def record_user_feedback(run_id: str, feedback: str, target_artifact: str | None = None) -> dict[str, Any]:
    """Save user feedback using backend save_feedback hook."""
    clean_id = (run_id or "").strip()
    if not clean_id:
        return {"success": False, "error": "No active Run ID. Run or load a mission before saving feedback."}

    clean_feedback = (feedback or "").strip()
    if not clean_feedback:
        return {"success": False, "error": "Feedback text cannot be empty."}

    # Map target artifact display name to canonical capability / artifact name
    mapping = {
        "Research Dossier": "research",
        "Adversarial Review": "adversarial_review",
        "Editorial Recommendations": "editorial_enrichment",
        "General / Overall Mission": None,
    }
    canonical_target = mapping.get(target_artifact, target_artifact) if target_artifact else None

    try:
        res = save_feedback(clean_id, clean_feedback, artifact_name=canonical_target)
        # Update consolidated report with new feedback
        load_res = load_previous_run(clean_id)
        download_path = load_res.get("download_path") if load_res.get("success") else None
        return {
            "success": True,
            "run_id": clean_id,
            "path": res.get("path"),
            "download_path": download_path,
        }
    except Exception as exc:
        return {"success": False, "error": str(exc)}


def _run_mock_mission(material: str, topic: str, queries: list[str] | None) -> dict[str, Any]:
    """Simulate a test mission for offline UI verification without making live API calls."""
    run_id = f"book-mock-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"
    run_dir = ROOT / "runs" / run_id / "kevos-book"
    run_dir.mkdir(parents=True, exist_ok=True)

    disclaimer = (
        "> ⚠️ **MOCK / TEST DATA**: This run was executed in Test Mode for UI evaluation. "
        "No live API requests were made.\n\n"
    )

    research_content = disclaimer + f"""# Research Brief: {topic}

## Source Ledger

| Title | Publisher / Source | Date | URL | Key Contribution & Limitations |
|---|---|---|---|---|
| Attention Debt in High-Velocity Teams | ACM Queue / Practitioner Case Study | 2025-09-14 | [https://queue.acm.org/detail.cfm?id=3691234](https://queue.acm.org/detail.cfm?id=3691234) | Documents that asynchronous AI summary generation increased unread notification backlogs by 38% across 14 delivery teams. Observational sample only. |
| The Cost of AI Communication Polish | Harvard Business Review Insight | 2025-11-02 | [https://hbr.org/2025/11/ai-communication-paradox](https://hbr.org/2025/11/ai-communication-paradox) | Shows recipients spend 2.4x longer parsing politely padded AI emails than concise direct bullet points. Field survey (n=1,240). |
| La surcharge informationnelle à l'ère de l'IA | Revue Gestion & Organisation | 2025-10-18 | [https://gestion-organisation.fr/etudes/surcharge-ia](https://gestion-organisation.fr/etudes/surcharge-ia) | French enterprise study examining how automated executive summaries reduce context retention among project steering committees. |
| Deuda de Atención en Gestión de Proyectos | Project Management Latino | 2025-08-22 | [https://pmlatino.org/articulos/deuda-atencion-ia](https://pmlatino.org/articulos/deuda-atencion-ia) | Practical field guidance on implementing pre-send checklists for AI-drafted sprint retrospectives. |

## Verified Claims

1. **Lower creation cost shifts bottlenecks to reception:** AI tools have reduced drafting time for routine operational updates by 60–80%, but reading and decision latency has remained constant or increased. ([ACM Queue](https://queue.acm.org/detail.cfm?id=3691234), [HBR Insight](https://hbr.org/2025/11/ai-communication-paradox))
2. **Padded clarity creates cognitive drag:** Synthetic politeness and explanatory padding added by generic LLM prompts actively degrade message skimmability. ([HBR Insight](https://hbr.org/2025/11/ai-communication-paradox))

## Counterarguments and Practitioner Viewpoints

- **The 'Context Richness' Objection:** Senior engineering leads frequently note that concise bullet points lack critical risk nuance; terse summaries have led to misunderstood architectural trade-offs.
- **Filtering Asymmetry:** While individual communicators may adopt message subtraction, organizational reward structures still incentivize visible output and broadcast volume.
- **Multilingual Disagreements:** International practitioners highlight that direct subtraction principles fail in high-context business cultures (e.g. Japan, France, Latin America), where formal framing is essential for governance legitimacy.

## Unsupported Claims in Supplied Manuscript

- The claim that *"all communication volume directly degrades project velocity"* is an overgeneralization; low-friction synchronization channels actually prevent blocking dependencies in distributed teams.

## Research Gaps

- Longitudinal data on whether automated message filtering systems reduce or merely redirect cognitive debt.
- Quantitative benchmarks for cross-functional project management communication budgets.
"""

    adversarial_content = disclaimer + f"""# Adversarial Review: {topic}

## Sceptical Assessment & Risk Audit

| Dimension | Rating (1-5) | Critique & Sceptical Challenge |
|---|:---:|---|
| Argument Rigor | 3 | The central premise equates "communication volume" with "attention debt" without defining threshold limits or acceptable coordination overhead. |
| Evidence Robustness | 3 | Heavy reliance on observational case studies; lacks randomized operational trials showing measurable delivery improvements from subtraction alone. |
| Practitioner Reality | 4 | Strong resonance for delivery leads, but ignores enterprise compliance and audit obligations that require paper trails. |
| Reputational Risk | 4 | Low risk of backlash if framed as operating discipline rather than anti-AI sentiment. |

## Sceptical Challenges & Edge Cases

1. **The Regulatory / Audit Trap:** In regulated financial services and health technology delivery, "message subtraction" risks omitting legally required disclosures or compliance trail documentation.
2. **False Equivalence with Technical Debt:** Technical debt eventually halts releases; attention debt is diffuse, often absorbed silently through personal overtime, making governance enforcement difficult.
3. **The 'Missing Context' Failure Mode:** Aggressive subtraction by junior project managers can obscure critical early-warning risk signals from steering committees.

## Actionable Remedies

- Introduce a clear boundary: distinguish operational coordination messages from formal compliance / audit deliverables.
- Refine the core thesis to specify: *"Reduce unnecessary cognitive burden, not essential contextual clarity."*
"""

    editorial_content = disclaimer + f"""# Editorial Recommendations: {topic}

## Prioritized Improvement Plan

### 1. Reframe Core Thesis for Precision (High Priority)
- **Target Passage:** The opening assertion regarding AI-enabled workplace communication.
- **Issue:** Currently reads as an argument for sending fewer updates unconditionally, which risks encouraging operational opacity.
- **Recommended Revision:** Clarify that the goal is *cognitive efficiency and signal-to-noise ratio*, not blanket reduction.
- **Supporting Evidence:** See [HBR Insight](https://hbr.org/2025/11/ai-communication-paradox) regarding the parsing time of padded vs direct messages.

### 2. Add Practical Checklist for Delivery Leads (Medium Priority)
- **Target Passage:** Conclusion and implementation guidance.
- **Issue:** Abstract advice ("apply discipline before sending") lacks immediate utility for busy project managers.
- **Recommended Revision:** Insert a 4-step "Pre-Flight Filter":
  1. *Who is the single decision-maker for this update?*
  2. *What action is blocked without this message?*
  3. *Has AI added synthetic politeness or preamble that can be deleted?*
  4. *Would this be faster as a data link rather than prose?*

### 3. Acknowledge Regulatory and Cultural Nuance (Medium Priority)
- **Target Passage:** Discussion on cross-functional alignment.
- **Issue:** Western-centric, informal startup bias.
- **Recommended Revision:** Add a short paragraph explicitly addressing high-context communication and compliance record-keeping.
- **Supporting Evidence:** Refer to [Revue Gestion & Organisation](https://gestion-organisation.fr/etudes/surcharge-ia).
"""

    # Write files
    (run_dir / "research.md").write_text(research_content, encoding="utf-8")
    (run_dir / "adversarial-review.md").write_text(adversarial_content, encoding="utf-8")
    (run_dir / "editorial-enrichment.md").write_text(editorial_content, encoding="utf-8")

    artifacts = {
        "research": {"path": str(run_dir / "research.md"), "content": research_content},
        "adversarial_review": {"path": str(run_dir / "adversarial-review.md"), "content": adversarial_content},
        "editorial_enrichment": {"path": str(run_dir / "editorial-enrichment.md"), "content": editorial_content},
    }

    download_path = generate_consolidated_report(run_id, artifacts, topic=topic)

    return {
        "success": True,
        "run_id": run_id,
        "artifacts": artifacts,
        "download_path": download_path,
        "status": "complete",
        "mock": True,
    }
