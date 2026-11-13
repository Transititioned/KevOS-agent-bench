# KevOS Book Harness Python Contract

This is the backend contract for the Gradio UI and other Python clients. Import from `scripts.kevos_book_harness` (or add the repository root to `sys.path`). It does not depend on Gradio.

## Operations

### `list_capabilities() -> list[dict]`
Returns configured capability IDs, names and descriptions. Current workflow capabilities are `research`, `adversarial_review`, and `editorial_enrichment`.

Example:

```python
[{"id": "research", "name": "Research", "description": "..."}]
```

### `run_capability(capability, context, *, run_id=None, model=None) -> dict`
Runs one capability. `capability` is an ID from `list_capabilities()`. `context` is a mapping containing `material` (required for the first stage), optional `topic`, prior-stage `artifacts` and optional `research_queries`. `run_id` is an optional filesystem-safe identifier; generated otherwise. `model` overrides `OPENAI_MODEL`.

Returns `{"run_id": str, "capability": str, "artifact": {"path": str, "content": str}, "metadata": dict}`. Outputs are Markdown files under `runs/<run_id>/kevos-book/`. Editorial enrichment receives both the research dossier and adversarial review so citations and evidence remain available. Research uses OpenAI Responses API web search when configured, and its output records URLs and distinguishes verified claims from hypotheses.

### `get_artifact(run_id, artifact_name) -> dict`
Reads an existing artifact for that run. `artifact_name` is the capability ID or its Markdown filename. Returns `{"run_id": str, "artifact": {"path": str, "content": str}}`.

### `save_feedback(run_id, feedback, *, artifact_name=None) -> dict`
Appends human feedback to `runs/<run_id>/kevos-book/feedback.md`; feedback may be a string or JSON-serializable mapping. Returns `{"run_id": str, "path": str, "saved": True}`.

### `run_book_mission(material, *, topic=None, run_id=None, model=None, research_queries=None) -> dict`
Runs Research → Adversarial Review → Editorial Enrichment sequentially using the same hooks. `material` is the existing book section as text. Returns `{"run_id": str, "artifacts": {<capability>: {"path": str, "content": str}}, "status": "complete"}`. Original material is read only and is never overwritten.

## Errors

Invalid capability/name, missing run/artifact, unsafe run ID, missing material, unavailable OpenAI package, missing `OPENAI_API_KEY`, API/search failure, and filesystem failures raise descriptive `ValueError`, `FileNotFoundError`, or `RuntimeError`. A failed stage raises; earlier saved artifacts remain available for resume or inspection. No credentials are returned in results.

## Configuration

Install `requirements.txt`; copy `.env.example` to `.env`, set `OPENAI_API_KEY`, and optionally set `OPENAI_MODEL` (default `gpt-5.5`). Research requires a Responses API model/account with web search available. Configuration stays in environment variables; never put manuscript text or credentials in source control.

The Responses client timeout defaults to 600 seconds (`OPENAI_TIMEOUT_SECONDS`), with automatic SDK retries disabled by default (`OPENAI_MAX_RETRIES=0`) to avoid repeating costly web-search work after an ambiguous connection failure. Each completed stage is atomically written before the next stage starts. Mission logs include stage start, completion/failure, elapsed duration and artifact path. A request failure includes its exception class and chained transport cause.

Responses API background mode is a possible future option for long research calls: it returns a response ID and requires polling until a terminal state. It can decouple generation from one long-lived request connection, but the current synchronous UI would still need polling/cancellation and recovery handling. For Zero Data Retention projects, response data is temporarily stored for roughly 10 minutes to support polling, so background mode does not remove the need to persist completed stage artifacts. The current flow remains synchronous.

## Example

```python
from scripts.kevos_book_harness import run_book_mission, get_artifact, save_feedback

result = run_book_mission(
    "Paste a section here", topic="AI governance in delivery teams"
)
review = get_artifact(result["run_id"], "adversarial_review")
save_feedback(result["run_id"], "Keep the practical checklist; qualify claim 2.",
              artifact_name="editorial_enrichment")
```
