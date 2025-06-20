# Self-Audit Repository

This repository contains documentation that showcases a model's introspective audit, an agent roster, and a backlog of change requests. The goal is to maintain transparency and track improvements over time.

## Directory Structure
- `SELF_AUDIT.md` – Long-form narrative documenting the model's origins, governance, risks, and future roadmap.
- `AGENTS.md` – Table and vignettes describing each autonomous sub-agent.
- `CODEX_TASKS.md` – Backlog of Codex change requests using the schema below.
- `tests.sh` – Simple test script verifying word counts and task coverage.

## Codex Task Schema
Each Codex task follows this structure:

```yaml
id: CR-ABC-001
title: Short imperative phrase
priority: P0 | P1 | P2 | P3
phase: Architecture | Ops | R&D | Governance | Sustainability
category: Enhancement | Remediation | Research | Governance | Sustainability
axis: Security | Privacy | Reliability | Ethics | Sustainability | TechDebt | ProcessDebt
effort: 1 | 2 | 3 | 5 | 8 | 13 | 21
owner_hint: Agent Name
dependencies: [optional, other task ids]
rationale: |
  Free-form explanation linking to SELF_AUDIT or AGENTS insights.
steps: |
  Multi-step guidance on how to fulfil the task.
acceptance_criteria: |
  Measurable outcomes or tests proving completion.
```

## Running Tests
Run `./tests.sh` from the repository root. The script checks:
1. `SELF_AUDIT.md` has at least 5,000 words.
2. No placeholder brackets placeholders remain.
3. `AGENTS.md` lists at least eight agents.
4. `CODEX_TASKS.md` contains 20–30 tasks and coverage across all axes.

