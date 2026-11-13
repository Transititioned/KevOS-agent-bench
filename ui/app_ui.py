"""Gradio UI construction and event wiring for KevOS Agent Bench."""
from __future__ import annotations

from pathlib import Path
import gradio as gr

from ui.bridge import (
    extract_contrarian_perspectives,
    list_saved_runs,
    load_previous_run,
    record_user_feedback,
    run_mission_backend,
)


def build_app() -> gr.Blocks:
    """Build the KevOS Agent Bench Gradio Blocks application."""
    initial_runs = list_saved_runs()
    default_run = initial_runs[0] if initial_runs else None

    with gr.Blocks(
        title="KevOS Agent Bench",
    ) as app:

        # Header bar
        gr.HTML(
            """
            <div class="workbench-header">
                <div>
                    <h1 class="workbench-title">KevOS Agent Bench</h1>
                    <p class="workbench-subtitle">AI Book Research & Adversarial Critique Workbench</p>
                </div>
                <div>
                    <span class="workbench-badge">Runner: Local &bull; Workflow: Optional 4-Stage Sequential</span>
                </div>
            </div>
            """
        )

        # Status notification banner
        status_banner = gr.HTML(
            value='<div class="status-box status-idle">Ready. Enter a research topic to begin; book section material is optional.</div>'
        )

        with gr.Row(equal_height=False):
            # LEFT COLUMN: Mission Inputs, Run Management, Feedback & Export
            with gr.Column(scale=4, min_width=360):
                with gr.Group():
                    gr.Markdown("### Research Mission")
                    topic_input = gr.Textbox(
                        label="Research Topic / Question",
                        placeholder="e.g. Attention Debt: AI-Generated Workplace Communication",
                        lines=2,
                        max_lines=4,
                        interactive=True,
                    )
                    material_input = gr.Textbox(
                        label="Book Section Material",
                        placeholder="Paste an existing section of your AI book here...",
                        lines=10,
                        max_lines=18,
                        interactive=True,
                    )
                    file_upload = gr.File(
                        label="Or Upload Manuscript Section (.md, .txt)",
                        file_types=[".md", ".txt"],
                        type="filepath",
                    )
                    directions_input = gr.Textbox(
                        label="Additional Research Directions (Optional)",
                        placeholder="Optional custom search angles or queries, one per line...",
                        lines=3,
                    )
                    mock_checkbox = gr.Checkbox(
                        label="Test Mode (Mock Data for Offline UI Evaluation)",
                        value=False,
                    )
                    challenge_checkbox = gr.Checkbox(
                        label="Enable Research Challenge",
                        value=False,
                    )
                    rerearch_checkbox = gr.Checkbox(
                        label="Enable Selective Re-Research",
                        value=False,
                        interactive=False,
                    )
                    gr.Markdown("*Enable Research Challenge first. Selective Re-Research runs at most once when Challenge finds a credible unresolved question.*")
                    run_btn = gr.Button(
                        "Run Research Mission",
                        variant="primary",
                        elem_classes=["primary-run-btn"],
                    )

                with gr.Accordion("Previous Runs", open=False):
                    run_id_input = gr.Textbox(
                        label="Run Identifier",
                        placeholder="e.g. book-20261112-...",
                        lines=1,
                    )
                    recent_runs_dropdown = gr.Dropdown(
                        label="Saved Runs on Disk",
                        choices=initial_runs,
                        value=default_run,
                    )
                    with gr.Row():
                        load_btn = gr.Button("Load Run", variant="secondary")
                        refresh_runs_btn = gr.Button("Refresh Runs", variant="secondary")

                with gr.Accordion("Feedback & Export", open=True):
                    target_artifact_select = gr.Dropdown(
                        label="Target Artifact for Feedback",
                        choices=[
                            "General / Overall Mission",
                            "Research Dossier",
                            "Research Challenge",
                            "Targeted Research Investigation",
                            "Consolidated Findings",
                            "Adversarial Review",
                            "Editorial Recommendations",
                        ],
                        value="General / Overall Mission",
                    )
                    feedback_input = gr.Textbox(
                        label="Reviewer Feedback",
                        placeholder="Enter critique, notes, or instructions for this run...",
                        lines=3,
                    )
                    save_feedback_btn = gr.Button("Save Feedback", variant="secondary")
                    download_btn = gr.DownloadButton(
                        label="Download Complete Markdown Report",
                        visible=False,
                    )

            # RIGHT COLUMN: Results Tabs
            with gr.Column(scale=7, min_width=620):
                with gr.Tabs(elem_classes=["workbench-tabs"]) as tabs:
                    with gr.TabItem("Research Dossier", id="tab_research"):
                        research_output = gr.Markdown(
                            value="*No research dossier available yet. Enter a topic on the left and click **Run Research Mission**, or load an existing run.*",
                            elem_classes=["reading-pane"],
                        )

                    with gr.TabItem("Research Challenge", id="tab_challenge"):
                        challenge_output = gr.Markdown(
                            value="*Research Challenge is optional. Enable it before running a mission to independently inspect a bounded source shortlist.*",
                            elem_classes=["reading-pane"],
                        )

                    with gr.TabItem("Selective Re-Research", id="tab_targeted_research"):
                        selected_question_output = gr.Markdown(value="*No selected investigation question.*", elem_classes=["reading-pane"])
                        targeted_output = gr.Markdown(value="*Selective Re-Research is optional and defaults off.*", elem_classes=["reading-pane"])

                    with gr.TabItem("Consolidated Findings", id="tab_consolidated"):
                        consolidated_output = gr.Markdown(value="*No consolidated findings available yet.*", elem_classes=["reading-pane"])

                    with gr.TabItem("Contrarian Perspectives", id="tab_contrarian"):
                        contrarian_output = gr.Markdown(
                            value="*No contrarian perspectives available yet. Contrarian views and practitioner disagreements will display here once research is run or loaded.*",
                            elem_classes=["reading-pane"],
                        )

                    with gr.TabItem("Adversarial Review", id="tab_review"):
                        review_output = gr.Markdown(
                            value="*No adversarial review available yet. Critical assessment and unsupported claims will display here once a mission is run or loaded.*",
                            elem_classes=["reading-pane"],
                        )

                    with gr.TabItem("Editorial Recommendations", id="tab_editorial"):
                        editorial_output = gr.Markdown(
                            value="*No editorial recommendations available yet. Proposed improvements and prioritized changes will display here once a mission is run or loaded.*",
                            elem_classes=["reading-pane"],
                        )

        # ---------------- Event Handlers ----------------

        def handle_file_upload(file_path: str | None) -> str:
            if not file_path:
                return ""
            try:
                p = Path(file_path)
                return p.read_text(encoding="utf-8", errors="replace")
            except Exception as e:
                return f"Error reading file: {e}"

        file_upload.change(
            fn=handle_file_upload,
            inputs=[file_upload],
            outputs=[material_input],
        )

        challenge_checkbox.change(fn=lambda enabled: gr.update(interactive=True) if enabled else gr.update(interactive=False, value=False),
                                  inputs=[challenge_checkbox], outputs=[rerearch_checkbox])

        def handle_recent_runs_change(selected_run: str | None) -> str:
            return selected_run or ""

        recent_runs_dropdown.change(
            fn=handle_recent_runs_change,
            inputs=[recent_runs_dropdown],
            outputs=[run_id_input],
        )

        def handle_refresh_runs():
            runs = list_saved_runs()
            sel = runs[0] if runs else None
            return gr.update(choices=runs, value=sel)

        refresh_runs_btn.click(
            fn=handle_refresh_runs,
            inputs=[],
            outputs=[recent_runs_dropdown],
        )

        def handle_run_mission(
            material: str,
            topic: str,
            directions: str,
            mock_mode: bool,
            enable_challenge: bool,
            enable_rerearch: bool,
        ):
            try:
                clean_material = (material or "").strip()
                clean_topic = (topic or "").strip()
                if not clean_material and not clean_topic:
                    return (
                        '<div class="status-box status-error">❌ <strong>Error:</strong> Enter a research topic or provide book section material to start a mission.</div>',
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                    )

                # Invoke backend
                result = run_mission_backend(
                    material=clean_material,
                    topic=topic,
                    additional_directions=directions,
                    mock_mode=mock_mode,
                    enable_research_challenge=enable_challenge,
                    enable_selective_re_research=enable_rerearch,
                )

                if not result.get("success"):
                    err_msg = result.get("error", "Unknown error")
                    status_html = f'<div class="status-box status-error">❌ <strong>Mission Failed:</strong> {err_msg}</div>'
                    return (
                        status_html,
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                    )

                run_id = result.get("run_id", "")
                artifacts = result.get("artifacts", {})
                is_mock = result.get("mock", False)
                download_path = result.get("download_path")

                research_text = artifacts.get("research", {}).get("content", "*Empty research artifact*")
                challenge_text = artifacts.get("research_challenge", {}).get("content", "*Research Challenge was not enabled for this mission.*")
                selected_question_text = "*No further investigation was warranted.*"
                if enable_rerearch:
                    selected_match = __import__("re").search(r"(?im)^Research question:\s*(.+)$", challenge_text)
                    selected_question_text = (selected_match.group(1).strip() if selected_match else result.get("re_research_skip_reason", "No further investigation was warranted."))
                targeted_text = artifacts.get("targeted_research", {}).get("content", "*" + result.get("re_research_skip_reason", "Selective Re-Research was not run.") + "*")
                consolidated_text = artifacts.get("consolidated_findings", {}).get("content", "*No consolidated findings artifact was produced.*")
                if result.get("challenge_error"):
                    challenge_text = f"**Research Challenge failed.** {result['challenge_error']}\n\nThe original research dossier was preserved; no challenge findings were produced."
                contrarian_text = extract_contrarian_perspectives(research_text)
                review_text = artifacts.get("adversarial_review", {}).get("content", "*Empty review artifact*")
                editorial_text = artifacts.get("editorial_enrichment", {}).get("content", "*Empty editorial artifact*")

                if result.get("challenge_error"):
                    status_html = (
                        f'<div class="status-box status-mock">Research and later stages completed. Research Challenge failed: '
                        f'{result.get("challenge_error")}. The original research dossier is preserved.</div>'
                    )
                elif result.get("targeted_research_error"):
                    status_html = (
                        f'<div class="status-box status-mock">Research and later stages completed, but Selective Re-Research failed: '
                        f'{result.get("targeted_research_error")}. Consolidated findings reflect the available evidence.</div>'
                    )
                elif is_mock:
                    status_html = (
                        f'<div class="status-box status-mock">⚠️ <strong>TEST MODE COMPLETED (Simulated):</strong> '
                        f'Displaying mock research & critique for UI evaluation. Run ID: <code>{run_id}</code></div>'
                    )
                else:
                    challenge_meta = result.get("challenge_metadata", {})
                    challenge_usage = challenge_meta.get("usage", {})
                    usage_bits = []
                    if challenge_meta.get("duration_seconds") is not None:
                        usage_bits.append(f"{challenge_meta['duration_seconds']}s")
                    if isinstance(challenge_usage, dict) and challenge_usage.get("total_tokens") is not None:
                        usage_bits.append(f"{challenge_usage['total_tokens']} tokens")
                    usage_text = " Research Challenge: " + ", ".join(usage_bits) + "." if usage_bits else ""
                    stages_text = (
                        "Successfully executed Research, Research Challenge, Adversarial Review, Evidence Synthesis, and Editorial Enrichment."
                        if artifacts.get("research_challenge") else
                        "Successfully executed Research, Adversarial Review, Evidence Synthesis, and Editorial Enrichment."
                    )
                    status_html = (
                        f'<div class="status-box status-success">✅ <strong>Mission Completed:</strong> '
                        f'{stages_text}{usage_text} Run ID: <code>{run_id}</code></div>'
                    )

                saved_runs = list_saved_runs()
                dl_update = (
                    gr.update(value=str(Path(download_path).resolve()), visible=True)
                    if download_path and Path(download_path).is_file()
                    else gr.update(visible=False)
                )

                return (
                    status_html,
                    research_text,
                    challenge_text,
                    contrarian_text,
                    review_text,
                    editorial_text,
                    selected_question_text,
                    targeted_text,
                    consolidated_text,
                    run_id,
                    gr.update(choices=saved_runs, value=run_id),
                    dl_update,
                )
            except Exception as exc:
                return (
                    f'<div class="status-box status-error">❌ <strong>Error:</strong> {exc}</div>',
                    gr.update(), gr.update(), gr.update(), gr.update(), gr.update(),
                    gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(),
                )

        run_btn.click(
            fn=handle_run_mission,
            inputs=[material_input, topic_input, directions_input, mock_checkbox, challenge_checkbox, rerearch_checkbox],
            outputs=[
                status_banner,
                research_output,
                challenge_output,
                contrarian_output,
                review_output,
                editorial_output,
                selected_question_output,
                targeted_output,
                consolidated_output,
                run_id_input,
                recent_runs_dropdown,
                download_btn,
            ],
            show_progress="full",
        )

        def handle_load_run(run_id: str):
            try:
                clean_id = (run_id or "").strip()
                if not clean_id:
                    return (
                        '<div class="status-box status-error">❌ <strong>Error:</strong> Please specify a Run ID to load.</div>',
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                    )

                result = load_previous_run(clean_id)
                if not result.get("success"):
                    err_msg = result.get("error", "Unknown error")
                    return (
                        f'<div class="status-box status-error">❌ <strong>Load Failed:</strong> {err_msg}</div>',
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                        gr.update(),
                    )

                artifacts = result.get("artifacts", {})
                download_path = result.get("download_path")

                research_text = artifacts.get("research", {}).get("content", "*Empty research artifact*")
                challenge_text = artifacts.get("research_challenge", {}).get("content", "*No saved Research Challenge artifact for this run.*")
                selected_question_text = "*No selected investigation question.*"
                challenge_match = __import__("re").search(r"(?im)^Research question:\s*(.+)$", challenge_text)
                if challenge_match:
                    selected_question_text = challenge_match.group(1).strip()
                targeted_text = artifacts.get("targeted_research", {}).get("content", "*No saved targeted investigation for this run.*")
                consolidated_text = artifacts.get("consolidated_findings", {}).get("content", "*No saved consolidated findings for this run.*")
                contrarian_text = extract_contrarian_perspectives(research_text)
                review_text = artifacts.get("adversarial_review", {}).get("content", "*Empty review artifact*")
                editorial_text = artifacts.get("editorial_enrichment", {}).get("content", "*Empty editorial artifact*")

                status_html = (
                    f'<div class="status-box status-success">✅ <strong>Run Loaded:</strong> '
                    f'Retrieved artifacts for Run ID <code>{clean_id}</code>.</div>'
                )

                dl_update = (
                    gr.update(value=str(Path(download_path).resolve()), visible=True)
                    if download_path and Path(download_path).is_file()
                    else gr.update(visible=False)
                )

                return (
                    status_html,
                    research_text,
                    challenge_text,
                    contrarian_text,
                    review_text,
                    editorial_text,
                    selected_question_text,
                    targeted_text,
                    consolidated_text,
                    dl_update,
                )
            except Exception as exc:
                return (
                    f'<div class="status-box status-error">❌ <strong>Load Failed:</strong> {exc}</div>',
                    gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(),
                )

        load_btn.click(
            fn=handle_load_run,
            inputs=[run_id_input],
            outputs=[
                status_banner,
                research_output,
                challenge_output,
                contrarian_output,
                review_output,
                editorial_output,
                selected_question_output,
                targeted_output,
                consolidated_output,
                download_btn,
            ],
        )

        def handle_save_feedback(run_id: str, feedback_text: str, target_artifact: str):
            try:
                clean_id = (run_id or "").strip()
                if not clean_id:
                    return (
                        '<div class="status-box status-error">❌ <strong>Error:</strong> No active Run ID. Run or load a mission before saving feedback.</div>',
                        gr.update(),
                        gr.update(),
                    )

                clean_text = (feedback_text or "").strip()
                if not clean_text:
                    return (
                        '<div class="status-box status-error">❌ <strong>Error:</strong> Feedback text cannot be empty.</div>',
                        gr.update(),
                        gr.update(),
                    )

                res = record_user_feedback(clean_id, clean_text, target_artifact)
                if not res.get("success"):
                    err_msg = res.get("error", "Unknown error")
                    return (
                        f'<div class="status-box status-error">❌ <strong>Save Feedback Failed:</strong> {err_msg}</div>',
                        gr.update(),
                        gr.update(),
                    )

                path = res.get("path", "")
                download_path = res.get("download_path")

                status_html = (
                    f'<div class="status-box status-success">✅ <strong>Feedback Saved:</strong> '
                    f'Appended to <code>{path}</code></div>'
                )

                dl_update = (
                    gr.update(value=str(Path(download_path).resolve()), visible=True)
                    if download_path and Path(download_path).is_file()
                    else gr.update()
                )

                return (
                    status_html,
                    "",  # Clear feedback text on successful save
                    dl_update,
                )
            except Exception as exc:
                return (
                    f'<div class="status-box status-error">❌ <strong>Save Feedback Failed:</strong> {exc}</div>',
                    gr.update(),
                    gr.update(),
                )

        save_feedback_btn.click(
            fn=handle_save_feedback,
            inputs=[run_id_input, feedback_input, target_artifact_select],
            outputs=[status_banner, feedback_input, download_btn],
        )

    return app
