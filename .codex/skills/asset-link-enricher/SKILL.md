---
name: asset-link-enricher
description: Use when importing multiple lexical asset files (word/collocations/phrases/patterns/slang/idioms/spoken) and needing automatic relation enrichment with unresolved-tolerant reporting and repeatable quality baselines.
---

# Asset Link Enricher

## Overview
Use this skill to run the repeatable "parse -> bundle import -> auto-link -> unresolved report -> governance plan" loop for lexical assets.

Core rule: prefer source-data fixes over frontend fallbacks. If data cannot be linked, keep it unresolved and visible.

## Trigger Signals
Use this skill when any of the following appears:
- "import asserts/*.md and build links"
- "why unresolved is high"
- "re-run asset coverage baseline"
- "check skippedBlocks / unresolvedRefs by file"

## Workflow
1. Ensure assets exist under `asserts/` and include supported file types: `.md/.txt/.csv`.
2. Run the helper script (it executes rehearsal + parser diagnostics tests).
3. Read JSON summary and rank files by unresolved/skipped.
4. Read parser diagnostics and separate format issues from linking issues.
5. Read governance output (`contract / registry / patchSuggestions`) to build source-first repair plan.
6. Propose source-file fixes first (schema/refs/aliases), not UI patching.
7. Re-run and compare against previous baseline.

Encoding guardrail:
- All asset reads/writes must be explicit UTF-8.
- If parser diagnostics reports `ASSET_TEXT_MOJIBAKE_DETECTED`, stop and repair source files first.

## Commands
From repo root `d:\06-project\expo_duo`:

```powershell
powershell -ExecutionPolicy Bypass -File .\.agents\skills\asset-link-enricher\scripts\run-asset-link-enricher.ps1
```

Optional output file:

```powershell
powershell -ExecutionPolicy Bypass -File .\.agents\skills\asset-link-enricher\scripts\run-asset-link-enricher.ps1 -OutFile .\reports\asset-link-baseline.json
```

## Expected Output
The script prints and optionally saves:
- `totalFiles / totalEntries / nodesTotal / edgesTotal`
- `unresolvedRefs / pendingReview`
- `fileSummaries[]` sorted by unresolved desc
- `unresolvedTopByFile[]` (top unresolved labels by source file)
- parser diagnostics (`entries/parsed/skipped/warnings/errors`)
- governance report:
  - `contract.byFile[]` (which files fail strict source contract)
  - `registry` (canonical key inventory + duplicate key hints)
  - `patchSuggestions` (add_alias / add_ref / create_node recommendations)

## Decision Rules
- High `skippedBlocks`: fix source format/schema first.
- High `unresolvedRefs` with low skipped: improve refs/aliases/lemma normalization.
- Do not block entire import for partial unresolved.
- Do not create fake target nodes to hide unresolved.

## Common Mistakes
- Running only single-file import and assuming bundle quality is known.
- Treating unresolved as frontend rendering issue.
- Adding fallback text cleanup in learning UI instead of fixing asset source.
