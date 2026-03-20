# Autopilot Workflow

This document defines the default high-closure delivery workflow for this repo.

## Goal

Turn one user task into one complete delivery:
- requirement interpretation
- implementation
- verification
- final report

without asking the user to orchestrate intermediate steps.

## Execution Pipeline

1. Intake
- Parse user intent into functional goals and constraints.
- Extract acceptance criteria from:
  - latest user message
  - AGENTS.md rules
  - existing architecture and conventions

2. Task decomposition
- Split into non-conflicting tracks:
  - frontend/UI
  - backend/API
  - data/model
  - testing/verification
  - docs/memory
- Run independent discovery and checks in parallel.

3. Build
- Implement smallest effective change set.
- Keep UX simple for operators; hide internal-only controls by default.
- Preserve existing patterns unless redesign is explicitly requested.

4. Verify (required)
- Syntax/type check for touched code.
- Run targeted tests for affected modules.
- Run feature smoke path for the user-visible flow.
- If verification fails, patch and re-run until stable or blocked.

5. Deliver
- Provide concise result summary:
  - what changed
  - file list
  - verification commands + outcomes
  - remaining risks (if any)

## Definition of Done

A task is done only when all are true:
- acceptance criteria met
- changed code validated
- user-facing flow confirmed
- `PROJECT_MEMORY.md` updated
- `PROJECT_PROGRESS.md` updated

## Persistent Memory Rules

After each session, append to `PROJECT_MEMORY.md`:
- What changed (files + intent)
- What was learned (behavior/architecture)
- Next steps / open questions

## Notes

- This workflow is repo-level process memory, not model memory.
- It works across restarts as long as this file and `AGENTS.md` remain in the project.
