"""UI styles and theme configuration for KevOS Agent Bench research workbench."""
from __future__ import annotations

import gradio as gr

WORKBENCH_THEME = gr.themes.Base(
    primary_hue=gr.themes.colors.slate,
    neutral_hue=gr.themes.colors.slate,
    font=[
        "-apple-system",
        "BlinkMacSystemFont",
        "Segoe UI",
        "Roboto",
        "Helvetica Neue",
        "Arial",
        "sans-serif",
    ],
)

WORKBENCH_CSS = """
/* Reset & Workbench Layout */
.gradio-container {
    max-width: 1440px !important;
    margin: 0 auto !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
    color: #0f172a !important;
}

/* Header */
.workbench-header {
    padding: 0.75rem 1rem;
    margin-bottom: 0.75rem;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.workbench-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #0f172a;
    letter-spacing: -0.02em;
    margin: 0;
}

.workbench-subtitle {
    font-size: 0.85rem;
    color: #64748b;
    margin: 0.15rem 0 0 0;
}

.workbench-badge {
    font-size: 0.75rem;
    font-weight: 500;
    background: #e2e8f0;
    color: #334155;
    padding: 0.25rem 0.6rem;
    border-radius: 4px;
    letter-spacing: 0.02em;
}

/* Tab Navigation Styling */
.tab-nav {
    border-bottom: 1px solid #e2e8f0 !important;
    display: flex !important;
    flex-wrap: nowrap !important;
    gap: 2px !important;
}

.tab-nav button {
    padding: 0.45rem 0.75rem !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    color: #475569 !important;
    border-radius: 6px 6px 0 0 !important;
    white-space: nowrap !important;
    letter-spacing: -0.01em !important;
}

.tab-nav button.selected {
    color: #0f172a !important;
    font-weight: 600 !important;
    border-bottom: 2px solid #1e3a5f !important;
    background: #f8fafc !important;
}

/* Status Notifications */
.status-box {
    padding: 0.75rem 1rem;
    border-radius: 6px;
    margin-bottom: 0.75rem;
    font-size: 0.875rem;
    line-height: 1.5;
}

.status-idle {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    color: #475569;
}

.status-running {
    background: #eff6ff;
    border: 1px solid #93c5fd;
    color: #1e40af;
}

.status-success {
    background: #f0fdf4;
    border: 1px solid #86efac;
    color: #166534;
}

.status-error {
    background: #fef2f2;
    border: 1px solid #fca5a5;
    color: #991b1b;
}

.status-mock {
    background: #fffbeb;
    border: 1px solid #fcd34d;
    color: #92400e;
}

/* Long-form Reading Pane */
.reading-pane {
    max-height: 72vh !important;
    overflow-y: auto !important;
    padding: 1.25rem 1.75rem !important;
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 0 0 6px 6px !important;
    line-height: 1.7 !important;
    font-size: 15px !important;
    color: #1e293b !important;
}

.reading-pane h1 {
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    margin-top: 1.25rem !important;
    margin-bottom: 0.75rem !important;
    padding-bottom: 0.4rem !important;
    border-bottom: 1px solid #e2e8f0 !important;
    color: #0f172a !important;
}

.reading-pane h2 {
    font-size: 1.25rem !important;
    font-weight: 600 !important;
    margin-top: 1.25rem !important;
    margin-bottom: 0.6rem !important;
    padding-bottom: 0.3rem !important;
    border-bottom: 1px solid #f1f5f9 !important;
    color: #1e293b !important;
}

.reading-pane h3 {
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    margin-top: 1rem !important;
    margin-bottom: 0.4rem !important;
    color: #334155 !important;
}

.reading-pane p {
    margin-bottom: 0.85rem !important;
}

.reading-pane ul, .reading-pane ol {
    margin-bottom: 0.85rem !important;
    padding-left: 1.5rem !important;
}

.reading-pane li {
    margin-bottom: 0.35rem !important;
}

.reading-pane a {
    color: #1d4ed8 !important;
    text-decoration: underline !important;
    text-underline-offset: 2px !important;
    font-weight: 500 !important;
}

.reading-pane a:hover {
    color: #1e40af !important;
}

.reading-pane blockquote {
    border-left: 3px solid #94a3b8 !important;
    background: #f8fafc !important;
    padding: 0.6rem 1rem !important;
    margin: 0.85rem 0 !important;
    color: #334155 !important;
    font-style: italic !important;
}

.reading-pane table {
    width: 100% !important;
    border-collapse: collapse !important;
    margin: 1rem 0 !important;
    font-size: 0.875rem !important;
}

.reading-pane th {
    background: #f1f5f9 !important;
    color: #0f172a !important;
    font-weight: 600 !important;
    text-align: left !important;
    padding: 8px 12px !important;
    border: 1px solid #cbd5e1 !important;
}

.reading-pane td {
    padding: 8px 12px !important;
    border: 1px solid #e2e8f0 !important;
}

.reading-pane tr:nth-child(even) td {
    background: #f8fafc !important;
}

.reading-pane code {
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
    background: #f1f5f9 !important;
    color: #0f172a !important;
    padding: 0.15rem 0.35rem !important;
    border-radius: 4px !important;
    font-size: 0.875em !important;
}

/* Compact Controls */
.compact-accordion .label-wrap {
    font-weight: 600;
    font-size: 0.9rem;
}

button.primary-run-btn {
    background-color: #1e3a5f !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    border: none !important;
}

button.primary-run-btn:hover {
    background-color: #2d5282 !important;
}
"""
