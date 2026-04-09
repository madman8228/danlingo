# Asset Repair Recommendations V1

## Scope
This document provides **source-asset repair recommendations only** for:
- `asserts/word.md`
- `asserts/collocations.md`
- `asserts/phrases.md`
- `asserts/sentencePatterns.md`
- `asserts/slang.md`
- `asserts/idioms.md`
- `asserts/spokenExpressions.md`

No runtime UI fallback changes are included.

## Baseline (2026-04-03)
From bundle rehearsal:
- files: 7
- entries: 64
- nodes: 130
- edges: 488
- unresolvedRefs: 329
- pendingReview: 51

Highest risk files:
1. `word.md` (`unresolved=358`, `skipped=26`)
2. `spokenExpressions.md` (`unresolved=21`, `skipped=0`)
3. `phrases.md` (`unresolved=4`)
4. `collocations.md` (`unresolved=3`)
5. `sentencePatterns.md` (`skipped=22`)

Parser diagnostics show:
- `sentencePatterns.md` skipped lines are mostly numbered explanations (`1. **It** ...`) that current parser does not consume.
- `word.md` skipped lines are mostly comment lines (`<!-- Level x -->`), low severity.

## Root Cause Summary
1. **Independent generation without shared identity**: labels are free text, not linked to a common entry ID/lemma set.
2. **Reference strings drift**: same concept appears with quote/punctuation or variant wording (e.g., `"That's extensive!"`, `a little bit`).
3. **Coverage mismatch**: many referenced terms do not exist as resolvable nodes in imported corpus.
4. **Mixed structured + narrative content** in `sentencePatterns.md`, causing non-actionable parse skips.

## Priority Plan

### P0 (first)
Goal: reduce unresolved quickly without changing product logic.

1. Add shared registry file:
- New file: `asserts/lexicon-registry.csv`
- Minimum columns:
  - `entryId` (stable id, e.g. `word:happy`, `phrase:little_by_little`)
  - `nodeType` (`word_sense|phrase|collocation|sentence_pattern|spoken|slang|idiom`)
  - `headword`
  - `lemma`
  - `aliases` (pipe-separated)
  - `preferredPos`

2. Add explicit references in every asset block:
- `refs: entryId1 || entryId2 ...`
- For spoken lines, add anchor id:
  - `anchorRef: word:big`

3. Normalize quoted spoken expressions before export:
- Remove outer quotes from spoken text.
- Keep punctuation, but normalize smart quotes and duplicate spaces.

### P1 (second)
Goal: stabilize parser throughput and reduce skipped noise.

1. `sentencePatterns.md` split narrative from machine fields:
- Keep importable keys only in main file:
  - `中文`, `结构`, `用法`, `例句1`, `例句2`, `相关句型`
- Move long numbered explanation to sidecar docs (optional):
  - `sentencePatterns.notes.md`

2. Optional: remove `<!-- Level x -->` comments in import path or keep in a non-import copy.

### P2 (third)
Goal: improve linking quality after schema is stable.

1. Add high-frequency alias corrections from unresolved top labels:
- `word.md`:
  - `sorrowful`, `dismayed`, `abundant`, `a little bit`, `absolutely delighted`
- `spokenExpressions.md`:
  - normalize lines such as `That's extensive!`, `How big of you!`, `Happy days!`

2. Add consistency lint before import:
- reject/refactor labels not present in `lexicon-registry.csv` or alias set.

## Recommended Minimal Contract (for independent LLM generation)
When each file is generated independently, enforce this contract:

1. Every block/line must include stable identity fields:
- `entryId`
- `headword`
- `lemma`

2. Every cross-knowledge link uses IDs, not only text:
- `refs: word:happy || idiom:water_under_bridge`

3. Text is display-only; linking uses IDs:
- `text: Happy days!`
- `ref: spoken:happy_days`

4. Unknown refs are allowed but flagged:
- unresolved does not block import, but appears in report.

## File-Specific Suggestions

### `word.md`
- Keep as main source, but add `entryId` and `refs` per block.
- Ensure each synonym/antonym/phrase/collocation item has a resolvable target id.
- Reduce creative variants that have no registry target.

### `spokenExpressions.md`
- Keep one expression per line format, add anchor and reference ids:
  - `big (L1): How big of you! || 你可真大方！ || anchorRef=word:big || ref=spoken:how_big_of_you`
- Remove wrapping double quotes around expression text.

### `sentencePatterns.md`
- Keep machine-import fields flat; move teaching prose to notes sidecar.
- Add `ref` entries for related patterns by id.

### `collocations.md` / `phrases.md` / `slang.md` / `idioms.md`
- Add `entryId` for each block and `refs` to parent/related word ids.
- Normalize variants to registry aliases.

## Acceptance Targets for Next Iteration
- unresolvedRefs: 329 -> <= 140
- pendingReview: 51 -> <= 30
- sentencePatterns skippedBlocks: 22 -> <= 3
- no file with unresolvedRefs > 120

## Execution Note
Use skill command to re-check after each asset update:

```powershell
powershell -ExecutionPolicy Bypass -File .\.agents\skills\asset-link-enricher\scripts\run-asset-link-enricher.ps1 -OutFile .\reports\asset-link-baseline.json
```
