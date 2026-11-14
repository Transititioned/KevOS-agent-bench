from __future__ import annotations

import tempfile
import unittest
import ast
from types import SimpleNamespace
from pathlib import Path
from unittest.mock import Mock, patch

from scripts import kevos_book_harness as harness
from ui import bridge, app_ui


class ResearchChallengeTests(unittest.TestCase):
    def test_mission_callbacks_match_declared_output_counts_on_error_paths(self):
        tree = ast.parse(Path(app_ui.__file__).read_text(encoding="utf-8"))
        declared = {}
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute) or node.func.attr != "click":
                continue
            keywords = {keyword.arg: keyword.value for keyword in node.keywords}
            fn = keywords.get("fn")
            outputs = keywords.get("outputs")
            if isinstance(fn, ast.Name) and fn.id in {"handle_load_run", "handle_run_mission"}:
                declared[fn.id] = len(outputs.elts)
        self.assertEqual(declared, {"handle_run_mission": 12, "handle_load_run": 10})
        functions = {node.name: node for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
        for name, expected in declared.items():
            with self.subTest(callback=name):
                calls = [node for node in ast.walk(functions[name]) if isinstance(node, ast.Call)
                         and isinstance(node.func, ast.Name) and node.func.id == "_error_callback_result"]
                self.assertTrue(calls)
                self.assertTrue(all(isinstance(call.args[1], ast.Constant) and call.args[1].value == expected for call in calls))
                self.assertEqual(len(app_ui._error_callback_result("<div>Load failed</div>", expected)), expected)

    def test_successful_callback_tuples_match_declared_output_counts(self):
        tree = ast.parse(Path(app_ui.__file__).read_text(encoding="utf-8"))
        for name, expected in (("handle_load_run", 10), ("handle_run_mission", 12)):
            with self.subTest(callback=name):
                function = next(node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == name)
                return_tuples = [node.value for node in ast.walk(function) if isinstance(node, ast.Return) and isinstance(node.value, ast.Tuple)]
                self.assertTrue(return_tuples)
                self.assertTrue(all(len(value.elts) == expected for value in return_tuples))

    def test_targeted_research_prompt_requests_only_focused_investigation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill_path = root / "skills/targeted-research/SKILL.md"
            skill_path.parent.mkdir(parents=True)
            skill_path.write_text("Focused investigation skill", encoding="utf-8")
            with patch.object(harness, "ROOT", root), patch.object(harness, "_response", return_value="## Targeted Research Investigation\nEvidence.") as response:
                harness.run_capability("targeted_research", {
                    "topic": "Question", "research_question": "Does it replicate?",
                    "artifacts": {"research": "Research", "research_challenge": "Challenge"},
                }, run_id="targeted-prompt")
            prompt = response.call_args.args[0]
            self.assertIn("## Targeted Research Investigation", prompt)
            self.assertNotIn("Then `## Consolidated Findings`", prompt)

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

    def test_mission_anchor_is_verbatim_and_prominent_in_every_stage(self):
        contexts = []
        research = "Research conclusion: technical tangent. https://example.org/source"
        challenge = "Decision: SKIP\nWhy it matters: No unresolved direct lead."

        def fake_run(capability, context, **kwargs):
            contexts.append((capability, context))
            content = {"research": research, "research_challenge": challenge}.get(capability, capability)
            return {"artifact": {"content": content, "path": "unused"}, "metadata": {}}

        directions = ["How does individual AI use affect authority?", "Trace impacts on cross-functional workflows."]
        with patch.object(harness, "run_capability", side_effect=fake_run):
            harness.run_book_mission(material="Chapter draft context", topic="Individual adoption versus collective capability",
                research_queries=directions, enable_research_challenge=True)

        expected_stages = {"research", "research_challenge", "adversarial_review", "evidence_synthesis", "editorial_enrichment"}
        self.assertEqual({name for name, _ in contexts}, expected_stages)
        for capability, context in contexts:
            with self.subTest(stage=capability):
                rendered = harness._context_text(context, capability)
                self.assertTrue(rendered.startswith("## MISSION ANCHOR"))
                self.assertIn("Individual adoption versus collective capability", rendered)
                for direction in directions:
                    self.assertIn(direction, rendered)
                self.assertIn("Chapter draft context", rendered)
        self.assertEqual(len({harness._mission_anchor(context) for _, context in contexts}), 1)
        challenge_context = harness._context_text(dict(contexts)["research_challenge"], "research_challenge")
        self.assertIn("https://example.org/source", challenge_context)
        self.assertNotIn("technical tangent", challenge_context)
        self.assertNotIn("Research conclusion", challenge_context)

    def test_challenge_adjacency_and_invalid_fields_safely_skip_paid_followup(self):
        cases = {
            "adjacent": ("Decision: INVESTIGATE\nSelected finding: Temporal retrieval design\nResearch question: "
                "How fresh is enterprise knowledge?\nRelevance to original mission: ADJACENT\n"
                "Expected impact on original question: This may change temporal retrieval design.\n"
                "Why it matters: The finding is useful for knowledge infrastructure.\nKnown limitations: Few cases", "ADJACENT"),
            "missing": ("Decision: INVESTIGATE\nSelected finding: A lead\nResearch question: Check it\n"
                "Why it matters: Could be useful.", "missing required field"),
            "invalid": ("Decision: INVESTIGATE\nSelected finding: A lead\nResearch question: Check it\n"
                "Relevance to original mission: MAYBE\nExpected impact on original question: Unclear.\n"
                "Why it matters: Unclear.", "must be DIRECT"),
        }
        for name, (decision, expected_reason) in cases.items():
            with self.subTest(case=name):
                lead = harness._challenge_lead(decision)
                self.assertFalse(lead["investigate"])
                self.assertIn(expected_reason.lower(), lead["skip_reason"].lower())
                calls = []

                def fake_run(capability, context, **kwargs):
                    calls.append(capability)
                    content = decision if capability == "research_challenge" else capability
                    return {"artifact": {"content": content, "path": "unused"}, "metadata": {}}

                with patch.object(harness, "run_capability", side_effect=fake_run):
                    result = harness.run_book_mission(topic="Original question", enable_research_challenge=True,
                        enable_selective_re_research=True)
                self.assertNotIn("targeted_research", calls)
                self.assertIn(expected_reason.split()[0].lower(), result["re_research_skip_reason"].lower())

    def test_saved_drift_example_fails_closed_without_new_fields(self):
        saved_selection = (Path(__file__).parent / "fixtures/research-challenge-adjacent-selection.md").read_text(encoding="utf-8")
        lead = harness._challenge_lead(saved_selection)
        self.assertFalse(lead["investigate"])
        self.assertIn("Relevance to original mission", lead["skip_reason"])

    def test_direct_finding_can_launch_targeted_research(self):
        direct = ("Decision: INVESTIGATE\nSelected finding: Data quality prevents cross-team coordination\n"
                  "Research question: Does master-data fragmentation materially affect collaboration?\n"
                  "Relevance to original mission: DIRECT\n"
                  "Expected impact on original question: It may materially change the explanation for collaboration failures.\n"
                  "Why it matters: It may materially connect individual productivity gains to collective workflow outcomes.\n"
                  "Known limitations: Evidence is case-based.")
        calls = []

        def fake_run(capability, context, **kwargs):
            calls.append((capability, context))
            return {"artifact": {"content": direct if capability == "research_challenge" else capability, "path": "unused"}, "metadata": {}}

        with patch.object(harness, "run_capability", side_effect=fake_run):
            harness.run_book_mission(topic="Individual AI adoption and collective capability",
                research_queries=["cross-functional workflows"], enable_research_challenge=True,
                enable_selective_re_research=True)
        self.assertIn("targeted_research", [name for name, _ in calls])
        target_context = next(context for name, context in calls if name == "targeted_research")
        self.assertEqual(target_context["relevance"], "DIRECT")
        self.assertIn("Individual AI adoption and collective capability",
            harness._context_text(target_context, "targeted_research"))

    def test_supporting_finding_requires_and_accepts_explicit_material_effect(self):
        fields = ("Decision: INVESTIGATE\nSelected finding: Workflow handoffs depend on shared context\n"
                  "Research question: Does the contributing condition alter team outcomes?\n"
                  "Relevance to original mission: SUPPORTING\n")
        insufficient = fields + "Expected impact on original question: It may be relevant.\nWhy it matters: Interesting evidence."
        self.assertFalse(harness._challenge_lead(insufficient)["investigate"])
        sufficient = fields + ("Expected impact on original question: This may materially change the explanation of team outcomes.\n"
            "Why it matters: This materially affects whether individual productivity becomes collective capability.\nKnown limitations: One context.")
        self.assertTrue(harness._challenge_lead(sufficient)["investigate"])

    def test_adjacent_findings_reach_synthesis_and_editorial_contexts(self):
        adjacent = "ADJACENT finding: temporal retrieval governs knowledge freshness; retain for a future chapter."
        calls = []

        def fake_run(capability, context, **kwargs):
            calls.append((capability, context))
            content = adjacent if capability == "research_challenge" else capability
            return {"artifact": {"content": content, "path": "unused"}, "metadata": {}}

        with patch.object(harness, "run_capability", side_effect=fake_run):
            harness.run_book_mission(topic="Individual adoption and collaboration", enable_research_challenge=True)
        for stage in ("evidence_synthesis", "editorial_enrichment"):
            context = next(ctx for name, ctx in calls if name == stage)
            self.assertIn(adjacent, "\n".join(context["artifacts"].values()))

    def test_composite_case_provenance_instruction_reaches_review_and_synthesis(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture = Path(__file__).parent / "fixtures/composite-case-evidence.md"
            composite = fixture.read_text(encoding="utf-8")
            for capability in ("adversarial_review", "evidence_synthesis"):
                skill_path = root / "skills" / capability.replace("_", "-") / "SKILL.md"
                skill_path.parent.mkdir(parents=True, exist_ok=True)
                actual_skill = harness.ROOT / "skills" / capability.replace("_", "-") / "SKILL.md"
                skill_path.write_text(actual_skill.read_text(encoding="utf-8"), encoding="utf-8")
            prompts = []

            def fake_response(prompt, *args, **kwargs):
                prompts.append(prompt)
                return "The composite vignette is illustrative and does not establish measured field outcomes."

            with patch.object(harness, "ROOT", root), patch.object(harness, "_response", side_effect=fake_response):
                for capability in ("adversarial_review", "evidence_synthesis"):
                    harness.run_capability(capability, {"topic": "AI adoption and collaboration", "artifacts": {
                        "research": composite, "adversarial_review": "Review", "consolidated_findings": "Synthesis",
                    }}, run_id="composite-test")
            self.assertEqual(len(prompts), 2)
            for prompt in prompts:
                self.assertIn("An explicitly composite teaching case", prompt)
                self.assertIn("independently verified deployments", prompt)
                self.assertIn("measured field outcomes", prompt)

    def test_offline_pipeline_does_not_call_response_api(self):
        def fake_run(capability, context, **kwargs):
            return {"artifact": {"content": capability, "path": "unused"}, "metadata": {}}

        with patch.object(harness, "run_capability", side_effect=fake_run), patch.object(harness, "_response") as response:
            harness.run_book_mission(topic="Offline regression", enable_research_challenge=True)
        response.assert_not_called()

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
                "research.md": """# Enterprise Transformation Research
## Contrarian perspectives
The frequently cited transformation failure rate has uncertain provenance.

Practitioners report that established frameworks can work when adapted to legacy systems, data quality and organisational capability.

## Distinctive research findings
This later section must not appear in the Contrarian tab.
""",
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
            self.assertIn("# Enterprise Transformation Research", report)
            extracted = bridge.extract_contrarian_perspectives(loaded["artifacts"]["research"]["content"])
            self.assertIn("uncertain provenance", extracted)
            self.assertIn("adapted to legacy systems", extracted)
            self.assertNotIn("This later section", extracted)
            self.assertEqual(loaded["artifacts"]["research"]["content"],
                (run_dir / "research.md").read_text(encoding="utf-8"))

    def test_selective_reresearch_investigates_once_then_synthesizes_and_reloads(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            calls = []
            research = "# Research\n## Source Ledger\nhttps://example.org/primary\n## Claims\nClaim with caveat."
            challenge = ("Decision: INVESTIGATE\nSelected finding: A contested implementation result\n"
                         "Research question: Does it materially change the original explanation?\n"
                         "Relevance to original mission: DIRECT\n"
                         "Expected impact on original question: It may materially change the explanation.\n"
                         "Why it matters: It may materially alter the original problem's causal account.\n"
                         "Known limitations: Single-site evidence")
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
            synthesis_context = next(context for name, context in calls if name == "evidence_synthesis")
            self.assertEqual(set(synthesis_context["artifacts"]), {
                "research", "research_challenge", "targeted_research", "adversarial_review"})

    def test_synthesis_receives_research_and_review_when_optional_stages_are_disabled(self):
        captured = {}

        def fake_run(capability, context, **kwargs):
            if capability == "evidence_synthesis":
                captured.update(context["artifacts"])
            return {"artifact": {"content": capability, "path": "unused"}, "metadata": {}}

        with patch.object(harness, "run_capability", side_effect=fake_run):
            harness.run_book_mission(topic="Question")
        self.assertEqual(set(captured), {"research", "adversarial_review"})

    def test_selective_reresearch_failure_is_reported_and_synthesis_still_runs(self):
        calls = []
        challenge = ("Decision: INVESTIGATE\nSelected finding: Lead\nResearch question: Check it\n"
                     "Relevance to original mission: DIRECT\nExpected impact on original question: It may change the conclusion.\n"
                     "Why it matters: It could change the original explanation.\nKnown limitations: None")

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
        lead = harness._challenge_lead("Decision: INVESTIGATE\nSelected finding: X\nResearch question: Y\n"
            "Relevance to original mission: DIRECT\nExpected impact on original question: It may change the conclusion.\n"
            "Why it matters: It challenges the existing explanation.\nKnown limitations: Limited evidence")
        self.assertEqual(lead["question"], "Y")
        self.assertFalse(harness._challenge_lead("Decision: SKIP\nSelected finding: None\nResearch question: None")["investigate"])
        long_evidence = "# Research\n" + ("evidence " * 2500) + "\n## Source Ledger\nCOMPLETE_SOURCE_URL"
        handed = harness._context_text({"artifacts": {"research": long_evidence,
            "adversarial_review": "Review"}}, "editorial_enrichment")
        self.assertIn("COMPLETE_SOURCE_URL", handed)

    def test_contrarian_extractor_does_not_fall_back_to_dossier(self):
        dossier = "# Research\nPlain text Contrarian Perspectives\nUnrelated claim"
        extracted = bridge.extract_contrarian_perspectives(dossier)
        self.assertNotIn("Unrelated claim", extracted)
        self.assertIn("could be extracted", extracted)

    def test_contrarian_extractor_accepts_standalone_plain_text_heading(self):
        dossier = """# Research
Other research findings.

Contrarian perspectives
- The 70% transformation-failure statistic is questionable.
- Established frameworks can work when adapted to the organisation's operating model.
- Some failures result from genuine legacy, data and capability constraints, not defective governance.

## Research Gaps
Do not include this later section.
"""
        extracted = bridge.extract_contrarian_perspectives(dossier)
        self.assertIn("The 70% transformation-failure statistic is questionable.", extracted)
        self.assertIn("adapted to the organisation's operating model", extracted)
        self.assertIn("genuine legacy, data and capability constraints", extracted)
        self.assertNotIn("Do not include this later section", extracted)

    def test_contrarian_extractor_still_accepts_markdown_heading(self):
        extracted = bridge.extract_contrarian_perspectives(
            "## Contrarian Perspectives\nDistinct disagreement.\n\n## Next Section\nLater content."
        )
        self.assertIn("Distinct disagreement.", extracted)
        self.assertNotIn("Later content.", extracted)

    def test_contrarian_extractor_accepts_heading_variants_and_stops_at_markdown_section(self):
        for heading in ("## Contrarian Perspectives", "Contrarian Perspectives:",
                        "**Contrarian perspectives**", "### Counterarguments and Practitioner Viewpoints",
                        "Practitioner disagreements"):
            with self.subTest(heading=heading):
                extracted = bridge.extract_contrarian_perspectives(
                    f"{heading}\nAlternative explanation: capability constraints matter.\n\n"
                    "## Distinctive research findings\nDo not include the findings."
                )
                self.assertIn("capability constraints matter", extracted)
                self.assertNotIn("Do not include", extracted)

    def test_contrarian_extractor_stops_at_plain_text_synthesis_heading(self):
        dossier = """Contrarian perspectives
The 70% transformation-failure statistic has uncertain provenance.

Established frameworks can work when adapted to legacy systems and local capability.

Short evidence-based synthesis
The mainstream conclusion remains persuasive, with implementation qualifications.

Distinctive research findings
Later research content is outside the extracted section.
"""
        extracted = bridge.extract_contrarian_perspectives(dossier)
        self.assertIn("uncertain provenance", extracted)
        self.assertIn("adapted to legacy systems", extracted)
        self.assertNotIn("The mainstream conclusion", extracted)
        self.assertNotIn("Later research content", extracted)

    def test_contrarian_heading_with_introductory_text_on_same_line(self):
        dossier = """Contrarian perspectives (genuine disagreements, failures, and limits)
Credible alternative: legacy data quality can be causal.

Distinctive research findings (prioritized evidence and implications)
This next section must be excluded.
"""
        extracted = bridge.extract_contrarian_perspectives(dossier)
        self.assertIn("genuine disagreements, failures, and limits", extracted)
        self.assertIn("legacy data quality can be causal", extracted)
        self.assertNotIn("This next section", extracted)

    def test_contrarian_extractor_fallback_is_explicit_when_section_missing(self):
        extracted = bridge.extract_contrarian_perspectives(
            "## Distinctive research findings\nMainstream finding only.\n\nShort evidence-based synthesis\nSummary."
        )
        self.assertIn("No separately headed contrarian perspectives section", extracted)
        self.assertNotIn("Mainstream finding", extracted)

    def test_contrarian_extractor_captures_complete_sections_from_two_saved_outputs(self):
        fixtures = Path(__file__).parent / "fixtures"
        # Verbatim section excerpts from two saved enterprise transformation
        # research runs; each fixture includes its next section heading.
        for filename in ("research-contrarian-enterprise-1.md", "research-contrarian-enterprise-2.md"):
            with self.subTest(fixture=filename):
                dossier = (fixtures / filename).read_text(encoding="utf-8").rstrip()
                expected_section = dossier.rsplit("\n\n", 1)[0]
                extracted = bridge.extract_contrarian_perspectives(dossier)
                section_text = extracted.split("\n\n", 1)[1]
                self.assertEqual(section_text, expected_section)
                next_heading = dossier.rsplit("\n", 1)[-1]
                self.assertNotIn(next_heading, section_text)


if __name__ == "__main__":
    unittest.main()
