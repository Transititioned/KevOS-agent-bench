cat > setup-kevos-agent-bench.sh <<'EOF'
#!/usr/bin/env bash

set -e

echo "Creating KevOS Agent Bench folder structure..."

# Core docs
touch README.md
touch vision.md
touch operating-model.md
touch use-cases.md

# Agent definitions
mkdir -p agents
touch agents/researcher.md
touch agents/collator.md
touch agents/strategist.md
touch agents/planner.md
touch agents/builder.md
touch agents/qa-auditor.md
touch agents/operator-chief-of-staff.md
touch agents/voice-keeper.md

# Playbooks
mkdir -p playbooks/001-research-to-article
touch playbooks/001-research-to-article/workflow.md
touch playbooks/001-research-to-article/intake-template.md
touch playbooks/001-research-to-article/approval-pack-template.md
touch playbooks/001-research-to-article/qa-checklist.md

mkdir -p playbooks/002-job-opportunity-analysis
touch playbooks/002-job-opportunity-analysis/placeholder.md

mkdir -p playbooks/003-client-brief-to-proposal
touch playbooks/003-client-brief-to-proposal/placeholder.md

mkdir -p playbooks/004-project-kickoff-pack
touch playbooks/004-project-kickoff-pack/placeholder.md

# First article run
mkdir -p runs/001-attention-debt
touch runs/001-attention-debt/intake.md
touch runs/001-attention-debt/research-pack.md
touch runs/001-attention-debt/strategy-pack.md
touch runs/001-attention-debt/draft-output.md
touch runs/001-attention-debt/artefacts.md
touch runs/001-attention-debt/qa-report.md
touch runs/001-attention-debt/approval-pack.md

# Templates
mkdir -p templates
touch templates/work-packet-template.md
touch templates/source-ledger-template.md
touch templates/decision-log-template.md
touch templates/qa-report-template.md
touch templates/approval-pack-template.md

# Backlog
mkdir -p backlog
touch backlog/improvement-backlog.md
touch backlog/agent-ideas.md
touch backlog/automation-candidates.md

# Add basic starter content
cat > README.md <<'MD'
# KevOS Agent Bench

A reusable personal AI delivery bench for research, planning, artefact creation, QA, and professional work support.

## Purpose

This repository is a working lab for building a modular AI agent team that can support different professional workflows.

The first pilot use case is:

**Use Case 001 — Research-to-Article Pipeline**

The broader goal is to build reusable patterns for turning messy inputs into approval-ready work packets.

## Core pattern

1. Intake
2. Classify
3. Research
4. Collate
5. Strategise
6. Build
7. QA
8. Approval pack
9. Save and improve
MD

cat > vision.md <<'MD'
# Vision

Build a reusable agent bench that helps me operate at higher throughput across professional work.

This is not an article generator.

The article pipeline is the first controlled use case for testing a broader personal AI delivery system.

## Target capability

Given a messy work packet, the agent bench should help:

- research the topic
- organise the material
- identify the best angle or recommendation
- build useful artefacts
- check the quality
- prepare an approval-ready output pack
MD

cat > operating-model.md <<'MD'
# Operating Model

## Core workflow spine

1. Intake
2. Clarify / classify
3. Research / retrieve
4. Collate
5. Strategise
6. Build
7. QA
8. Approval pack
9. Save / learn

## Human-in-the-loop rule

The system supports judgement. It does not replace judgement.

Final decisions, publication, client advice, and professional positioning remain human-led.
MD

cat > use-cases.md <<'MD'
# Use Cases

## 001 — Research-to-Article Pipeline

Turn research sources, forum posts, newsletters, notes, and rough observations into:

- article ideas
- recommended angle
- evidence-backed draft
- LinkedIn post
- blog article
- reusable artefact
- QA report
- approval pack

## 002 — Job Opportunity Analysis

Analyse a job ad and produce a fit assessment, application angle, tailored resume guidance, and interview preparation pack.

## 003 — Client Brief to Proposal

Turn a messy client brief into problem framing, scope options, delivery approach, risks, assumptions, and proposal draft.

## 004 — Project Kickoff Pack

Turn early project material into a project brief, work breakdown, stakeholder map, risk list, decision log, and next-actions pack.
MD

cat > agents/researcher.md <<'MD'
# Agent: Researcher

## Purpose

Find, validate, summarise, and compare external information.

## Responsibilities

- Identify credible sources
- Summarise key findings
- Note competing views
- Flag weak or unsupported claims
- Produce source notes for downstream agents

## Output

- Source summary
- Key claims
- Evidence strength
- Gaps and uncertainties
MD

cat > agents/collator.md <<'MD'
# Agent: Collator

## Purpose

Turn messy inputs into structured working material.

## Responsibilities

- Group related material
- Remove duplication
- Preserve useful details
- Create structured packs for strategy, drafting, or planning

## Output

- Organised notes
- Theme map
- Source clusters
- Working pack
MD

cat > agents/strategist.md <<'MD'
# Agent: Strategist

## Purpose

Work out the angle, implication, positioning, and recommended move.

## Responsibilities

- Identify the strongest take
- Assess audience fit
- Clarify business relevance
- Recommend the best direction

## Output

- Recommended angle
- Rationale
- Risks
- Alternative angles
MD

cat > agents/planner.md <<'MD'
# Agent: Planner

## Purpose

Turn intent into sequence, milestones, tasks, dependencies, and next actions.

## Responsibilities

- Build work plans
- Break down tasks
- Identify dependencies
- Prepare next-step options

## Output

- Work plan
- Task list
- Sequence
- Dependencies
MD

cat > agents/builder.md <<'MD'
# Agent: Builder

## Purpose

Produce the actual artefact.

## Responsibilities

- Draft articles, posts, briefs, plans, checklists, tables, frameworks, and templates
- Follow the approved angle and source pack
- Keep outputs practical and usable

## Output

- Draft artefact
- Supporting notes
- Variant options
MD

cat > agents/qa-auditor.md <<'MD'
# Agent: QA / Auditor

## Purpose

Protect quality, accuracy, logic, source integrity, and professional credibility.

## Responsibilities

- Check claims
- Check source support
- Flag overclaiming
- Check voice and tone
- Identify missing logic
- Recommend publish / revise / reject

## Output

- QA report
- Risk flags
- Fix list
- Approval recommendation
MD

cat > agents/operator-chief-of-staff.md <<'MD'
# Agent: Operator / Chief of Staff

## Purpose

Keep the work moving and package decisions for review.

## Responsibilities

- Track actions
- Maintain decision logs
- Prepare approval packs
- Summarise status
- Identify blocked items

## Output

- Approval pack
- Decision summary
- Next actions
MD

cat > agents/voice-keeper.md <<'MD'
# Agent: Voice Keeper

## Purpose

Make sure outputs sound like me, not generic AI.

## Responsibilities

- Remove generic AI phrasing
- Keep tone practical, senior, and grounded
- Preserve clear Australian workplace style
- Avoid hype, fluff, and fake certainty

## Output

- Voice pass notes
- Revised text
- Tone risks
MD

cat > templates/approval-pack-template.md <<'MD'
# Approval Pack Template

## Recommended decision

- Approve / revise / reject:

## One-line summary

## Why this is worth doing

## Output prepared

- Main artefact:
- Supporting artefacts:
- Source ledger:
- QA report:

## Key risks

## What was checked

## Open questions

## Final approval notes
MD

cat > templates/work-packet-template.md <<'MD'
# Work Packet Template

## Work packet name

## Source material

## Desired output

## Audience

## Constraints

## Definition of done

## Notes
MD

cat > templates/source-ledger-template.md <<'MD'
# Source Ledger Template

| Claim | Source | Confidence | Notes |
|---|---|---|---|
|  |  |  |  |
MD

cat > templates/decision-log-template.md <<'MD'
# Decision Log Template

| Date | Decision | Rationale | Owner | Follow-up |
|---|---|---|---|---|
|  |  |  |  |  |
MD

cat > templates/qa-report-template.md <<'MD'
# QA Report Template

## Overall recommendation

- Approve / revise / reject:

## Checks completed

- Claims checked:
- Sources checked:
- Tone checked:
- Structure checked:
- Risk checked:

## Issues found

## Fixes recommended

## Final notes
MD

cat > playbooks/001-research-to-article/workflow.md <<'MD'
# Playbook 001 — Research-to-Article Pipeline

## Purpose

Turn source material into an approval-ready article package.

## Workflow

1. Capture seed idea
2. Research supporting and opposing evidence
3. Collate findings into a research pack
4. Select recommended angle
5. Draft LinkedIn/blog outputs
6. Build reusable artefact
7. Run QA
8. Prepare approval pack

## Outputs

- Intake
- Research pack
- Strategy pack
- Draft output
- Artefacts
- QA report
- Approval pack
MD

cat > playbooks/001-research-to-article/intake-template.md <<'MD'
# Research-to-Article Intake Template

## Seed idea

## Source material

## Initial reaction

## Possible audience

## Possible angle

## Why this may matter

## Risks / sensitivities
MD

cat > playbooks/001-research-to-article/approval-pack-template.md <<'MD'
# Research-to-Article Approval Pack

## Recommended article title

## Recommended decision

## Why this is worth publishing

## Target audience

## Main argument

## Drafts prepared

- LinkedIn post:
- Blog article:
- Supporting artefact:

## Source confidence

## QA findings

## Final approval notes
MD

cat > playbooks/001-research-to-article/qa-checklist.md <<'MD'
# Research-to-Article QA Checklist

## Content

- [ ] Clear central argument
- [ ] Useful to the target audience
- [ ] Not generic AI content
- [ ] Practical takeaway included

## Evidence

- [ ] Claims supported
- [ ] Sources credible
- [ ] Links checked
- [ ] Uncertain claims flagged

## Voice

- [ ] Sounds like Kev
- [ ] No hype
- [ ] No empty thought-leadership language
- [ ] Clear and grounded

## Approval

- [ ] Publish-ready
- [ ] Needs revision
- [ ] Reject / park
MD

cat > backlog/improvement-backlog.md <<'MD'
# Improvement Backlog

## Candidate improvements

- Add source ingestion
- Add idea scoring rubric
- Add approval pack generator
- Add QA scoring
- Add Codex task templates
MD

cat > backlog/agent-ideas.md <<'MD'
# Agent Ideas

## Current core agents

- Researcher
- Collator
- Strategist
- Planner
- Builder
- QA / Auditor
- Operator / Chief of Staff
- Voice Keeper

## Future agents

- Interview Coach
- Proposal Builder
- Risk Reviewer
- Stakeholder Mapper
- Resume Tailor
MD

cat > backlog/automation-candidates.md <<'MD'
# Automation Candidates

Only automate after the manual workflow proves useful.

## Candidates

- Create new run folder from template
- Generate approval pack from run files
- Pull RSS/newsletter sources
- Create GitHub issue for each seed idea
- Export approved article to blog draft
MD

echo "Folder structure created."

echo ""
echo "Next steps:"
echo "1. Review files: find . -maxdepth 3 -type f | sort"
echo "2. Check git status: git status"
echo "3. Commit changes:"
echo "   git add ."
echo "   git commit -m 'Create KevOS Agent Bench structure'"
echo ""
EOF