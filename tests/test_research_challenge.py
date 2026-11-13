from __future__ import annotations

import tempfile
import unittest
from types import SimpleNamespace
from pathlib import Path
from unittest.mock import Mock, patch

from scripts import kevos_book_harness as harness
from ui import bridge


class ResearchChallengeTests(unittest.TestCase):
    def test_openai_client_uses_configured_timeout_and_retry_limit(self):
        constructor = Mock(return_value=object())
        with patch.object(harness, "load_dotenv"), patch.dict("sys.modules", {"openai": SimpleNamespace(OpenAI=constructor)}), patch.dict(
            "os.environ", {"OPENAI_API_KEY": "offline-test-key", "OPENAI_TIMEOUT_SECONDS": "123", "OPENAI_MAX_RETRIES": "2"}, clear=False
        ):
            harness._client(None)
        self.assertEqual(constructor.call_args.kwargs, {"timeout": 123.0, "max_retries": 2})

    def test_openai_request_errors_include_exception_class_and_cause(self):
        transport_error = OSError("socket closed")
        request_error = ConnectionError("Connection error")
        request_error.__cause__ = transport_error
        fake_client = type("Client", (), {
            "responses": type("Responses", (), {
                "create": staticmethod(lambda **kwargs: (_ for _ in ()).throw(request_error))
            })()
        })()
        with patch.object(harness, "_client", return_value=(fake_client, "gpt-5")):
            with self.assertRaisesRegex(RuntimeError, "ConnectionError.*OSError: socket closed"):
                harness._response("prompt")

    def test_capability_publishes_completed_artifact_before_returning(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill_path = root / "skills/editorial-enrichment/SKILL.md"
            skill_path.parent.mkdir(parents=True)
            skill_path.write_text("Editorial skill", encoding="utf-8")
            with patch.object(harness, "ROOT", root), patch.object(harness, "_response", return_value="# Saved editorial\n"):
                result = harness.run_capability("editorial_enrichment", {
                    "artifacts": {"adversarial_review": "Review", "research": "Research"},
                }, run_id="saved-stage")
            output_path = Path(result["artifact"]["path"])
            self.assertTrue(output_path.is_file())
            self.assertEqual(output_path.read_text(encoding="utf-8"), "# Saved editorial\n")
            self.assertFalse(output_path.with_suffix(".md.tmp").exists())

    def test_optional_research_disabled_still_runs_evidence_synthesis(self):
        calls = []

        def fake_run(capability, context, **kwargs):
            calls.append((capability, context))
            return {"artifact": {"content": capability, "path": "unused"}, "metadata": {}}

        with patch.object(harness, "run_capability", side_effect=fake_run):
            result = harness.run_book_mission(topic="Question")

        self.assertEqual([name for name, _ in calls], ["research", "adversarial_review", "evidence_synthesis", "editorial_enrichment"])
        self.assertNotIn("research_challenge", result["artifacts"])

    def test_enabled_adds_exactly_one_call_between_research_and_review(self):
        calls = []

        def fake_run(capability, context, **kwargs):
            calls.append((capability, context))
            return {"artifact": {"content": capability, "path": "unused"}, "metadata": {"duration_seconds": 1.2, "usage": {"total_tokens": 42}}}

        with patch.object(harness, "run_capability", side_effect=fake_run):
            result = harness.run_book_mission(topic="Question", enable_research_challenge=True)

        self.assertEqual([name for name, _ in calls], ["research", "research_challenge", "adversarial_review", "evidence_synthesis", "editorial_enrichment"])
        self.assertEqual(calls[1][1]["artifacts"], {"research": "research"})
        self.assertIn("research_challenge", calls[2][1]["artifacts"])
        self.assertIn("research_challenge", calls[3][1]["artifacts"])
        self.assertIn("research_challenge", calls[4][1]["artifacts"])
        self.assertIn("consolidated_findings", calls[4][1]["artifacts"])
        self.assertEqual(result["artifacts"]["research"]["content"], "research")
        self.assertEqual(result["challenge_metadata"]["usage"]["total_tokens"], 42)

    def test_challenge_context_is_bounded_and_unprimed(self):
        report = "## Source Ledger\n" + "\n".join(
            f"Practitioner case study https://example.org/source-{n}" for n in range(10)
        ) + "\n## Distinctive Research Findings\nThe researcher's ranked conclusion"
        context = harness._challenge_context({
            "topic": "Original question",
            "research_queries": ["direction one"],
            "artifacts": {"research": report},
        })
        self.assertEqual(context.count("https://example.org/source-"), 6)
        self.assertIn("Original question", context)
        self.assertIn("direction one", context)
        self.assertNotIn("ranked conclusion", context)
        self.assertNotIn("Distinctive Research Findings", context)

    def test_challenge_uses_one_mocked_web_response_and_returns_usage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / "skills/research-challenge/SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("Challenge skill", encoding="utf-8")
            with patch.object(harness, "ROOT", root), patch.object(harness, "_response", return_value=("## Overlooked Research Insights\nNone.", {"duration_seconds": 0.4, "usage": {"total_tokens": 12}})) as response:
                result = harness.run_capability("research_challenge", {
                    "topic": "Question",
                    "research_queries": ["angle"],
                    "artifacts": {"research": "Source https://example.org/a"},
                }, run_id="test-run")
            self.assertEqual(response.call_count, 1)
            self.assertTrue(response.call_args.kwargs["web_search"])
            self.assertTrue(response.call_args.kwargs["include_metadata"])
            self.assertNotIn("verified conclusion", response.call_args.args[0])
            self.assertEqual(result["metadata"]["usage"]["total_tokens"], 12)

    def test_challenge_failure_keeps_research_and_completes_later_stages(self):
        calls = []

        def fake_run(capability, context, **kwargs):
            calls.append(capability)
            if capability == "research_challenge":
                raise RuntimeError("offline challenge failure")
            return {"artifact": {"content": capability, "path": "unused"}, "metadata": {}}

        with patch.object(harness, "run_capability", side_effect=fake_run):
            result = harness.run_book_mission(topic="Question", enable_research_challenge=True)
        self.assertEqual(calls, ["research", "research_challenge", "adversarial_review", "evidence_synthesis", "editorial_enrichment"])
        self.assertEqual(result["artifacts"]["research"]["content"], "research")
        self.assertEqual(result["challenge_error"], "offline challenge failure")

    def test_existing_and_challenge_artifacts_load_and_download(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_dir = root / "runs" / "fixture-run" / "kevos-book"
            run_dir.mkdir(parents=True)
            for name, content in {
                "research.md": "# Research\nsource https://example.org",
                "research-challenge.md": "## Overlooked Research Insights\nA distinct clue",
                "adversarial-review.md": "# Review",
                "editorial-enrichment.md": "# Editorial",
            }.items():
                (run_dir / name).write_text(content, encoding="utf-8")
            with patch.object(bridge, "ROOT", root), patch.object(harness, "ROOT", root):
                loaded = bridge.load_previous_run("fixture-run")
                report = Path(loaded["download_path"]).read_text(encoding="utf-8")
            self.assertTrue(loaded["success"])
            self.assertIn("research_challenge", loaded["artifacts"])
            self.assertIn("A distinct clue", report)
            self.assertIn("# Research", report)

    def test_selective_reresearch_investigates_once_then_synthesizes_and_reloads(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            calls = []
            research = "# Research\n## Source Ledger\nhttps://example.org/primary\n## Claims\nClaim with caveat."
            challenge = "Decision: INVESTIGATE\nSelected finding: A contested implementation result\nResearch question: Does it replicate?\nWhy it matters: Reader relevance\nKnown limitations: Single-site evidence"
            targeted = "## Targeted Research Investigation\nNew source https://example.org/second\nContradicts the first study.\nLimited to one site."
            synthesis = "# Consolidated Findings\n## Contradictions\nThe sources disagree; both are single-site and require qualification."

            def fake_run(capability, context, **kwargs):
                calls.append((capability, context))
                content = {"research": research, "research_challenge": challenge,
                           "targeted_research": targeted, "adversarial_review": "Review with caveats",
                           "evidence_synthesis": synthesis, "editorial_enrichment": "Three directions"}[capability]
                if capability == "targeted_research":
                    self.assertIn("## Complete original research evidence", harness._context_text(context, capability))
                    self.assertIn("Single-site evidence", context["limitations"])
                if capability == "evidence_synthesis":
                    self.assertIn("Review with caveats", context["artifacts"]["adversarial_review"])
                    self.assertIn("Contradicts the first study", context["artifacts"]["targeted_research"])
                output_file = harness._config()["capabilities"][capability]["output_file"]
                path = root / "runs" / kwargs["run_id"] / "kevos-book" / output_file
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
                return {"artifact": {"content": content, "path": str(path)}, "metadata": {}}

            with patch.object(harness, "ROOT", root), patch.object(bridge, "ROOT", root), patch.object(harness, "run_capability", side_effect=fake_run):
                result = harness.run_book_mission(topic="Question", run_id="selective-run",
                    enable_research_challenge=True, enable_selective_re_research=True)
                loaded = bridge.load_previous_run("selective-run")
            self.assertEqual([name for name, _ in calls].count("targeted_research"), 1)
            self.assertIn("consolidated_findings", result["artifacts"])
            self.assertEqual(loaded["artifacts"]["consolidated_findings"]["content"], synthesis)

    def test_selective_reresearch_failure_is_reported_and_synthesis_still_runs(self):
        calls = []
        challenge = "Decision: INVESTIGATE\nSelected finding: Lead\nResearch question: Check it"

        def fake_run(capability, context, **kwargs):
            calls.append(capability)
            if capability == "research_challenge":
                return {"artifact": {"content": challenge, "path": "unused"}, "metadata": {}}
            if capability == "targeted_research":
                raise RuntimeError("targeted request failed")
            return {"artifact": {"content": capability, "path": "unused"}, "metadata": {}}

        with patch.object(harness, "run_capability", side_effect=fake_run):
            result = harness.run_book_mission(topic="Question", enable_research_challenge=True, enable_selective_re_research=True)
        self.assertIn("targeted_research", calls)
        self.assertIn("evidence_synthesis", calls)
        self.assertEqual(result["targeted_research_error"], "targeted request failed")

    def test_selective_decision_parsing_and_complete_handoff(self):
        lead = harness._challenge_lead("Decision: INVESTIGATE\nSelected finding: X\nResearch question: Y")
        self.assertEqual(lead["question"], "Y")
        self.assertIsNone(harness._challenge_lead("Decision: SKIP\nSelected finding: None\nResearch question: None"))
        long_evidence = "# Research\n" + ("evidence " * 2500) + "\n## Source Ledger\nCOMPLETE_SOURCE_URL"
        handed = harness._context_text({"artifacts": {"research": long_evidence,
            "adversarial_review": "Review"}}, "editorial_enrichment")
        self.assertIn("COMPLETE_SOURCE_URL", handed)

    def test_contrarian_extractor_does_not_fall_back_to_dossier(self):
        dossier = "# Research\nPlain text Contrarian Perspectives\nUnrelated claim"
        extracted = bridge.extract_contrarian_perspectives(dossier)
        self.assertNotIn("Unrelated claim", extracted)
        self.assertIn("could be extracted", extracted)


if __name__ == "__main__":
    unittest.main()
