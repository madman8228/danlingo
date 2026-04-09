---
name: isee
description: Convert user-specified text into constitution-ready rules, expand it into concrete guardrails, preview in terminal, and write to constitution files only after explicit confirmation. Use when users call isee with a phrase they want institutionalized.
---

# isee

## Overview
Use this skill to transform text explicitly provided by the user in the current request into concise, enforceable constitution rules.
Do not summarize the previous assistant reply unless the user explicitly asks for that behavior.

## Input Contract
- Read only the text the user explicitly specifies in the same isee request.
- If no explicit text is provided, ask for seed text before continuing.
- Treat user text as the source of truth.
- Expand the seed text into adjacent, practical rules without changing intent.

## Workflow
1. Capture the user-specified seed text.
2. Rewrite it into 1-3 core imperative rules.
3. Expand to 3-8 total rules by adding concrete guardrails:
- scope boundary (what to include/exclude)
- quality gate (how to check)
- anti-pattern (what to avoid)
- consistency rule (how to keep behavior stable)
4. Keep each rule concise, testable, and reusable.
5. Run script in preview mode first (no `--apply`) to show lessons and targets.
6. Ask user to confirm.
7. Only after confirmation, rerun with `--apply`.
8. Report updated files and added rules.

## Rule Expansion Heuristics
- Convert abstract goals into observable checks.
- Prefer imperative wording: "Do X", "Avoid Y", "Verify Z before merge".
- Add at most one anti-pattern rule per concern.
- Avoid duplicates with nearby constitution lines.
- Keep only high-value rules; do not add noise.

## Write Targets
Default targets auto-discovered under workspace:
- AGENTS.md (if present)
- any markdown file whose filename contains CONSTITUTION (case-insensitive)

## Command
Step 1: Preview only (default, no write)

```bash
python3 "C:/Users/Administrator/.codex/skills/isee/scripts/append_constitution_lessons.py" \
  --workspace "<workspace-path>" \
  --lesson "Rule 1" \
  --lesson "Rule 2" \
  --source-label "User-specified text"
```

Step 2: Write after user confirms

```bash
python3 "C:/Users/Administrator/.codex/skills/isee/scripts/append_constitution_lessons.py" \
  --workspace "<workspace-path>" \
  --lesson "Rule 1" \
  --lesson "Rule 2" \
  --source-label "User-specified text" \
  --apply
```

Optional:
- --section "ISee Lessons"
- --max-lessons 5
- --max-chars 90

## Output Contract
Preview stage must report:
- normalized rule list generated from user-specified text
- target files
- explicit note that no files were written

Apply stage must report:
- files updated
- rules added
- skipped reasons (for example, no constitution file found)
