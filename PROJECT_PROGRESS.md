## 2026-04-15 - Hide relation candidate panel when no pending items
- Current status:
  - Updated [LexicalAssetImportPanel.tsx](/d:/06-project/expo_duo/duoxx/components/admin/LexicalAssetImportPanel.tsx) to show `Relation Candidate Review` only when there are pending candidates.
  - When `pendingReview=0` and candidate list is empty, the panel is not rendered on page load/refresh.
- Verification:
  - `duoxx`: `npx tsc --noEmit` passed.
  - `duoxx`: `npm run lint -- components/admin/LexicalAssetImportPanel.tsx` passed.
- Blocked / not yet done:
  - None for this behavior change.
- Next concrete work item:
  - If needed, add an explicit "Show Batch Details" toggle for low-frequency diagnostics instead of auto-display.

## 2026-04-15 - Import panel template actions moved to secondary tier
- Current status:
  - Updated [LexicalAssetImportPanel.tsx](/d:/06-project/expo_duo/duoxx/components/admin/LexicalAssetImportPanel.tsx) to demote template actions from the primary action row.
  - Primary row now only keeps core workflow actions (choose file / create batch / publish / clear).
  - Template downloads are now in a secondary utility row (`Templates (Optional)`) with lighter link-style affordance.
- Verification:
  - `duoxx`: `npx tsc --noEmit` passed.
  - `duoxx`: `npm run lint -- components/admin/LexicalAssetImportPanel.tsx src/storage/lexicalAssetImportSessionStorage.ts` passed.
- Blocked / not yet done:
  - No functional behavior changes to import pipeline; this is hierarchy/interaction emphasis only.
- Next concrete work item:
  - If needed, add a collapsible "More tools" wrapper so optional utilities can be hidden by default.

## 2026-04-15 - Import panel stale warning/session persistence fix
- Current status:
  - Updated import session storage version to `v2` in [lexicalAssetImportSessionStorage.ts](/d:/06-project/expo_duo/duoxx/src/storage/lexicalAssetImportSessionStorage.ts) to drop stale cached parse state.
  - Added `batchId` into persisted import session so refresh can restore current batch context.
  - Updated [LexicalAssetImportPanel.tsx](/d:/06-project/expo_duo/duoxx/components/admin/LexicalAssetImportPanel.tsx):
    - restore `batchId` on hydration and auto-refresh batch report/candidates,
    - after successful import batch creation, clear in-memory parser review/file fields so old parse warnings are not repeatedly shown,
    - persist `review: null` once `batchId` exists to keep UI focused on batch review.
- Verification:
  - `duoxx`: `npx tsc --noEmit` passed.
  - `duoxx`: `npm run lint -- components/admin/LexicalAssetImportPanel.tsx src/storage/lexicalAssetImportSessionStorage.ts` passed.
- Blocked / not yet done:
  - Import flow is still manual for save/publish actions.
- Next concrete work item:
  - Add optional one-click "upload -> create batch -> refresh review" action (still stop before publish).

## 2026-04-15 - Remove 1A local asset-build path
- Current status:
  - Removed 1A local-processing feature artifacts from repo:
    - deleted `scripts/build-knowledge-dag-assets.js`
    - deleted `.codex/skills/knowledge-dag-asset-builder/`
    - deleted generated output folder `asserts/knowledge-dag/`
  - Active workflow is now simplified to direct admin upload/import/review/publish in `/admin/pipeline -> Review Hub -> Import`.
- Blocked / not yet done:
  - None for this removal.
- Next concrete work item:
  - If needed, add in-page one-click auto-run (upload -> create batch -> refresh report) without reintroducing local file-build step.

## 2026-04-15 - Lexical markdown parser plural-header fix
- Current status:
  - Fixed parser routing for structured markdown assets in [lexicalSingleFileImport.ts](/d:/06-project/expo_duo/duoxx/src/services/lexicalSingleFileImport.ts:1178).
  - Structured detector now accepts plural and explicit headers used by uploaded files:
    - `collocations`, `phrases`, `sentencePatterns`, `idioms`, `spokenExpressions` (plus singular forms).
  - This prevents files from falling back to word-parser mode that generates mass `ORPHAN_FIELD` warnings (`Field appears outside a word block`).
- Verification:
  - `duoxx`: `npx tsc --noEmit` passed.
  - `duoxx`: `npm test -- src/services/__tests__/assetParseDiagnostics.test.ts --runInBand` passed.
- Blocked / not yet done:
  - Import tab still requires manual `Save Assets` and `Publish`.
- Next concrete work item:
  - Add one-click import flow that automatically creates batch and refreshes report/candidates after upload.

## 2026-04-14 - Knowledge absorb breadcrumb depth rule finalized
- Current status:
  - Breadcrumb display now uses explicit rule `navigationStack.length >= 2`.
  - Depth `1`: no breadcrumb chip shown.
  - Depth `2+`: first level and current level are both shown.
  - Card title top spacing follows the same rule (only offsets when breadcrumb is visible).
- Blocked / not yet done:
  - None for this behavior.
- Next concrete work item:
  - If needed, add a small interaction test around breadcrumb depth transitions to prevent future regressions.

## 2026-04-14 - Knowledge absorb breadcrumb visibility rule (hide single-item breadcrumb)
- Current status:
  - `duoxx/app/knowledge-absorb.tsx` now shows breadcrumb row only when `navigationStack.length > 1`.
  - Single-node state no longer shows the redundant first breadcrumb chip above the card title.
  - Title offset for breadcrumb mode now follows the same condition, removing wasted top spacing in single-node state.
- Blocked / not yet done:
  - None for this behavior change.
- Next concrete work item:
  - If you want, add a tiny enter animation only when breadcrumb appears (2+ levels) so hierarchy transition is clearer.

## 2026-04-14 - Knowledge absorb expansion items support click-to-drill
- Current status:
  - In `duoxx/app/knowledge-absorb.tsx`, expansion knowledge rows are now clickable.
  - Clicking an expansion item now opens that node as the active top card via existing `handleOpenNode` flow.
  - Breadcrumb path and node-specific expansion loading continue to work on the clicked target.
  - Expansion rows now include right chevron affordance and improved tappable row layout.
- Blocked / not yet done:
  - No additional interaction animation/polish was added in this step (only behavior + baseline visual affordance).
- Next concrete work item:
  - If UX needs stronger feedback, add pressed-state visuals and small motion to expansion row taps.

## 2026-04-10 - Pipeline graph node search missing go/get (active scope fallback fix)
- Current status:
  - Backend `listNodes` now supports keyword fallback:
    - if `scope=active` + keyword has no active hits, it auto-searches the active published snapshot and returns matching rows.
  - Response meta now includes `fallbackScope`, `fallbackReason`, and `snapshotVersion` for visibility.
  - Admin panel now shows hint text when displayed rows are from snapshot fallback.
  - Added integration test coverage for this behavior in `src/services/__tests__/lexiconGraphService.integration.test.js`.
  - Frontend type definitions updated to include new fallback meta fields.
- Blocked / not yet done:
  - Backend jest execution is blocked in this Windows workspace because backend dev dependencies are unavailable (`cross-env` missing in current shell environment).
- Next concrete work item:
  - Re-run backend test in the server environment with dependencies installed:
    - `npm test -- src/services/__tests__/lexiconGraphService.integration.test.js --runInBand`
  - Manually verify in `/admin/pipeline` that searching `go` / `get` under active scope now returns results (with fallback hint visible when triggered).

## 2026-04-10 - Admin pipeline graph relations UI polish (knowledge graph view)
- Current status:
  - `duoxx/components/admin/LexiconGraphExplorerPanel.tsx` relation-group tabs are now compact horizontal chips with separate count badges.
  - Fixed the stretched vertical-pill issue in the relation-group strip by constraining tab height and cross-axis alignment.
  - Relation rows now show clearer metadata pills (`relation type`, `confidence`) and improved spacing/background for faster scan.
  - Added edge-type label mapping for user-facing readability (`formatEdgeTypeLabel`).
  - Type check passed: `npx tsc --noEmit` (in `duoxx/`).
- Blocked / not yet done:
  - Browser visual QA against real admin runtime has not yet been re-run in this task.
- Next concrete work item:
  - Run `/admin/pipeline` manual visual smoke on desktop + narrower viewport and adjust chip truncation rules only if long labels overflow.

## 2026-04-03 - Admin /pipeline Review Hub browser smoke after MCP recovery
- Current status:
  - Browser automation channel recovered and used for real UI validation on `http://localhost:8081/admin/pipeline`.
  - Login with operator account succeeded and dashboard rendered normally.
  - Clicking `Review Hub` did not reproduce the prior runtime crash (`Cannot read properties of undefined (reading 'length')`).
  - Console showed only normal login/course-fetch logs, no error/warn stack for Review Hub.
- Blocked / not yet done:
  - This round is smoke-level validation; no exhaustive dataset permutation test was run.
- Next concrete work item:
  - If user can still reproduce intermittently, capture the exact click sequence + imported dataset id and run focused reproduction with the same data.
## 2026-04-03 - Browser MCP transport recovery (playwright + chrome_devtools)
- Current status:
  - Browser automation transport recovered in-session: both `mcp__playwright__browser_tabs` and `mcp__chrome_devtools__list_pages` now return normal results.
  - The prior error was `Transport closed` on both channels, indicating MCP connection-layer failure rather than page logic failure.
- Blocked / not yet done:
  - Root-cause certainty is inferred from process behavior; there is no dedicated per-session MCP crash trace exposed in current logs.
- Next concrete work item:
  - If this recurs, immediately capture the Codex app-server process list + MCP call error timestamp, then do the same minimal app-server recycle flow.
## 2026-04-03 - Graph-first runtime smoke (manual trigger, no scheduler)
- Current status:
  - Live API smoke on http://localhost:3000 passed with real login (/api/auth/login) and operator token.
  - Retired routes now behave as expected: /api/pipeline/quizzes* and /api/learning/lexical-quizzes/active return 404.
  - Graph-first learner route works: /api/learning/recommendations returns recommendations and snapshot version.
  - Import -> report -> publish -> recommendation loop was executed once successfully via:
    - POST /api/pipeline/lexicon/import-batches
    - GET /api/pipeline/lexicon/import-batches/:batchId/report
    - POST /api/pipeline/lexicon/publish
  - Strict quality gate consistency was fixed in service code: report/publish now share the same gate evaluator.
  - Added integration regression assertion to guarantee report qualityReport.passed aligns with publish behavior.
  - Restarted WSL backend runtime and re-ran live smoke: report_passed=True and publish succeeded consistently for the same batch.
- Blocked / not yet done:
  - Frontend browser-level click path (/admin/pipeline full UI interactions) has not been re-run in this round.
  - Automated browser MCP channels were unavailable in this session (transport closed), so Review Hub click flow still needs manual/browser verification.
- Next concrete work item:
  - Run one browser-level admin smoke on /admin/pipeline (Import & Review + Review Hub click path) against this restarted runtime.
## 2026-03-26 - Imported-word browse course exposed in Courses tab
- Current status:
  - 鐎电厧鍙嗙拠宥嗙湽濞村繗顫嶉敓?is now visible in /(tabs)/courses under the default ll category and routes to /imported-word-course.
- Blocked / not yet done:
  - Entry is currently a fixed local card, not backend-configurable course metadata.
- Next concrete work item:
  - If needed, migrate this card to backend course registry so it can be managed with other course items.
## 2026-03-26 - Hotfix for home tab compile block
- Current status:
  - pp/(tabs)/index.tsx syntax around ocabSubtitle is now parse-safe; no unterminated-template compile block.
- Blocked / not yet done:
  - None in code; only potential local cache residue on developer machine.
- Next concrete work item:
  - If red screen remains, run Expo with cache clear and hard reload once.
## 2026-03-26 - Imported-word browse course (no exercise loading)
- Current status:
  - Learner now has a dedicated route /imported-word-course for browsing imported words only (no quiz/exercise rendering).
  - Data source reads imported lexical assets via pipelineApi.listLexicalLearningEntries() with local-storage fallback.
  - Home tab includes a direct entry card to this browse course.
- Blocked / not yet done:
  - Not yet surfaced in learning-modules registry list.
  - No learner progress/bookmark state is recorded yet for this browse flow.
- Next concrete work item:
  - Decide whether to add this route into module registry and whether to add lightweight progress markers (last viewed word/bookmark).
## 2026-03-20 - Mongo lexical option migration + higher-quality distractor rules
- Current status:
  - Added backend migration script `duoxx_server/scripts/migrate-lexical-quiz-options-v1.js` to rewrite legacy `translation_choice / word_card` options using the latest translation-choice rules.
  - Added backend helper `duoxx_server/src/services/lexicalQuizOptionRules.js` and test coverage so migration dry-run and future option normalization use explicit Chinese-translation-only rules.
  - Server-side and local fallback distractor selection now prioritize same part of speech first, then closer difficulty, then overlapping scene tags, while excluding `true/false`, duplicates, and the correct answer.
- Blocked / not yet done:
  - Existing Mongo records are not rewritten until the migration is run with `--apply`; only dry-run validation has been executed so far.
  - The backend service and the frontend fallback still keep similar rule logic in separate files; they now behave consistently but are not yet physically deduplicated across runtimes.
- Next concrete work item:
  - Run `npm --prefix duoxx_server run migrate:lexical-quiz-options-v1 -- --apply` against the target environment after reviewing the dry-run samples, then smoke-test one migrated lexical course in the learner.
## 2026-03-20 - Exercise Review approve-and-activate simplification
- Current status:
  - Exercise Review now uses a single primary action: 閿熸枻鎷峰噯閿熸枻鎷烽敓鏂ゆ嫹鏁?
  - Already-active questions no longer show a second activation button; they display 閿熸枻鎷峰墠閿熸枻鎷?instead.
- Blocked / not yet done:
  - The backend still keeps separate approve/activate endpoints internally; the simplification is currently a UI-level orchestration.
- Next concrete work item:
  - Decide whether the backend should gain a dedicated pprove-and-activate endpoint or whether the current UI composition is sufficient.
## 2026-03-20 - Exercise Review semantic simplification
- Current status:
  - Exercise Review no longer exposes 閿熸枻鎷烽敓鏂ゆ嫹閿熸枻鎷?/ 閿熸枻鎷锋€侀敓鏂ゆ嫹 / 閿熸枻鎷峰墠閿熻姤鏈?in the operator UI.
  - The panel now groups by 閿熸枻鎷烽敓鏂ゆ嫹 on the left and shows all exercises under the selected sense on the right.
  - The generic 閿熸枻鎷烽敓缂寸尨鎷烽€?action has been replaced with explicit 閿熸枻鎷烽敓鏂ゆ嫹閫夐敓鏂ゆ嫹閿熸枻鎷?and 閿熸枻鎷烽敓鏂ゆ嫹閿熷彨璁规嫹閿熸枻鎷?actions.
- Blocked / not yet done:
  - Backend data still keeps quiz versioning internally; the UI now hides that model instead of deleting it.
  - Learning-side quiz consumption still has not switched to the active lexical quiz endpoint.
- Next concrete work item:
  - Run a browser smoke test for /admin/pipeline -> Exercise Review, then decide whether 閿熸枻鎷蜂负閿熸枻鎷锋晥閿熸枻鎷?should be auto-triggered on approve.
## 2026-03-20 - Import panel session persistence
- Current status:
  - `Import & Review` now restores uploaded file name, parsed review result, selected entry, and status after tab switches.
  - A local session store was added for the import panel only.
- Blocked / not yet done:
  - This does not alter backend quiz APIs or data persistence for imported quiz content.
- Next concrete work item:
  - If needed, wire any additional import UI fields into the same session store; otherwise leave the scope limited to the current restored fields.
## 2026-03-20 - Exercise Review panel encoding fix
- Current status:
  - `Exercise Review` UI labels were rewritten into a UTF-8-safe config and the panel source was rewritten to remove mojibake.
  - Backend quiz lifecycle remains unchanged.
- Blocked / not yet done:
  - Old imported quiz content can still be garbled if it was created from earlier corrupted template data.
- Next concrete work item:
  - If the page still shows bad quiz text after a hard refresh, re-import or clear the stale seed/local review data source that fed those records.
## 2026-03-23 - Exercise Review duplicate quiz dedupe
- Current status:
  - Exercise Review now deduplicates identical quizzes by semantic signature before rendering, so a seed/generated pair with the same visible question no longer appears twice.
  - Backend generation now skips writing duplicate quizzes when the new question would be visually identical to an existing seed or generated item.
- Blocked / not yet done:
  - Existing duplicate records remain in Mongo, but they are now hidden by list dedupe and no longer get regenerated.
  - The learner side has not been smoke-tested against a duplicate-heavy course after this backend change.
- Next concrete work item:
  - Run one admin import/review + learner smoke path on a course that previously showed duplicate judgment questions, then decide whether to backfill a Mongo cleanup script for historical duplicates.
# Project Progress

Last updated: 2026-03-20

## Current Focus
- V5 single-file lexical asset import is the default operator flow.
- Markdown is the primary template; CSV/TXT are compatibility inputs.
- 閿熺粸浼欐嫹閿熸枻鎷烽敓鏂ゆ嫹閿熸枻鎷烽敓鏂ゆ嫹閿熺Ц鍖℃嫹涓虹郴缁熼敓鏂ゆ嫹閿熺即锝忔嫹`閿熸枻鎷烽敓鏂ゆ嫹閫夐敓鏂ゆ嫹閿熸枻鎷?/ 閿熷彨璁规嫹閿熸枻鎷穈閿熸枻鎷?
## Done
- Single-file import and review page is live in `/admin/pipeline`.
- Word/phrase headwords, multiple senses, translated facets, and translated examples are supported.
- 閿熷姭鍑ゆ嫹閿熸枻鎷烽敓渚ョ》鎷锋ā閿熸枻鎷烽敓鏂ゆ嫹閿熸枻鎷峰彧閿熸枻鎷烽敓鏂ゆ嫹鐭ヨ瘑閿熺粸璇ф嫹閿熻娈碉綇鎷烽敓鏂ゆ嫹閿熸枻鎷风ず閿熸枻鎷烽敓鏂ゆ嫹鍐?quiz閿熸枻鎷?- Seed quizzes can now be persisted from lexical review into backend Mongo collections.
- Generated quiz versions, active quiz bindings, and stale marking are now implemented in backend Mongo collections, with local AsyncStorage fallback still kept as a dev safety net.
- `Exercise Review` now hosts the lexical quiz version review panel with `Seed / Generated / Active / Stale` filters and approve/reject/activate/generate actions.
- Vocab lesson routes now prefer `/api/learning/lexical-quizzes/active` for `multiple_choice` and `true_false` quiz playback, with automatic fallback to the existing lesson payload when no usable active lexical quiz exists.
- The main admin page no longer exposes the old V4 multi-file import flow by default.
- `lexical-quiz-lifecycle-v1.md` now defines where dynamic quiz updates should be stored and how admins should review them.
- Progress tracking is now mandatory in both `PROJECT_MEMORY.md` and `PROJECT_PROGRESS.md`.
- The unused V4 lexical import implementation and its test/config files have been removed from the Expo repo.
- Backend learning route now exposes `/api/learning/lexical-quizzes/active` for current active lexical quiz reads.
- `Exercise Review` 閿熸枻鎷烽敓鏂ゆ嫹閿熸枻鎷烽敓鏂ゆ嫹 `閿熸枻鎷烽敓缂村嚖鎷烽敓鏂ゆ嫹閫夐敓鏂ゆ嫹閿熸枻鎷?/ 閿熸枻鎷烽敓鏂ゆ嫹閿熷彨璁规嫹閿熸枻鎷穈閿熸枻鎷烽敓鏂ゆ嫹閿熷姭甯嫹 `word_card` 閿熸枻鎷烽敓鏂ゆ嫹閿熸枻鎷烽敓鏂ゆ嫹閿熸枻鎷烽敓鏂ゆ嫹閿熼叺鈽呮嫹
- 瀛︿範閿熸枻鎷烽敓鏂ゆ嫹閿熸枻鎷峰紡鏀敓鏂ゆ嫹 `translation_choice`閿熸枻鎷穕egacy `word_card / multiple_choice` 閿熸枻鎷烽敓鑺傝鎷峰彇鏃堕敓鏂ゆ嫹閿熸枻鎷疯縼閿熺嫛鈽呮嫹

## Not Done
- 瀛︿範閿熷壙浼欐嫹娌￠敓鏂ゆ嫹閿熸枻鎷烽敓鏂ゆ嫹閿熸枻鎷烽敓鏂ゆ嫹閿熺粸鍖℃嫹閿熸枻鎷烽敓鏂ゆ嫹閿熺禇translation_choice` 閿熺殕闈╂嫹閿熸枻鎷烽敓鏂ゆ嫹閿熸枻鎷烽€夐敓鏂ゆ嫹閿熸枻鎷烽敓鏂ゆ嫹閿熸枻鎷烽敓?- There is still legacy candidate-review code in the repo outside the current lexical quiz review path; it is bypassed but not fully deleted.
- The frontend still keeps local lexical quiz storage as fallback; once backend stability is confirmed, that fallback can be reduced or removed.

## Next Steps
- Decide whether the learner should keep reusing the current multiple-choice renderer for `translation_choice` or gain a dedicated lexical-card layout.
- Decide whether to keep or remove the frontend local lexical quiz fallback after backend smoke testing.
- Remove or archive the remaining legacy candidate-review code after the Mongo-backed lexical quiz path is stable.

## 2026-03-20 - Lexical quiz V2 contraction to knowledge-first + system-generated questions
- Current status:
  - Official Markdown/TXT/CSV lexical templates now only demonstrate knowledge assets; hand-written quiz blocks were removed from the operator-facing templates.
  - `Exercise Review` now treats `translation_choice` as the formal word-meaning exercise type and uses explicit buttons: `閿熸枻鎷烽敓缂村嚖鎷烽敓鏂ゆ嫹閫夐敓鏂ゆ嫹閿熸枻鎷?/ 閿熸枻鎷烽敓鏂ゆ嫹閿熷彨璁规嫹閿熸枻鎷穈.
  - Learner-side active lexical quiz playback now formally supports `translation_choice`, while legacy `word_card / multiple_choice` payloads are mapped into the same path for compatibility.
- Blocked / not yet done:
  - Backend and local storage still retain internal `seed/generated/version` structures; those are hidden from the operator UI but not yet renamed internally.
  - The import parser still accepts legacy quiz blocks for compatibility, even though the official template no longer promotes them.
- Next concrete work item:
  - Run a live end-to-end smoke test: import a knowledge-only markdown file, save assets to Mongo, generate one translation-choice quiz, approve it, and confirm the learner reads it from `/api/learning/lexical-quizzes/active`.

## 2026-03-20 - Learning-side active lexical quiz hookup
- Current status:
  - `app/lesson-exercise/[lessonId].tsx` now checks `GET /api/learning/lexical-quizzes/active` first for vocab routes and converts usable active quizzes into `LessonEngine` exercises.
  - If the active lexical quiz pool is empty or contains only unsupported quiz types, the screen falls back to the existing backend lesson payload without breaking the old course flow.
  - Adaptive session startup remains disabled for this lexical-active path so the new quiz source does not fight the existing adaptive lesson contract.
- Blocked / not yet done:
  - This learner-side path still renders `word_card` as a meaning multiple-choice exercise; there is not yet a dedicated flashcard-style interaction.
- Next concrete work item:
  - Decide whether `word_card` should stay as a meaning multiple-choice shortcut or graduate into its own dedicated learner interaction.

## 2026-03-20 - Mongo persistence feedback + Exercise Review status copy
- Current status:
  - `Import & Review` now explicitly tells operators whether `閿熸枻鎷烽敓鏂ゆ嫹閿熺粸璇ф嫹閿熻淇濋敓鏂ゆ嫹閿熸枻鎷穈 wrote to backend Mongo or fell back to local storage.
  - `Exercise Review` now reports whether quiz versions were loaded from backend Mongo or local fallback.
  - Review filter labels, status labels, quiz type labels, and generation reasons are now driven by UTF-8-safe copy config.
- Blocked / not yet done:
  - If old records were imported from corrupted source text, item content itself can still look bad until re-imported.
- Next concrete work item:
  - Re-run `閿熸枻鎷烽敓鏂ゆ嫹閿熺粸璇ф嫹閿熻淇濋敓鏂ゆ嫹閿熸枻鎷穈 after restarting backend, confirm status says backend Mongo, then verify `lexicalAssets` and `seedQuizzes` collections receive documents.

## 2026-03-20 - Lexical quiz API path fix + import session persistence
- Current status:
  - Lexical quiz review/import API calls now consistently target `/api/pipeline/...` and `/api/learning/...`, fixing the earlier 404 path mismatch that forced silent local fallback.
  - `Import & Review` now persists its local session across tab switches and shows whether seed save hit backend Mongo or local fallback.
  - `Exercise Review` also shows whether the current quiz list came from backend Mongo or local fallback.
- Blocked / not yet done:
  - Need a live operator smoke test after backend restart to confirm Mongo receives `lexicalAssets` and `seedQuizzes`.
- Next concrete work item:
  - Re-open `/admin/pipeline`, import a lexical asset file, click `閿熸枻鎷烽敓鏂ゆ嫹閿熺粸璇ф嫹閿熻淇濋敓鏂ゆ嫹閿熸枻鎷穈, confirm the status says backend Mongo, then verify the two Mongo collections contain documents.

## 2026-03-20 - Import & Review left list compactness
- Current status:
  - The left lexical entry list in `LexicalAssetImportPanel.tsx` now shows `鐠囧秵鈧溇 | 娓氬褰瀤` on the same line as the title and uses smaller vertical padding/margins.
  - This change is presentation-only; parsing, save behavior, and API paths remain unchanged.
- Blocked / not yet done:
  - No business-logic changes were made by request.
- Next concrete work item:
  - If needed, further tighten left-rail typography and badge sizing after a browser smoke test.
## 2026-03-20 - Import review list compaction
- Current status:
  - Import review left-side word rows now show `閿熸枻鎷烽敓鏂ゆ嫹 x | 閿熸枻鎷烽敓鏂ゆ嫹 x` inline beside the headword instead of taking a second summary line.
  - Entry row vertical spacing has been tightened to reduce wasted height in the review list.
- Blocked / not yet done:
  - A live browser check is still needed to confirm the compact row density feels right with real long words and issue badges.
- Next concrete work item:
  - Verify the compact list with a real imported markdown asset and adjust widths only if count text wraps too aggressively.
## 2026-03-20 - Exercise Review compactness + version-copy cleanup
- Current status:
  - The Exercise Review panel now groups quiz items by sense and uses a denser left list with shorter row height.
  - Display copy avoids version-like labels in the main UI, and the active-state wording is simplified to `瑜版挸澧犳０姒?/ `瀹稿弶娴涢幑顣?
- Blocked / not yet done:
  - Need a browser smoke test on real imported assets to confirm the tighter list still reads well.
- Next concrete work item:
  - Run the admin page with real quiz data, check the compressed grouped list, and trim widths only if labels wrap awkwardly.

## 2026-03-20 - Lexical practice answer-validation investigation and option normalization
- Current status:
  - Browser-level verification on `/lesson-exercise/vocab-course-...` confirmed the learner does not actually mark every option correct; wrong selections still produce `閿熸枻鎷烽敓鏂ゆ嫹涓€閿熸枻鎷穈.
  - Root cause was lexical option quality, not validator failure:
    - legacy `word_card` compatibility could pull `true/false` answers into translation distractors
    - translation-choice options kept the correct answer pinned too predictably at the first slot
  - Frontend lexical quiz adapter now filters legacy distractors to translation-like Chinese answers only and rotates options deterministically so the correct answer is not always first.
  - Local storage generation and backend Mongo generation now apply the same deterministic option rotation for new `translation_choice` questions.
- Blocked / not yet done:
  - Existing active quiz records in Mongo keep their stored option order; the learner adapter normalizes them at read time, but no data migration has been run yet.
- Next concrete work item:
  - Decide whether to run a one-off Mongo migration to rewrite old `translation_choice` and promoted legacy `word_card` option arrays into the new normalized order.

## 2026-03-20 - Translation-choice distractor quality upgrade
- Current status:
  - `duoxx_server/src/services/lexicalQuizService.js` now scores translation-choice distractors with explicit priority for same part of speech, then difficulty proximity, then scene-tag overlap.
  - `duoxx/src/storage/lexicalQuizReviewStorage.ts` uses the same scoring rules for local generation so backend and fallback stay aligned.
  - Non-translation distractors are filtered out; ASCII-only `true/false` style candidates no longer enter translation-choice option pools.
  - New tests cover the higher-quality distractor selection path on both backend generation and local storage generation.
- Blocked / not yet done:
  - Existing saved quiz records are not migrated; the new rules apply to new generation and to read-time normalization.
- Next concrete work item:
  - Optionally run a one-off data cleanup later if old stored translation-choice rows should also be rewritten in place.

## 2026-03-26 - Learning tab IA simplification (task-first)
- Current status:
  - Home tab non-parent mode now renders as three sections: `閿熸枻鎷峰涔犺矾閿熸枻鎷穈 / `閿熸枻鎷烽敓鏂ゆ嫹鏁仾鐧?/ `瀛︿範閿熸枻鎷锋簮`.
  - Repeated `瀛︿範閿熸枻鎷烽敓鏂ゆ嫹` entry in resource cards was removed; diagnostic actions are now閿熸枻鎷烽敓鏂ゆ嫹閿熸枻鎷?`閿熸枻鎷烽敓鏂ゆ嫹鏁仾鐧?閿熸枻鎷烽敓鏂ゆ嫹.
  - Old `瀛︿範缁熼敓鏂ゆ嫹` block was removed from first screen to reduce visual load.
- Blocked / not yet done:
  - No in-device visual QA screenshots yet for narrow screens and CHILD/STUDENT mode spacing.
- Next concrete work item:
  - Run RN device smoke checks for Home tab (Adult + Child + Student), then tune spacing if diagnostic block appears crowded.
## 2026-03-26 - Learning tab compact-mode optimization
- Current status:
  - Home tab now has responsive compact layout (`width < 390`) with stacked diagnostic cards/actions and tighter section spacing.
  - CHILD/STUDENT mode now uses medium avatar + smaller heart icons on compact screens to avoid crowding.
- Blocked / not yet done:
  - No screenshot-based device QA record yet for 360/375 widths.
- Next concrete work item:
  - Run visual smoke tests on narrow devices and fine-tune subtitle truncation/line-clamp rules if still crowded.
## 2026-03-26 - 閿熸枻鎷烽敓鏂ゆ嫹閿熸枻鎷烽〉閿熸枻鎷峰閿熸枻鎷?閿熸枻鎷蜂範/閿熸枻鎷烽敓娲侊級
- Current status:
  - 閿熻瀹剁鎷烽敓鏂ゆ嫹椤甸敓鏂ゆ嫹閿熸枻鎷烽敓鏂ゆ嫹涓?3 閿熸枻鎷烽敓鏂ゆ嫹閿熶粙锛歚瀛︿範閿熸枻鎷风煡璇嗛敓鏂ゆ嫹AI閿熺嫛纭锋嫹閿熸枻鎷穈閿熸枻鎷穈閿熸枻鎷蜂範閿熸枻鎷风煡璇哷閿熸枻鎷穈灞曢敓鏂ゆ嫹閿熸枻鎷烽敓鏂ゆ嫹`閿熸枻鎷?  - 閿熸枻鎷烽敓鏂ゆ嫹閿熸枻鎷烽敓渚ヮ剨鎷烽敓鏂ゆ嫹閿熸枻鎷风顑愰敓鏂ゆ嫹閿熸枻鎷峰睍绀洪敓鏂ゆ嫹閿熸枻鎷烽敓鏂ゆ嫹閿熸澃鍖℃嫹鐗囬敓鏂ゆ嫹閿熸枻鎷烽敓鏂ゆ嫹閿熸彮浼欐嫹閿熸枻鎷烽敓鏂ゆ嫹閿熸枻鎷疯妿閿熸枻鎷疯繙閿熸枻鎷烽敓鏂ゆ嫹閿?- Hidden entries kept (do not drop):
  - `閿熸枻鎷烽敓鏂ゆ嫹閿熸枻鎷烽敓鏂ゆ嫹鎷囬敓鏂ゆ嫹閿熺禇 -> `/prescriptions`
  - `閿熸枻鎷烽敓鏂ゆ嫹閿熺潾闈╂嫹` -> `/weakness-workbench`
  - `閿熸枻鎷烽敓鏂ゆ嫹璁敓鏂ゆ嫹` -> `/task-training`
  - `瀛︿範閿熸枻鎷烽敓鏂ゆ嫹` -> `/progress-dashboard`
  - `閿熸枻鎷烽敓鐨嗕紮鎷穈 -> `/personalization`
  - `閿熺粸浼欐嫹閿熸枻鎷烽敓鏂ゆ嫹閿熸枻鎷穈 -> `/vocab-assessment`
  - `閿熸枻鎷烽敓鏂ゆ嫹椹堕敓鏂ゆ嫹閿熸枻鎷穈 -> `/imported-word-course`
  - `閿熺即灏变紮鎷烽敓鏂ゆ嫹` -> `/achievements`
  - `閿熸枻鎷烽敓鏂ゆ嫹瀛︿範妯￠敓鏂ゆ嫹` -> `/learning-modules`
- Blocked / not yet done:
  - 閿熸枻鎷锋湭閿熸枻鎷烽敓鏂ゆ嫹閿熸枻鎷烽敓閰电》鎷烽敓琛椼倧鎷烽敓绲燨S/Android绐勯敓鏂ゆ嫹閿熸枻鎷风‘閿熸枻鎷烽敓渚ュ府鎷烽敓鎴鎷烽敓鏂ゆ嫹閿熶粙銆?- Next concrete work item:
  - 閿熸枻鎷烽敓鏂ゆ嫹 360/375 閿熸枻鎷烽敓鏂ゆ嫹娉抽敓鏂ゆ嫹姣撴浼欐嫹閿熸帴纰夋嫹閿熸枻鎷烽敓鏂ゆ嫹閿熸枻鎷烽箠閿熸枻鎷烽敓鏂ゆ嫹閿熸枻鎷烽敓鏂ゆ嫹鏂滈敓鏂ゆ嫹閿熸枻鎷烽敓鏂ゆ嫹閿熸枻鎷风ず閿熸枻鎷烽敓鐨嗭綇鎷烽敓鏂ゆ嫹妯￠敓鏂ゆ嫹鐪夐敓鏂ゆ嫹閿熸枻鎷?
## 2026-03-27 - CEO review retry (project-wide gaps and execution order)
- Current status:
  - Re-ran baseline checks from existing logs: duoxx/lint-full.log still reports 331 problems (81 errors, 250 warnings), and duoxx/tsc-full.log still reports 25 blocking TypeScript errors.
  - Critical blockers remain clustered in module exports/contracts and dependency mismatch (expo-blur missing, expo-speech previously flagged by audit).
  - Current admin/pipeline iteration speed improved, but engineering baseline (type safety + lint pass) is still below a safe acceleration threshold.
- Blocked / not yet done:
  - No full green CI baseline (lint, tsc, test) yet, so feature velocity is constrained by regression risk.
  - Home tab IA has been simplified, but no unified design token/system enforcement yet, so UI consistency can drift across screens.
  - Data contract governance is not yet strict enough to fully prevent malformed or duplicate content at import/publish boundaries.
- Next concrete work item:
  - Execute P0 stabilization sprint in this order: (1) dependency parity, (2) export/index cleanup, (3) route typing fixes, (4) failing type contracts, (5) targeted smoke tests on pipeline and learning primary flows.

## 2026-03-27 - P0 stabilization execution (blocking errors cleared)
- Current status:
  - TypeScript blocking errors were reduced from 25 to 0 (`cmd /c npx tsc --noEmit` passed).
  - ESLint blocking errors were reduced from 76 to 0 (`npm run lint` now reports `0 errors, 248 warnings`).
  - Survival Phrases typed routes were restored by adding missing Expo Router files under `app/modules/survival-phrases/*`.
- Blocked / not yet done:
  - Lint warnings remain large (248), mostly hooks deps / unused vars / import ordering and BOM warnings.
  - End-to-end smoke test for admin pipeline + learner lexical flow is still pending in this round.
- Next concrete work item:
  - Start warning-burndown batch by domain (`admin`, `speaking-avatar`, `dynamic-lexicon`) and keep `0 lint errors` invariant.

## 2026-03-27 - Warning burndown completion (lint clean)
- Current status:
  - ESLint warnings were reduced from 248 to 0; `npm run lint` now returns fully clean output.
  - TypeScript remains green after cleanup (`cmd /c npx tsc --noEmit` passed).
  - Targeted regression tests for touched areas passed:
    - `AnimationEngine.test.ts`
    - `SpeakingAvatarController.test.ts`
    - `ScenarioValidator.test.ts`
    - `PhraseManager.test.ts`
- Blocked / not yet done:
  - Full-app test suite was not run in this pass; verification was targeted to changed modules.
- Next concrete work item:
  - Run broader smoke/QA on primary learner flows and admin pipeline flow to confirm no runtime UI regressions after cleanup.

## 2026-04-02 - AGENTS constitution update (development-first engineering rules)
- Current status:
  - Added `Development-Phase Constitution (Mandatory)` in `AGENTS.md`.
  - New guardrails: architecture/code clarity first, no minimal-diff bias, no workaround/fallback padding in default development work.
- Blocked / not yet done:
  - Policy is documented, but no automated enforcement tooling is configured.
- Next concrete work item:
  - Apply the new constitution in the next implementation task and reject workaround-style proposals by default.

## 2026-04-02 - AGENTS.md quality pass (clarity and enforceability)
- Current status:
  - AGENTS.md was structurally optimized for developer-agent execution.
  - Added explicit rule priority, removed duplicated session-persistence wording, and clarified that commands run under duoxx/ by default.
  - Replaced the file-organization tree with ASCII-safe formatting.
- Blocked / not yet done:
  - No automated lint/check exists yet to validate AGENTS policy consistency.
- Next concrete work item:
  - In next workflow update, optionally add a lightweight AGENTS consistency checklist script.
## 2026-04-02 - Sentence Insight Pack V1閽€钘夋勾閿涘牏顬囩痪鍨瘶濞戝牐鍨?+ 閸欍儱鐡欐稉璇插幢閿?- Current status:
  - 瀹告彃鐣幋?V1 閺佺増宓佹總鎴犲娑撳骸褰傜敮鍐，缁備緤绱伴弽绋跨妇 4 濡€虫健缂傚搫銇戞导姘愁潶閺嶏繝鐛欓幏锔藉焻閵?  - 瀹告彃鐣幋鎰叀鐠囧棗鎯涢弨璺虹穿閹垮骸褰炵€涙劖妲х亸鍕剁窗娓氬褰為崣顖炩偓姘崇箖 `sentenceId/exampleKey` 缁墽鈥橀崨鎴掕厬 insight 閸栧懌鈧?  - 瀹告彃鐣幋鎰叀鐠囧棗鎯涢弨鍫曘€夋禍銈勭鞍閿涙碍婀侀崠鍛閺勫墽銇氶垾婊嗩嚊鐟欙絺鈧繐绱濋悙鐟板毊閸氬骸鍨忛崣銉ョ摍娑撹宕遍獮鑸垫暜閹镐讲鈧粏绻戦崶鐐插斧鐠囧秮鈧縿鈧?  - 瀹告彃鐣幋鎰侀崸妤€瀵查幎钘夌溄濞撳弶鐓嬮敍姘綖鐎涙劖膩瀵繑瀵滃Ο鈥虫健濞夈劌鍞界悰銊﹁閺屾搫绱濇稉宥勭贩鐠ф牕鍟撳璇插瀻閺€顖樷偓?- Blocked / not yet done:
  - 娴犲秶宸辩粋鑽ゅ殠閹电懓顦╅悶鍡楊嚤閸忋儰鎹㈤崝锛勬畱缁旑垰鍩岀粩顖欒閼辨棃鐛欑拠渚婄礄婢堆勫闁插繒婀＄€圭偛瀵橀敍澶堚偓?  - 娴犲秶宸辨い鐢告桨缁狙嗗殰閸斻劌瀵叉禍銈勭鞍濞村鐦敍鍫滅伐婵″倸鍨忕拠宥嗏偓褍鎮楅崘宥嗩偧鏉╂稑鍙嗙拠锕佇掗敍澶堚偓?- Next concrete work item:
  - 閹恒儱鍙嗛獮鎯扮獓闁艾顦婚柈銊﹀婢跺嫮鎮?insight 閸栧懎顕遍崗?smoke閿涘牆鎯?schema+鐎瑰本鏆ｉ幀?閸ョ偞鍑芥稉鈧懛瀛樷偓褝绱氶敍灞藉晙鐞涖儰绔撮弶?UI 娴溿倓绨伴懛顏勫З閸栨牜鏁ゆ笟瀣洬閻╂牕褰炵€涙劒瀵岄崡鈥崇窔鏉╂柣鈧?

## 2026-04-02 - Lexicon graph auto-first pipeline (strict gate + minimal manual)
- Current status:
  - Backend lexicon graph contract and routes are in place for import/review/publish and learning consumption.
  - Admin `LexicalAssetImportPanel` now supports:
    - batch creation from parsed lexical review
    - quality report and pending-candidate retrieval
    - tri-action candidate decisions (`闁俺绻?/ 閹锋帞绮?/ 閸氬牆鑻焋)
    - auto-publish when pending candidates are zero
  - Learner `imported-word-course` now supports graph-style navigation:
    - expansion click promotes target to main node
    - grouped expansion browsing, back navigation, return-to-root
    - `閻旂喐鍊?閹哄本褰檂 marking and recommendation refresh
  - Vocab completion scoring now uses composite score:
    - `final_score = 0.65*answer_accuracy + 0.35*mastery_progress`
    - quick-mark finish-state race is fixed, avoiding stale completion params.
- Blocked / not yet done:
  - Frontend `lexiconApi` still returns loosely typed payloads in several call sites.
  - No full e2e regression test yet for the complete lexicon graph operator->learner chain.
  - Legacy lexical seed-quiz import side-effect is still retained as compatibility behavior.
- Next concrete work item:
  - Add end-to-end smoke/e2e case for: import -> candidate decision -> publish -> learner graph expand/mark/recommend loop.
  - Add strict TS response interfaces for lexicon APIs and remove ad-hoc casts from UI.
  - Evaluate removal plan for legacy seed-quiz side-effect once graph flow is stable in production-like usage.

## 2026-04-02 - Lexicon API strict typing + route smoke loop
- Current status:
  - `duoxx/src/services/lexiconApi.ts` now exports explicit contract types for import/report/candidate/publish/graph/mark/recommend payloads.
  - `duoxx/app/imported-word-course.tsx` and `duoxx/components/admin/LexicalAssetImportPanel.tsx` now consume typed responses directly and removed ad-hoc response casts.
  - Added backend route smoke test `duoxx_server_link/src/routes/lexiconGraphFlow.test.js` covering:
    - import batch -> candidate review -> publish
    - learner graph node/expand read
    - mastery mark + recommendation refresh
- Blocked / not yet done:
  - This smoke test validates route orchestration with stateful service mocks; it is not a real DB-integrated e2e yet.
  - Legacy seed-quiz side-effect (`pipelineApi.importSeedQuizzesFromLexicalReview`) is still retained for compatibility.
- Next concrete work item:
  - Add one DB-backed integration test (or staging smoke script) for strict gate behavior with real persisted edges/nodes.
  - Plan and execute removal of legacy seed-quiz side-effect after confirming graph-only operator flow in production-like usage.

## 2026-04-02 - Lexicon strict-gate DB integration test landed
- Current status:
  - Added `mongodb-memory-server` dev dependency in `duoxx_server_link/package.json` (and lockfile updated) for real Mongo persistence integration testing.
  - Added `duoxx_server_link/src/services/__tests__/lexiconGraphService.integration.test.js`:
    - imports a real batch into Mongo
    - verifies strict gate blocks publish while candidates are pending
    - approves pending candidate and verifies publish succeeds
    - verifies active snapshot persisted and learner-side service methods (`getNode/expand/mark/recommend`) read expected data
  - Combined verification now passes:
    - route smoke tests + new DB integration test
- Blocked / not yet done:
  - This DB integration currently targets service-level orchestration, not full HTTP+auth+DB e2e.
  - Legacy seed-quiz compatibility side-effect still exists in admin import flow.
- Next concrete work item:
  - Add one HTTP-level e2e test on top of memory Mongo (pipeline+learning routes with auth middleware) to complete full-chain verification.
  - Start implementing deprecation/removal plan for legacy seed-quiz side-effect after one staging validation round.

## 2026-04-02 - Lexicon HTTP+DB e2e + legacy side-effect removal
- Current status:
  - Added full HTTP+DB e2e test `duoxx_server_link/src/routes/lexiconGraph.e2e.test.js` (memory Mongo + real pipeline/learning routes):
    - import batch
    - strict gate publish blocked before review
    - candidate approve
    - publish success
    - learner graph read/expand + mastery mark + recommendations
  - Removed legacy seed-quiz import side-effect from admin graph import flow:
    - `duoxx/components/admin/LexicalAssetImportPanel.tsx` no longer calls `pipelineApi.importSeedQuizzesFromLexicalReview(review)` during graph batch creation.
  - Route smoke + DB integration + new HTTP e2e are now all green.
- Blocked / not yet done:
  - Legacy seed-quiz endpoints and storage path still exist in backend codebase, but are no longer triggered by the graph import panel.
  - No staging telemetry yet on operator behavior after side-effect removal.
- Next concrete work item:
  - Observe one staging cycle for graph import and learner recommendation flow to confirm no hidden dependency on old seed-quiz write path.
  - Then remove/archive remaining legacy seed-quiz import code and update operator docs accordingly.

## 2026-04-02 - Legacy seed-quiz import endpoint retired
- Current status:
  - Frontend `pipelineApi` no longer exports legacy `importSeedQuizzesFromLexicalReview` method.
  - Backend `/api/pipeline/seed-quizzes/import-from-lexical-review` route has been removed from `pipeline.js`.
  - Backend `lexicalQuizService.importFromLexicalReview` and its dedicated helper code were removed; quiz review APIs remain available for existing generated/seed data.
  - Added regression guard in `pipeline.test.js`: posting legacy endpoint now returns `404`.
- Blocked / not yet done:
  - Legacy seed-quiz storage schema (`LexicalAsset` / `SeedQuiz`) still exists for compatibility and historical data reads.
  - Operator docs have not yet been explicitly updated to state that graph import is now the only supported import path.
- Next concrete work item:
  - Update operator-facing docs to mark legacy seed-quiz import as retired.
  - Plan archival/removal scope for remaining unused seed-quiz storage/write paths after staging observation.

## 2026-04-02 - Graph-only contract docs sync + legacy path labeling
- Current status:
  - Updated `duoxx/docs/lexical-quiz-lifecycle-v1.md` to the current graph-first lifecycle contract and marked legacy seed-quiz path as compatibility-only.
  - Added `duoxx/docs/seed-quiz-legacy-retirement-plan.md` with phased retirement workflow (observe -> deprecate UI -> retire writes -> archive -> final removal).
  - Updated admin/operator-facing wording:
    - `OperatorWorkbench` tab label now shows `Exercise Review (Legacy)`.
    - `pipelineApi` and backend routes now include explicit comments that legacy quiz APIs are compatibility paths, not default flow.
  - Synced README notes in both app and server repos to explicitly document graph import APIs and retired seed import endpoint.
- Blocked / not yet done:
  - Legacy quiz collections and compatibility endpoints are still present for historical reads.
  - No staging telemetry window has been executed yet for final removal decision.
- Next concrete work item:
  - Run one staging observation cycle and collect endpoint usage for `/api/pipeline/quizzes*` and `/api/learning/lexical-quizzes/active`.
  - If usage is zero or acceptable, start Phase 2/3 retirement from `seed-quiz-legacy-retirement-plan.md`.

## 2026-04-02 - Operator default nav hides legacy Exercise Review
- Current status:
  - `OperatorWorkbench` main tab row no longer exposes `Exercise Review` as a default entry.
  - Legacy review code path is kept in codebase for compatibility, but operators now enter graph flow from `Import` by default.
- Blocked / not yet done:
  - Legacy review component is still present and can still be reached only if tab state is set programmatically.
- Next concrete work item:
  - In the next cleanup phase, remove legacy review component mount block and related state/actions after staging confirms no dependency.

## 2026-04-02 - Staging observe round #1 (real HTTP flow)
- Current status:
  - Ran one full real-HTTP observation loop against running backend (`http://localhost:3000`):
    - auth register/login (operator)
    - graph import batch create
    - strict gate block before review (`409 LEXICON_QUALITY_GATE_BLOCKED`)
    - candidate approve decisions
    - publish success with snapshot
    - learner graph read/expand + mastery mark + recommendation refresh
  - Key observed results:
    - batch created: `pending_review=2`
    - publish before review: blocked as expected
    - publish after review: success (`snapshotVersion` generated)
    - mastery mark write/read loop: success
  - Legacy probes in same round:
    - retired endpoint `/api/pipeline/seed-quizzes/import-from-lexical-review` -> `404` (expected)
    - compatibility endpoints still return data:
      - `/api/pipeline/quizzes` -> `200`, data count `24`
      - `/api/learning/lexical-quizzes/active` -> `200`, data count `4`
- Blocked / not yet done:
  - This round validates API behavior, but does not yet provide passive traffic usage telemetry from real operator sessions.
  - Legacy compatibility endpoints still serve data, so immediate hard removal remains risky.
- Next concrete work item:
  - Add endpoint usage counters/log aggregation for `/api/pipeline/quizzes*` and `/api/learning/lexical-quizzes/active` over a staging window.
  - If observed real traffic is near-zero, proceed with Phase 2/3 retirement.

## 2026-04-03 - Enforce manual-trigger only for lexicon import/publish (no timer/scheduled publish)
- Current status:
  - Removed auto-publish behavior from `LexicalAssetImportPanel` after batch creation.
  - Import flow now stops at `batch ready` and requires explicit human click on `Publish`.
  - Cleaned broken string/render lines introduced during edit and restored full compile health.
  - Removed `scheduled_refresh` from `GeneratedQuizVersion.generationReason` enum to prevent future timed-generation semantics from being written.
- Blocked / not yet done:
  - Legacy compatibility read endpoints still exist (`/api/pipeline/quizzes*`, `/api/learning/lexical-quizzes/active`) and are outside this manual-trigger change.
- Next concrete work item:
  - Continue legacy endpoint usage observation window, then retire compatibility write/review paths by phase plan.

## 2026-04-03 - System test baseline step #1 (automation + smoke precheck)
- Current status:
  - Frontend baseline check passed:
    - `cmd /c npx tsc --noEmit --pretty false` (duoxx) -> pass.
  - Backend stable route-suite baseline passed:
    - `node_modules\\.bin\\jest.cmd src/routes/pipeline.test.js src/routes/learning.test.js src/routes/lexiconGraphFlow.test.js --runInBand` -> pass (3 suites / 15 tests).
  - Backend deep integration/e2e suites were blocked by environment dependency, not business assertion:
    - `src/routes/lexiconGraph.e2e.test.js`
    - `src/services/__tests__/lexiconGraphService.integration.test.js`
    - blocker: `mongodb-memory-server` first-run binary download + lockfile conflict (`C:\\Users\\Administrator\\.cache\\mongodb-binaries\\8.2.1.lock`) causing hook timeout and cleanup errors.
  - Authenticated API smoke in this shell is currently blocked by local auth/data mismatch:
    - register flow hits `E11000 ... email_1/phone_1 dup key: { ...: null }` in running backend (cannot create fresh smoke user via `/api/auth/register`).
    - existing admin/operator credentials are required to continue protected endpoint smoke from this environment.
- Blocked / not yet done:
  - Full authenticated staging smoke loop cannot be re-run end-to-end in this shell until one valid existing account is available (or auth null-unique index issue is fixed in running env).
  - `mongodb-memory-server` cache lock issue prevents reliable local execution of heavy integration/e2e suites.
- Next concrete work item:
  - Unblock one of:
    - provide a staging admin/operator test account for smoke script, or
    - fix/register-path null-unique-index behavior in running backend and rerun.
  - Clear mongodb-memory-server cache lock and rerun integration/e2e suites to complete baseline gate.

## 2026-04-03 - System test baseline step #1 completed (deep suites recovered)
- Current status:
  - Cleared corrupted Mongo memory-server cache artifacts under `C:\\Users\\Administrator\\.cache\\mongodb-binaries`, then reran deep suites successfully:
    - `src/services/__tests__/lexiconGraphService.integration.test.js` -> pass.
    - `src/routes/lexiconGraph.e2e.test.js` -> pass.
  - Stable + deep automated baseline now all green for graph core path:
    - frontend type gate pass,
    - backend route suites pass,
    - backend integration/e2e pass.
  - Runtime API smoke (without operator credentials) confirms learner read/expand/mark chain is live on current server:
    - `/health` -> 200
    - `/api/learning/recommendations` -> 200
    - `/api/learning/graph/node/:id` -> 200
    - `/api/learning/graph/node/:id/expand` -> 200
    - `/api/learning/mastery/mark` -> 200 (guest mode)
  - Operator-protected import endpoint auth gate is active:
    - `/api/pipeline/lexicon/import-batches` without token -> 401.
- Blocked / not yet done:
  - Real runtime operator import/review/publish smoke against the running staging server is still blocked by missing reusable admin/operator credentials from this shell.
  - Running server `/api/auth/register` currently returns null-unique-index duplicate-key errors in this environment, so smoke account bootstrap cannot rely on register API.
- Next concrete work item:
  - Step #2 staging business-chain鐟欏倹绁?
    - use existing operator account to run import -> candidate decision -> manual publish once,
    - then verify learner recommendations and legacy compatibility endpoint status.

## 2026-04-03 - Staging business-chain observe round #2 (operator account)
- Current status:
  - Used real operator account to run one full graph flow on running backend:
    - login -> import batch -> report -> publish gate block -> candidate decisions -> manual publish -> learner read/expand/mark.
  - Observed key runtime results:
    - import batch: `lexbatch_word_1775185968198_md_mnibw3fg`
    - import stats: `nodes=21`, `edges=14`, `pendingReview=6`
    - strict gate blocked before review: yes
    - reviewed/approved candidates: `6/6`
    - publish success snapshot: `lexicon_snapshot_mnibw3os`
    - learner recommendations: count `5`
    - root node probe `node_ws_run_v_1_1775185968198`: node `200`, `expand(all)=9`, `expand(synonyms)=2`
    - mastery mark write: success
  - Legacy path probe in same round:
    - retired seed import endpoint: `404` (expected)
    - compatibility endpoints still serving:
      - `/api/pipeline/quizzes`: `200`, count `24`
      - `/api/learning/lexical-quizzes/active`: `200`, count `4`
- Blocked / not yet done:
  - Legacy compatibility read endpoints still have data and are not yet retired.
  - `strict gate` error payload in this runtime did not return a stable `code` field every time, only block behavior.
- Next concrete work item:
  - Keep graph-only workflow as default and continue compatibility endpoint usage observation before final legacy removal.
  - If removal window starts, add response contract assertion for strict-gate blocked code consistency.

## 2026-04-03 - System test step #3 (compatibility + retirement risk check)
- Current status:
  - Runtime contract checks:
    - strict quality gate publish block returns `409`, and error payload includes code `LEXICON_QUALITY_GATE_BLOCKED`.
    - legacy compatibility routes are auth-protected at runtime:
      - `/api/pipeline/quizzes` -> `401` without token, `200` with operator token.
      - retired `/api/pipeline/seed-quizzes/import-from-lexical-review` -> `401` without token, `404` with token.
  - Static dependency scan (frontend) found active callers still depending on legacy compatibility APIs:
    - `app/lesson-exercise/[lessonId].tsx` calls `learningApi.getActiveLexicalQuizzes()` for `vocab-*` lessons.
    - `components/admin/LexicalQuizReviewPanel.tsx` still calls legacy quiz review/generate/approve/reject/activate APIs.
    - `src/services/learningApi.ts` and `src/services/pipelineApi.ts` still expose legacy compatibility methods.
- Blocked / not yet done:
  - Legacy compatibility endpoints cannot be hard-retired yet without breaking:
    - learner lexical route for `vocab-*`,
    - admin legacy review panel behavior.
  - Current system is graph-first by default flow, but not graph-only at code dependency level.
- Next concrete work item:
  - Step #4 Go/No-Go report:
    - **Go** for graph-first rollout and manual-trigger import/publish policy,
    - **No-Go** for final legacy endpoint removal until `lesson-exercise` lexical path is migrated off `/api/learning/lexical-quizzes/active`.

## 2026-04-03 - Step #4 execution started (learner `vocab-*` route migrated to graph recommendations)
- Current status:
  - Implemented first retirement blocker removal on learner side:
    - `app/lesson-exercise/[lessonId].tsx` no longer calls `learningApi.getActiveLexicalQuizzes()` for `vocab-*` lessons.
    - `vocab-*` lessons now call `lexiconGraphApi.getRecommendations()` and build exercises from graph recommendations.
  - Added new adapter:
    - `src/services/lexiconRecommendationLessonAdapter.ts`
    - converts graph recommendation nodes into `MULTIPLE_CHOICE` lesson exercises (question = `word | pos`, answer/options from node definitions and recommendation pool).
  - Added unit tests:
    - `src/services/__tests__/lexiconRecommendationLessonAdapter.test.ts` (2 cases pass).
- Verification:
  - `cmd /c npx tsc --noEmit --pretty false` (duoxx) -> pass
  - `cmd /c npx eslint app/lesson-exercise/[lessonId].tsx src/services/lexiconRecommendationLessonAdapter.ts src/services/__tests__/lexiconRecommendationLessonAdapter.test.ts --max-warnings=0` -> pass
  - `cmd /c npx jest src/services/__tests__/lexiconRecommendationLessonAdapter.test.ts --runInBand` -> pass
- Blocked / not yet done:
  - Admin legacy review panel (`LexicalQuizReviewPanel`) and `pipelineApi` legacy quiz review actions still depend on `/api/pipeline/quizzes*`.
  - `learningApi.getActiveLexicalQuizzes` wrapper still exists (currently no remaining app caller after this change).
- Next concrete work item:
  - Continue step #4 by migrating admin legacy review path off `/api/pipeline/quizzes*`, then re-run compatibility scan for final retirement readiness.

## 2026-04-03 - Step #4 follow-up (admin legacy review panel detached from workbench render path)
- Current status:
  - Removed legacy review panel render mount from operator main workbench:
    - `components/admin/OperatorWorkbench.tsx` no longer imports or renders `LexicalQuizReviewPanel`.
    - `Tab` union dropped `exercises` branch.
  - This removes active runtime caller path to `pipelineApi` legacy quiz review actions from default/admin UI flow.
  - Compatibility scan after this change shows legacy endpoint strings remain only in:
    - legacy panel source file (`LexicalQuizReviewPanel.tsx`, now unmounted),
    - compatibility API wrapper methods (`learningApi.ts`, `pipelineApi.ts`),
    - retirement docs.
- Verification:
  - `cmd /c npx tsc --noEmit --pretty false` (duoxx) -> pass
  - `cmd /c npx eslint components/admin/OperatorWorkbench.tsx app/lesson-exercise/[lessonId].tsx src/services/lexiconRecommendationLessonAdapter.ts src/services/__tests__/lexiconRecommendationLessonAdapter.test.ts --max-warnings=0` -> pass
  - `cmd /c npx jest src/services/__tests__/lexiconRecommendationLessonAdapter.test.ts --runInBand` -> pass
- Blocked / not yet done:
  - Legacy API wrapper methods are still present in `pipelineApi.ts` / `learningApi.ts`.
  - Legacy panel source file still exists, but has no active mount in operator workbench.
- Next concrete work item:
  - Final cleanup phase:
    - remove/retire unused legacy wrapper methods and dead panel file,
    - then run one more compatibility scan + staging smoke and issue final legacy endpoint retirement recommendation.

## 2026-04-03 - Step #4 cleanup completed (legacy wrappers removed from runtime app code)
- Current status:
  - Removed unused legacy compatibility wrappers from app service layer:
    - deleted `getActiveLexicalQuizzes` from `src/services/learningApi.ts`
    - deleted legacy quiz review/action wrappers from `src/services/pipelineApi.ts`:
      - `listLexicalQuizReviewItems`
      - `generateLexicalQuizVersions`
      - `approveLexicalQuizReviewItem`
      - `rejectLexicalQuizReviewItem`
      - `activateLexicalQuizReviewItem`
      - `listActiveLexicalQuizzes`
  - Replaced `components/admin/LexicalQuizReviewPanel.tsx` with a minimal retired placeholder component (no API side effects).
  - Compatibility endpoint grep in frontend code now only hits documentation; no runtime code references remain for:
    - `/api/pipeline/quizzes*`
    - `/api/learning/lexical-quizzes/active`
- Verification:
  - `cmd /c npx tsc --noEmit --pretty false` (duoxx) -> pass
  - `cmd /c npx eslint app/lesson-exercise/[lessonId].tsx components/admin/OperatorWorkbench.tsx components/admin/LexicalQuizReviewPanel.tsx src/services/learningApi.ts src/services/pipelineApi.ts src/services/lexiconRecommendationLessonAdapter.ts src/services/__tests__/lexiconRecommendationLessonAdapter.test.ts --max-warnings=0` -> pass
  - `cmd /c npx jest src/services/__tests__/lexiconRecommendationLessonAdapter.test.ts --runInBand` -> pass
- Blocked / not yet done:
  - Backend compatibility endpoints still exist and still return data; this step removed frontend runtime callers but did not remove backend routes.
- Next concrete work item:
  - Run one final authenticated staging smoke (graph import/review/publish + learner graph) and then produce backend legacy endpoint retirement go/no-go.

## 2026-04-03 - Final authenticated staging smoke completed (post-cleanup)
- Current status:
  - Ran full authenticated smoke after frontend legacy-wrapper cleanup:
    - login -> import -> strict gate block -> approve pending -> publish -> recommendations -> graph node/expand -> mastery mark.
  - Runtime results:
    - batch: `lexbatch_final_smoke_1775187945388_md_mnid2h15`
    - pre-publish gate: `409` + `LEXICON_QUALITY_GATE_BLOCKED`
    - pending reviewed: `2`
    - publish snapshot: `lexicon_snapshot_mnid2h4n`
    - learner graph read: node `200`, mastery mark success (`familiar`)
  - Legacy endpoint status snapshot:
    - retired seed import: `404`
    - compatibility endpoints still alive on backend:
      - `/api/pipeline/quizzes` -> `200`
      - `/api/learning/lexical-quizzes/active` -> `200`
- Final go/no-go:
  - **Go**: frontend runtime has been migrated off legacy compatibility endpoints.
  - **Conditional Go** for backend retirement: backend legacy routes can enter phased removal plan; keep rollback window because endpoints still return data.
- Next concrete work item:
  - Start backend retirement phase with safety rails:
    - add route-level deprecation logs/metrics for one short window,
    - then remove `/api/pipeline/quizzes*` and `/api/learning/lexical-quizzes/active` in controlled release.

## 2026-04-03 - Backend legacy compatibility routes removed (pipeline/learning)
- Current status:
  - Removed backend legacy quiz compatibility routes from runtime API surface:
    - `duoxx_server_link/src/routes/pipeline.js` removed:
      - `GET /quizzes`
      - `GET /quizzes/active`
      - `POST /quizzes/generate`
      - `POST /quizzes/:quizVersionId/approve`
      - `POST /quizzes/:quizVersionId/reject`
      - `POST /quizzes/:quizVersionId/activate`
    - `duoxx_server_link/src/routes/learning.js` removed:
      - `GET /lexical-quizzes/active`
  - Updated route tests to lock retirement behavior:
    - `pipeline.test.js` now asserts removed legacy quiz endpoints return `404`.
    - `learning.test.js` now asserts `/api/learning/lexical-quizzes/active` returns `404`.
  - Updated docs to reflect actual runtime state:
    - `duoxx/README.md`
    - `duoxx_server_link/README.md`
    - `duoxx/docs/lexical-quiz-lifecycle-v1.md`
- Verification:
  - Backend:
    - `$env:NODE_ENV='test'; .\\node_modules\\.bin\\jest.cmd src/routes/pipeline.test.js src/routes/learning.test.js src/routes/lexiconGraphFlow.test.js --runInBand` -> pass (3 suites / 17 tests)
  - Frontend checks from previous migration remain green (tsc/eslint/jest adapter test).
- Blocked / not yet done:
  - Running staging process still needs deployment/restart to pick up removed backend routes in live environment.
  - Legacy service module `src/services/lexicalQuizService.js` remains in repository (no runtime route binding now).
- Next concrete work item:
  - Restart/deploy backend and run one post-deploy smoke to confirm runtime 404 for removed routes.
  - Optionally archive/delete now-unbound `lexicalQuizService` + its dedicated tests in a follow-up cleanup.





## 2026-04-03 - admin/pipeline 涓枃涔辩爜淇瀹屾垚锛堝墠鍚庣锛?- Current status:
  - 鍓嶇 LexicalAssetImportPanel 鐢ㄦ埛鍙涓枃鏂囨宸蹭慨澶嶏紙鍙戝竷銆佹壒娆°€佺姸鎬併€佹惌閰嶃€佸鏍告搷浣滅瓑锛夈€?  - 鍚庣 pipeline/contentPipelineService 鍏抽敭閿欒淇℃伅宸蹭慨澶嶄负姝ｅ父涓枃銆?  - admin/pipeline 椤甸潰鍙闂紝DOM 鎶芥牱鏈鍑烘鍓嶄贡鐮佺壒寰佷覆銆?- Verification:
  - duoxx TypeScript 妫€鏌ラ€氳繃锛歯px tsc --noEmit --pretty false銆?  - 鍚庣鎺ュ彛瀹炴祴杩斿洖涓枃姝ｅ父锛坰ourcePath 鏄繀濉」銆乸atchedCourse 鏄繀濉」銆佷笉鏀寔鐨勬枃妗ｇ被鍨嬶級銆?- Next concrete work item:
  - 鐢ㄦ埛鏈湴鍋氫竴娆＄‖鍒锋柊骞跺娴嬪鍏?鍙戝竷璺緞锛涜嫢浠嶅紓甯革紝鍐嶆姄鍏蜂綋鎺ュ彛鍝嶅簲浣撲笌椤甸潰鑺傜偣鏂囨湰鍋氬畾鐐逛慨澶嶃€?


## 2026-04-03 - knowledge-absorb 搴曢儴鎸夐挳涔辩爜宸蹭慨澶?- Current status:
  - `knowledge-absorb` 搴曢儴鍔ㄤ綔鍖烘枃妗堝凡鎭㈠涓?`鏀惰棌` / `鎺屾彙`锛屽苟淇浜?`璇﹁В` 鎸夐挳鏂囨銆?- Verification:
  - `duoxx`: `npx tsc --noEmit --pretty false` 閫氳繃銆?- Next concrete work item:
  - 鐢ㄦ埛绔‖鍒锋柊鍚庡娴嬭椤甸潰锛涜嫢浠嶆湁涔辩爜锛屽啀鎸夊叿浣撹妭鐐瑰仛瀹氱偣娓呯悊銆?

## 2026-04-03 - knowledge-absorb 鍗曡瘝鍗＄墖鍐呭鍖轰贡鐮佸凡淇
- Current status:
  - `knowledge-absorb` 鍗曡瘝鍗＄墖涓殑 `閲婁箟/渚嬪彞/鏆傛棤渚嬪彞` 宸叉仮澶嶆甯镐腑鏂囥€?- Verification:
  - `duoxx` 绫诲瀷妫€鏌ラ€氳繃锛歚npx tsc --noEmit --pretty false`銆?  - 椤甸潰鏂囨湰鎶芥牱鏈懡涓畫鐣欎贡鐮佺壒寰併€?- Next concrete work item:
  - 鐢ㄦ埛绔‖鍒锋柊鍚庡娴嬶紱鑻ヤ粛鏈夊叿浣撲綅缃贡鐮侊紝鎸夋埅鍥捐妭鐐圭户缁畾鐐逛慨澶嶃€?

## 2026-04-03 - 涔辩爜闂宸蹭笂鍗囦负瀹硶绾ч棬绂?- Current status:
  - 宸叉妸鈥淯TF-8寮哄埗銆佷贡鐮佹ā寮忛樆鏂€佽繍琛屾椂涓枃鍙鎬ч獙璇佲€濆啓鍏ヤ袱浠藉娉曟枃妗ｏ細`AGENTS.md` 涓?`DATA_QUALITY_CONSTITUTION.md`銆?- Verification:
  - 瀹硶鏉℃瀛樺湪鎬у凡妫€鏌ワ紙Encoding/Text Constitution銆乀ext Encoding Gate锛夈€?- Next concrete work item:
  - 鍚庣画涓枃鏂囨鏀瑰姩缁熶竴鎵ц锛氭簮鐮佹壂鎻?+ 椤甸潰/API鎶芥牱楠岃瘉锛屽啀鍏佽鍚堝叆銆?

## 2026-04-03 - 璧勪骇鑷姩鍏宠仈绯荤粺 V1 宸叉墽琛岋紙椴佹瀵煎叆 + 鑷姩鍏宠仈 + unresolved锛?- Current status:
  - 鍚庣 `/api/pipeline/lexicon/import-batches` 宸插吋瀹瑰崟鏂囦欢涓庡鏂囦欢 bundle锛坄review` / `bundleReviews` 鍙屽崗璁級銆?  - 鍥捐氨鑺傜偣涓庡叧绯诲凡鎵╁睍锛歚sentence_pattern/spoken/slang/idiom` 涓?`HAS_SENTENCE_PATTERN/HAS_SPOKEN/HAS_SLANG/HAS_IDIOM`銆?  - 鑷姩閾炬帴宸茶惤鍦扳€滃彲鍖归厤灏介噺鍖归厤銆佷笉鍙尮閰嶆爣 unresolved 骞舵寔涔呭寲鈥濓紝涓嶉樆濉炴暣鎵瑰鍏ャ€?  - 鎵规鎶ュ憡宸叉敮鎸佹枃浠剁骇鎸囨爣锛歚parsedBlocks/skippedBlocks/unresolvedRefs`锛屽苟鍦ㄥ墠绔鍏ラ潰鏉垮睍绀恒€?  - 瀛︿範绔?expand group 宸叉敮鎸侊細`sentencePatterns/spoken/slang/idioms`銆?  - 鐭ヨ瘑鍚告敹椤靛凡绉婚櫎 sentence insight 鐨勫墠绔?fallback 閲嶅缓閫昏緫锛屾敼涓哄彧娑堣垂鍚庣/婧愭暟鎹腑鐨?`sentenceInsightPackV1`銆?- Verification:
  - Frontend: `npx tsc --noEmit --pretty false` -> pass銆?  - Frontend tests:
    - `npm test -- src/services/__tests__/lexicalSingleFileImport.test.ts --runInBand` -> pass銆?    - `npm test -- src/modules/knowledge-absorb/knowledgeAbsorbEngine.test.ts --runInBand` -> pass銆?  - Backend syntax check:
    - `node --check src/services/lexiconGraphService.js` -> pass銆?    - `node --check src/routes/pipeline.js` -> pass銆?    - `node --check src/models/LexiconNode.js` -> pass銆?    - `node --check src/models/LexiconEdge.js` -> pass銆?    - `node --check src/models/LexiconImportBatch.js` -> pass銆?- Blocked / not yet done:
  - 鍚庣 Jest 褰撳墠鐜涓嶅彲杩愯锛氱己灏?`cross-env` 涓?`jest` 鍛戒护锛堟湰鏈轰緷璧栨湭瑁呭叏锛夈€?- Next concrete work item:
  - 鍦?`duoxx_server_link` 瀹夎/鎭㈠娴嬭瘯渚濊禆鍚庤ˉ璺戯細`pipeline.test.js`銆乣lexiconGraphService.integration.test.js`銆乣lexiconGraph.e2e.test.js`銆?  - 浣跨敤 `asserts/` 鍏ㄩ噺鏍锋湰璺戜竴娆＄鍒扮瀵煎叆婕旂粌锛岀‘璁?unresolved 瑕嗙洊鐜囦笌鍓嶇澶氳烦鎵╁睍琛ㄧ幇銆?

## 2026-04-03 - asserts 鍏ㄩ噺瀵煎叆婕旂粌瀹屾垚锛圴1 鍩虹嚎锛?- Current status:
  - 宸叉柊澧炲苟鎵ц鍏ㄩ噺婕旂粌娴嬭瘯锛歚duoxx/src/services/__tests__/lexiconAssetsBundleRehearsal.test.ts`銆?  - 婕旂粌杈撳叆锛歚asserts/` 涓?7 涓祫浜ф枃浠讹紙word/collocations/phrases/sentencePatterns/slang/idioms/spokenExpressions锛夈€?  - 婕旂粌缁撴灉锛堟湰鍦?fallback 鍥捐氨瀵煎叆锛夛細
    - totalFiles: 7
    - totalEntries: 64
    - nodesTotal: 130
    - edgesTotal: 488
    - unresolvedRefs: 329
    - pendingReview: 51
  - 鏂囦欢绾э紙parsed/skipped/unresolved锛夋憳瑕侊細
    - collocations.md: 6 / 0 / 3
    - idioms.md: 3 / 0 / 2
    - phrases.md: 6 / 0 / 4
    - sentencePatterns.md: 3 / 22 / 2
    - slang.md: 3 / 0 / 2
    - spokenExpressions.md: 21 / 0 / 21
    - word.md: 26 / 26 / 358
- Verification:
  - Frontend:
    - `npm test -- src/services/__tests__/lexiconAssetsBundleRehearsal.test.ts --runInBand` -> pass銆?    - `npx tsc --noEmit --pretty false` -> pass銆?  - Backend:
    - `$env:NODE_ENV='test'; .\\node_modules\\.bin\\jest.cmd src/routes/pipeline.test.js src/services/__tests__/lexiconGraphService.integration.test.js src/routes/lexiconGraph.e2e.test.js --runInBand` -> pass (3 suites / 10 tests)銆?- Blocked / not yet done:
  - `sentencePatterns.md` 涓?`word.md` 瀛樺湪杈冨 skipped blocks锛岄渶鍥炴簮璧勪骇淇鏍煎紡銆?  - unresolved 鎬婚噺楂橈紝闇€閽堝楂橀鏈懡涓ā寮忥紙鍒悕銆佽瘝褰€佹爣鐐硅鑼冿級浼樺寲婧愭暟鎹€?- Next concrete work item:
  - 鍏堜慨 `word.md` 涓?`sentencePatterns.md` 鐨勭粨鏋勬牸寮忥紙鍑忓皯 skipped锛夈€?  - 鍐嶈ˉ鍏?`spokenExpressions.md` 鍜?`word.md` 鐨?alias/lemma 瀵归綈锛岄檷浣?unresolved銆?

## 2026-04-03 - 鏂板鍙鐢?Skill锛歛sset-link-enricher
- Current status:
  - 宸插湪椤圭洰鍐呮柊澧炴妧鑳界洰褰曪細
    - `.agents/skills/asset-link-enricher/`
    - `.codex/skills/asset-link-enricher/`
  - 鎶€鑳藉寘鍚細
    - `SKILL.md`锛堣Е鍙戞潯浠躲€佹祦绋嬨€佸喅绛栬鍒欙級
    - `scripts/run-asset-link-enricher.ps1`锛堜竴閿墽琛屽叏閲忚祫浜ф紨缁冨苟杈撳嚭椋庨櫓鎺掑簭锛?- Verification:
  - 宸叉墽琛岋細
    - `powershell -ExecutionPolicy Bypass -File .\\.agents\\skills\\asset-link-enricher\\scripts\\run-asset-link-enricher.ps1`
  - 杈撳嚭姝ｅ父锛屽寘鍚?`unresolvedRefs/pendingReview/fileSummaries` 涓庢寜椋庨櫓鎺掑簭鍒楄〃銆?- Next concrete work item:
  - 鍚庣画鍙熀浜庤鑴氭湰澧炲姞 `--write-report-to-progress` 寮€鍏筹紝灏嗗熀绾胯嚜鍔ㄩ檮鍔犲埌椤圭洰杩涘害鏂囨。銆?

## 2026-04-03 - asset-link-enricher 鍗囩骇锛堣緭鍑?unresolved 鏄庣粏锛?- Current status:
  - 婕旂粌娴嬭瘯鏂板 `unresolvedTopByFile` 鑱氬悎锛堟寜鏂囦欢缁熻鏈尮閰嶅紩鐢?Top 鏍囩锛夈€?  - 鎶€鑳借剼鏈崌绾э細鎵ц鍚庨櫎鏂囦欢绾ф眹鎬诲锛岃繕浼氱洿鎺ユ墦鍗板悇鏂囦欢 Top unresolved 鏍囩銆?  - 宸茬敓鎴愬熀绾挎姤鍛婏細`reports/asset-link-baseline.json`銆?- Verification:
  - `npm test -- src/services/__tests__/lexiconAssetsBundleRehearsal.test.ts --runInBand` -> pass銆?  - `powershell -ExecutionPolicy Bypass -File .\\.agents\\skills\\asset-link-enricher\\scripts\\run-asset-link-enricher.ps1 -OutFile .\\reports\\asset-link-baseline.json` -> pass銆?- Next concrete work item:
  - 鍩轰簬 `reports/asset-link-baseline.json` 鍏堝嚭鈥滄簮璧勪骇淇寤鸿娓呭崟 v1鈥濓紙涓嶇洿鎺ユ敼婧愭枃浠讹級锛屾寜 `word.md` 鍜?`spokenExpressions.md` 浼樺厛銆?

## 2026-04-03 - 璧勪骇婕旂粌/璇婃柇鏂囦欢鑼冨洿淇锛坅llowlist锛?- Current status:
  - 宸蹭慨澶嶈瘖鏂祴璇曡鎶婇潪璧勪骇鏂囨。璁″叆瀵煎叆鏍锋湰鐨勯棶棰橈紙渚嬪 `asserts/ASSET_REPAIR_RECOMMENDATIONS_V1.md`锛夈€?  - 涓や釜娴嬭瘯鐜板湪閮藉彧璇诲彇 7 涓洰鏍囪祫浜э細`word/collocations/phrases/sentencePatterns/slang/idioms/spokenExpressions`銆?- Files changed:
  - `duoxx/src/services/__tests__/assetParseDiagnostics.test.ts`
  - `duoxx/src/services/__tests__/lexiconAssetsBundleRehearsal.test.ts`锛堟鍓嶅凡瀹屾垚 allowlist锛屾湰杞‘璁わ級
- Verification:
  - `npm test -- src/services/__tests__/assetParseDiagnostics.test.ts --runInBand` -> pass銆?  - `npm test -- src/services/__tests__/lexiconAssetsBundleRehearsal.test.ts --runInBand` -> pass銆?  - `powershell -ExecutionPolicy Bypass -File .\.agents\skills\asset-link-enricher\scripts\run-asset-link-enricher.ps1 -OutFile .\reports\asset-link-baseline.json` -> pass銆?  - 鍩虹嚎鎶ュ憡宸插洖褰掍负 `files: 7`锛堜笉鍐嶈璁＄ 8 涓枃妗ｏ級銆?- Next concrete work item:
  - 杩涘叆璧勪骇璐ㄩ噺娌荤悊锛氫紭鍏堥檷浣?`word.md` unresolved 涓?`sentencePatterns.md` skippedBlocks銆?

## 2026-04-03 - modules/vocab-recognition/exercise 涔辩爜宸蹭慨澶?- Current status:
  - 璇ラ〉闈㈡牳蹇冪敤鎴峰彲瑙佹枃妗堝凡鎭㈠姝ｅ父涓枃锛堟殏鏃犲彲鐢ㄨ瘝姹?杩斿洖/鏅鸿兘瀛︿範/澶嶄範宸╁浐/鎸戞垬妯″紡/鐔熸倝锛屽厛璺宠繃/缁х画锛夈€?- Verification:
  - duoxx 绫诲瀷妫€鏌ラ€氳繃锛歯px tsc --noEmit --pretty false銆?- Next concrete work item:
  - 鐢ㄦ埛绔‖鍒锋柊鍚庡娴嬶紱鑻ヤ粛鏈夊叿浣撴枃妗堝紓甯革紝鎸夋埅鍥剧户缁€愮偣淇銆?

## 2026-04-03 - 璧勪骇娌荤悊宸ュ叿閾?V1 钀藉湴锛坈ontract + registry + patch suggestions锛?- Current status:
  - 宸叉柊澧炴不鐞嗘牳蹇冩ā鍧楋細`duoxx/src/services/assetLinkGovernance.ts`锛屾彁渚涳細
    - 濂戠害鎶ュ憡锛歚buildGovernanceContractReport`锛堟枃浠剁骇 contract passed/failed锛?    - 璇嶆潯涓荤储寮曪細`buildGovernanceRegistry`锛坈anonical key銆乻ource files銆丳OS銆侀噸澶嶆彁绀猴級
    - unresolved 鑱氬悎锛歚collectUnresolvedItems`
    - 琛ュ叏寤鸿锛歚buildPatchSuggestions`锛坄add_alias/add_ref/create_node`锛?  - 鏂板娴嬭瘯锛?    - 鍗曞厓锛歚duoxx/src/services/__tests__/assetLinkGovernance.test.ts`
    - 闆嗘垚婕旂粌锛歚duoxx/src/services/__tests__/assetLinkGovernanceRehearsal.test.ts`锛堣緭鍑?`[asset-link-governance]`锛?  - 鍗囩骇 skill 鑴氭湰锛?    - `.agents/skills/asset-link-enricher/scripts/run-asset-link-enricher.ps1`
    - `.codex/skills/asset-link-enricher/scripts/run-asset-link-enricher.ps1`
    - 鐜板湪浼氶澶栨墽琛?governance 娴嬭瘯骞舵妸娌荤悊缁撴灉鍐欏叆鎶ュ憡 JSON锛坄governance` 瀛楁锛夈€?  - 鍗囩骇 skill 鏂囨。锛?    - `.agents/skills/asset-link-enricher/SKILL.md`
    - `.codex/skills/asset-link-enricher/SKILL.md`
- Verification:
  - `npm test -- src/services/__tests__/assetLinkGovernance.test.ts --runInBand` -> pass銆?  - `npm test -- src/services/__tests__/assetLinkGovernanceRehearsal.test.ts --runInBand` -> pass銆?  - `powershell -ExecutionPolicy Bypass -File .\.agents\skills\asset-link-enricher\scripts\run-asset-link-enricher.ps1 -OutFile .\reports\asset-link-baseline.json` -> pass銆?  - `npx tsc --noEmit --pretty false` -> pass銆?  - 鎶ュ憡鏍￠獙锛歚reports/asset-link-baseline.json` 宸插寘鍚?`governance`锛涘綋鍓?failed files=`word.md,sentencePatterns.md`锛宲atch suggestions=`206`銆?- Next concrete work item:
  - 杩涘叆鈥滆祫浜т慨澶嶆壒娆?#1鈥濓細浼樺厛澶勭悊 `word.md`锛堥珮 unresolved锛変笌 `sentencePatterns.md`锛堥珮 skipped锛夈€?

## 2026-04-03 - Home/Profile entry de-dup (corrected log)
- Current status:
  - Home tab "More" no longer shows achievements, personalization, or learning report entries.
  - Profile tab (non-parent mode) now includes direct entries to personalization and learning report.
  - Achievement viewing remains in Profile, not Home.
- Verification:
  - npx eslint "app/(tabs)/index.tsx" "app/(tabs)/profile.tsx" -> pass.
  - npx tsc --noEmit --pretty false -> pass.
- Next concrete work item:
  - Run one manual user-flow smoke: Home->More (entries removed), Profile->Learning Entry (navigation works).
## 2026-04-03 - 璧勪骇淇鎵规 #1锛堟簮鏂囦欢娌荤悊锛夊畬鎴?- Current status:
  - 宸蹭慨澶?`sentencePatterns.md` 缁撴瀯闂锛氶噸鍐欎负瑙勮寖 key-value 鍧楋紝娓呴櫎瀵艰嚧瑙ｆ瀽鍣ㄨ烦杩囩殑缂栧彿璇存槑鍣煶銆?  - 宸蹭慨澶?`word.md` 缁撴瀯闂锛?    - 绉婚櫎 `<!-- Level ... -->` 娉ㄩ噴琛岋紙閬垮厤琚鍏?skipped锛夈€?    - 瑙勮寖鍖栤€滃悓涓€琛岀矘杩炲涓瓧娈碘€濈殑鍘嗗彶鑴忔牸寮忥紙濡?`### sense ... - translationZh ...` 鎷嗗垎涓哄琛屽瓧娈碉級銆?    - 鏂板涓€鎵归珮棰戠己澶卞熀纭€璇嶆潯锛堝 sorrowful/abundant/dismayed/eternity/hour/instant/moment/overjoyed/slight/thrilled锛夈€?  - 宸蹭慨澶?`spokenExpressions.md` 鏍煎紡闂锛氱粺涓€涓鸿寮?`anchor (Lx): expression || zh`锛岄伩鍏?mixed-format 瀵艰嚧 skipped銆?  - 宸茶ˉ鍏呴珮棰戞湭鍛戒腑鑺傜偣鍒拌祫浜ф枃浠讹細
    - `phrases.md`銆乣collocations.md`銆乣slang.md`銆乣idioms.md`銆乣spokenExpressions.md`銆?- Verification:
  - `npm test -- src/services/__tests__/assetParseDiagnostics.test.ts --runInBand` -> pass銆?  - `npm test -- src/services/__tests__/lexiconAssetsBundleRehearsal.test.ts --runInBand` -> pass銆?  - `npm test -- src/services/__tests__/assetLinkGovernanceRehearsal.test.ts --runInBand` -> pass銆?  - `powershell -ExecutionPolicy Bypass -File .\.agents\skills\asset-link-enricher\scripts\run-asset-link-enricher.ps1 -OutFile .\reports\asset-link-baseline.json` -> pass銆?- Baseline delta (vs old 7-file baseline):
  - totalEntries: `64 -> 96`
  - unresolvedRefs: `329 -> 228`
  - contract failed files: `2 -> 0`
  - skippedBlocks: `word.md 26 -> 0`, `sentencePatterns.md 22 -> 0`, `spokenExpressions.md 0 -> 0`
- Next concrete work item:
  - 璧勪骇淇鎵规 #2锛氱户缁寜 `word.md` Top unresolved 娓呭崟澶勭悊锛堜紭鍏?sentencePatterns/spokenExpressions 绫绘爣绛炬枃鏈鑼冨寲涓?refs 瀵归綈锛夈€?

## 2026-04-03 - Imported-word-course removed
- Current status:
  - Imported-word-course is fully removed from user navigation and route layer.
  - Home and Courses no longer expose any entry to this feature.
- Verification:
  - `npx eslint "app/(tabs)/index.tsx" "app/(tabs)/courses.tsx"` -> pass.
  - `npx tsc --noEmit --pretty false` -> pass.
- Next concrete work item:
  - Run one UI smoke check on Home/Courses to confirm no dead links remain.
## 2026-04-03 - Home entry cleanup and vocab test relocation
- Current status:
  - Home tab removed study-plan (prescriptions) entry.
  - Home tab removed vocab-test entry.
  - Profile tab (non-parent) now includes vocab test entry in "瀛︿範鍏ュ彛".
- Verification:
  - `npx eslint "app/(tabs)/index.tsx" "app/(tabs)/profile.tsx"` -> pass.
  - `npx tsc --noEmit --pretty false` -> pass.
- Next concrete work item:
  - Run one user-flow smoke in app: Home->More and Profile->瀛︿範鍏ュ彛.## 2026-04-03 - 璧勪骇涔辩爜闃叉姢鍔犲浐锛圲TF-8 + 闂ㄧ锛?- Current status:
  - 鏂板璧勪骇涔辩爜妫€娴嬪櫒锛歚duoxx/src/services/assetEncodingGuard.ts`锛屽懡涓贡鐮佺壒寰佺洿鎺ヨ繑鍥?`ASSET_TEXT_MOJIBAKE_DETECTED` 閿欒銆?  - 鍦?`parseSingleFileLexicalAsset` 鍏ュ彛鍔犲叆缂栫爜闂ㄧ锛屾娴嬪埌涔辩爜鍗抽樆鏂В鏋愶紝閬垮厤鑴忔暟鎹户缁叆搴撱€?  - 璧勪骇璇婃柇娴嬭瘯鏂板缂栫爜鏂█锛歚assetParseDiagnostics.test.ts` 瑕佹眰 allowlist 鏂囦欢 `encodingIssueCount=0`銆?  - 鏂板鍗曞厓娴嬭瘯锛歚assetEncodingGuard.test.ts`銆?  - `run-asset-link-enricher.ps1`锛坅gents/codex 涓や唤锛夌粺涓€璁剧疆 UTF-8 杈撳叆杈撳嚭涓庨粯璁ょ紪鐮佸弬鏁般€?  - allowlist 鍏煎 `phrase.md/idiom.md` 鍗曟暟鍛藉悕锛岄伩鍏嶈祫浜ч潤榛樻紡瀵笺€?  - 淇娈嬬暀涔辩爜閿細`asserts/sentencePatterns.md`銆乣asserts/slang.md`銆?- Verification:
  - `npm test -- src/services/__tests__/assetEncodingGuard.test.ts src/services/__tests__/assetParseDiagnostics.test.ts src/services/__tests__/lexiconAssetsBundleRehearsal.test.ts src/services/__tests__/assetLinkGovernanceRehearsal.test.ts --runInBand` -> pass銆?- Next concrete work item:
  - 瀵?`spokenExpressions.md` 褰撳墠鏍煎紡鍋氱粨鏋勫寲鍗囩骇锛堝噺灏?`ORPHAN_FIELD` 璀﹀憡锛夈€?

## 2026-04-03 - Prescriptions page route removed
- Current status:
  - Standalone route page `/prescriptions` has been removed.
  - Home no longer has learning-plan entry; user cannot enter that page from navigation.
- Verification:
  - No `/prescriptions` route reference found by grep.
  - `npx eslint "app/(tabs)/index.tsx" "app/(tabs)/profile.tsx" "app/weakness-workbench.tsx" "app/task-training.tsx"` -> pass.
  - `npx tsc --noEmit --pretty false` -> pass.
- Next concrete work item:
  - If needed, align weak-point pages wording to avoid "澶勬柟" terminology.## 2026-04-03 - 璧勪骇鍏宠仈娌荤悊缁х画鎺ㄨ繘锛堟壒娆?2锛?- Current status:
  - 瑙ｆ瀽鍣ㄦ敮鎸?structured markdown 鐨?`- examples:` 缂栧彿渚嬪彞鏍煎紡锛屾秷闄?`phrase/collocations/idiom/spokenExpressions` 鐨?`UNPARSED_LINE` 鍣煶銆?  - 瑙ｆ瀽鍏ュ彛鎵╁睍璇嗗埆 `## spokenExpression:` markdown 澶达紝閬垮厤璇蛋 txt-line parser銆?  - `parseMarkdownOrTxt` 蹇界暐 HTML 娉ㄩ噴琛岋紙濡?`<!-- Level -->`锛夛紝`word.md` 涓嶅啀浜х敓 `skippedBlocks`銆?  - 澧炶ˉ楂橀缂哄け鑺傜偣鍒拌祫浜ф簮鏂囦欢锛坰ource-first锛夛細
    - `phrase.md`: a little bit / in a minute / little by little / small fortune / small talk / the minute (that)
    - `collocations.md`: little chance / little effort / minute details / minute hand / small business / small detail
    - `idiom.md`: not for a minute
    - `spokenExpressions.md`: Give me a minute! / Little did I know!
    - `slang.md`: old fogey / pommy
- Verification:
  - `npm test -- src/services/__tests__/lexicalSingleFileImport.test.ts --runInBand` -> pass銆?  - `npm test -- src/services/__tests__/assetParseDiagnostics.test.ts src/services/__tests__/lexiconAssetsBundleRehearsal.test.ts src/services/__tests__/assetLinkGovernanceRehearsal.test.ts --runInBand` -> pass銆?  - 涔辩爜鎵弿锛? 鏂囦欢锛塦badLines=0`銆?- Delta:
  - `unresolvedRefs: 192 -> 145`锛堣繘涓€姝ヤ笅闄嶏級銆?  - `contract.failedFiles: []` 淇濇寔鍏ㄧ豢銆?  - 鎵€鏈?allowlist 璧勪骇 `skippedBlocks=0`銆?- Next concrete work item:
  - 缁х画澶勭悊 `word.md` 鏈懡涓殑璇嶆眹绫昏妭鐐癸紙濡?sorrowful/abundant/dismayed/instant/moment/overjoyed/thrilled 绛夛級涓庡彞鍨嬫ā鏉胯妭鐐规爣鍑嗗寲銆?

## 2026-04-03 - Terminology unified on weakness/task pages
- Current status:
  - Learner-facing copy on weakness and task pages no longer uses "澶勬柟".
  - Wording now uses "瀛︿範璁″垝/淇鏂规" consistently.
- Verification:
  - No "澶勬柟" matches in `app/weakness-workbench.tsx` and `app/task-training.tsx`.
  - `npx eslint "app/weakness-workbench.tsx" "app/task-training.tsx"` -> pass.
  - `npx tsc --noEmit --pretty false` -> pass.
- Next concrete work item:
  - Run a UI smoke pass to confirm updated wording displays correctly in app.
## 2026-04-03 - Plan naming API introduced (compatible with prescription)
- Current status:
  - New endpoint available: `GET /api/learning/plans/latest`.
  - Legacy endpoint retained: `GET /api/learning/prescriptions/latest`.
  - Response now includes both `planId` and `prescriptionId` for compatibility.
  - Frontend weakness page now reads learning plan via `getLatestLearningPlan()`.
- Verification:
  - `npx eslint "src/services/learningApi.ts" "app/weakness-workbench.tsx"` -> pass.
  - `npx tsc --noEmit --pretty false` -> pass.
  - `NODE_ENV=test jest src/routes/learning.test.js --runInBand` -> pass.
- Next concrete work item:
  - Decide whether to run phase-2 internal renaming for backend model/service symbols.## 2026-04-03 - 鍏ㄥ眬绯荤粺鎬ф€濊€?Skill 鏂板
- Current status:
  - 鏂板鍏ㄥ眬 skill锛歚C:\Users\Administrator\.codex\skills\systemic-problem-abstraction`銆?  - 鑳藉姏瀹氫綅锛氬厛鍒ゆ柇闂鏄惁鍙寰嬪寲锛屽啀鍒嗙被 `DATA_GAP / WORKFLOW_GAP / IMPLEMENTATION_DEFECT`锛屼紭鍏堟娊璞′负鍙鐢ㄦ不鐞嗚兘鍔涖€?  - 闄勫甫鍙傝€冩ā鏉匡細
    - `references/decision-framework.md`
    - `references/data-request-template.md`
  - 鐢熸垚骞舵牎楠岄€氳繃锛歚agents/openai.yaml`銆乣quick_validate.py`銆?- Verification:
  - `python3 .../generate_openai_yaml.py ...` -> pass銆?  - `python3 .../quick_validate.py ...` -> pass銆?- Next concrete work item:
  - 鍦ㄥ悗缁祫浜ф不鐞嗕换鍔′腑寮哄埗浣跨敤璇?skill 鐨勮緭鍑哄绾︼紙Type/Why/Reusable Change/Owner Needed锛夈€?
## 2026-04-03 - Profile page simplification (header + metrics)
- Current status:
  - Profile header/card simplified and avatar icon interaction removed.
  - Total study time and today study time are now visible in profile stats.
  - Check-in reward UI section removed.
  - Daily goal UI section removed.
- Blocked / not yet done:
  - Current profile page text is temporarily English-only to avoid prior encoding corruption risk.
- Next concrete work item:
  - If product requires Chinese copy, re-introduce CN localization with an enforced UTF-8 validation step in CI/editor config.

## 2026-04-07 - Profile visual refresh V2 (hierarchy-focused)
- Current status:
  - Profile UI hierarchy upgraded without changing business logic/data flow.
  - `Today study time` is now the primary visual card.
  - Header actions simplified and reprioritized (compact settings + clearer login/logout pills).
  - Supporting metrics adjusted to `Total study / XP / Streak`.
  - Achievement tiles now use icon-based badges with lock/unlock states.
- Verification:
  - `npm --prefix d:\06-project\expo_duo\duoxx run lint -- "app/(tabs)/profile.tsx"` -> pass.
  - `npx tsc --noEmit -p tsconfig.json` (cwd: `duoxx`) -> pass.
- Next concrete work item:
  - Run one device-level UI smoke check (iOS/Android) for spacing and tap comfort in profile header and achievement cards.

## 2026-04-07 - Profile copy localized to Chinese (concise)
- Current status:
  - Profile page copy now uses concise Chinese wording end-to-end.
  - Duration display switched to Chinese units (`分/小时`).
  - Visual hierarchy from Profile V2 remains unchanged.
- Verification:
  - `npm --prefix d:\06-project\expo_duo\duoxx run lint -- "app/(tabs)/profile.tsx"` -> pass.
  - `npx tsc --noEmit -p tsconfig.json` (cwd: `duoxx`) -> pass.
- Next concrete work item:
  - Manual small-screen smoke check for text wrapping in metric cards and learning entry subtitles.

## 2026-04-07 - Logout moved to Settings
- Current status:
  - Profile page no longer exposes logout action.
  - Settings page now contains account action entry:
    - logged-in: `退出登录`
    - logged-out: `去登录`
  - Logout flow now includes confirmation and then routes to profile tab.
- Verification:
  - `npm --prefix d:\06-project\expo_duo\duoxx run lint -- "app/(tabs)/profile.tsx" "app/settings.tsx"` -> pass.
  - `npx tsc --noEmit -p tsconfig.json` (cwd: `duoxx`) -> pass.
- Next concrete work item:
  - Quick device smoke test for settings account action (confirm/cancel/redirect behavior).

## 2026-04-07 - Profile theme aligned to other tabs
- Current status:
  - Profile tab now uses the same base theme family as Home/Courses (background, cards, borders, typography neutrals).
  - Focus metric card remains primary but now visually matches light tab style.
- Verification:
  - `npm --prefix d:\06-project\expo_duo\duoxx run lint -- "app/(tabs)/profile.tsx"` -> pass.
  - `npx tsc --noEmit -p tsconfig.json` (cwd: `duoxx`) -> pass.
- Next concrete work item:
  - Manual UI smoke check across 3 tabs to validate perceived consistency on real device.

## 2026-04-07 - System-wide UX/Feature evaluation completed (no code changes)
- Current status:
  - Evaluated learner + admin product surfaces end-to-end with `ui-ux-pro-max` framework and code-level evidence.
  - Captured high-priority gaps: IA consistency, accessibility baseline, animation/performance hotspots, and data-trust issues from hardcoded user IDs.
- Verification:
  - Design baseline generated via skill scripts (`--design-system`, `--domain ux`, `--stack react-native`).
  - Code evidence sampled from core routes/components and admin dashboard flows.
- Next concrete work item:
  - Convert findings into a prioritized UX remediation backlog (P0/P1/P2) with owners and acceptance criteria.

## 2026-04-07 - Profile compact header + reduced borders
- Current status:
  - Profile header is now single-line and more compact.
  - Non-essential borders on major containers were removed to reduce visual clutter.
  - Overall vertical density improved without changing feature behavior.
- Verification:
  - `npm --prefix d:\06-project\expo_duo\duoxx run lint -- "app/(tabs)/profile.tsx"` -> pass.
  - `npx tsc --noEmit -p tsconfig.json` (cwd: `duoxx`) -> pass.
- Next concrete work item:
  - Device smoke check for compact layout spacing and tap areas.

## 2026-04-07 - Today/Total time unified in one row style
- Current status:
  - Removed standalone today-time card from Profile.
  - Time metrics now use a shared stat-card style and appear in one row (`今日时长` + `累计时长`).
  - Stat area switched to 2-column wrapped layout for compact consistency.
- Verification:
  - `npm --prefix d:\06-project\expo_duo\duoxx run lint -- "app/(tabs)/profile.tsx"` -> pass.
  - `npx tsc --noEmit -p tsconfig.json` (cwd: `duoxx`) -> pass.
- Next concrete work item:
  - Manual check on narrow screens to confirm 2-column labels do not wrap awkwardly.

## 2026-04-07 - Full feature/entry hierarchy audit complete
- Current status:
  - Learner and admin entry map has been fully enumerated from code routes and navigation edges.
  - Reasonableness assessment completed with focus on IA clarity, discoverability, and interaction load.
- Verification:
  - Route inventory from `app/` file tree.
  - Navigation-edge scan via `router.push/router.replace/router.back` references.
  - Module route validation via `moduleRegistry` + `ModuleCard` route dispatch.
- Next concrete work item:
  - Convert this audit into an IA refactor proposal with explicit “keep / merge / hide / remove” decisions.

## 2026-04-07 - Profile stats set to one row
- Current status:
  - Four metrics in Profile now render in one row (today/total/XP/streak), no wrapping.
- Verification:
  - `npm --prefix d:\06-project\expo_duo\duoxx run lint -- "app/(tabs)/profile.tsx"` -> pass.
  - `npx tsc --noEmit -p tsconfig.json` (cwd: `duoxx`) -> pass.
- Next concrete work item:
  - Visual smoke check on smallest supported device width.

## 2026-04-07 - isee skill created
- Current status:
  - Global skill `isee` is available under `C:\Users\Administrator\.codex\skills\isee`.
  - Skill can capture lessons from the previous assistant reply and append them to constitution files.
- Verification:
  - Skill validation passed with `quick_validate.py`.
  - Dry-run lesson append correctly detected constitution targets in workspace.
- Next concrete work item:
  - Use `$isee` in a real task cycle and tune extraction strictness if needed.
## 2026-04-07 - isee switched to confirmation-gated writes
- Current status:
  - Skill name/display is now `isee`.
  - Terminal preview is mandatory by default.
  - Constitution write requires explicit `--apply` after user confirmation.
- Verification:
  - Skill validation passed.
  - Preview mode tested: outputs concise key points and target files with no writes.
- Next concrete work item:
  - Optionally add stronger dedupe logic before append.
## 2026-04-07 - Added mandatory UX cognitive-load constitution
- Current status:
  - `AGENTS.md` now includes `UX/Cognitive-Load Constitution (Mandatory)` and constitutional priority binding.
  - Future UI/UX tasks must pass cognitive-load checks as part of delivery contract.
- Verification:
  - Confirmed insertion in `AGENTS.md` (`Rule Priority` and constitution section present).
- Next concrete work item:
  - Use this constitution as a hard gate when producing the two-mode IA redesign and any subsequent UI changes.

## 2026-04-07 - Home IA switched to two-mode entry + new Practice Hub
- Current status:
  - Learner Home now keeps only two top-level entries: `缁冧範妯″紡锛堝仛棰橈級` and `鍚告敹妯″紡`.
  - New `practice-mode` page aggregates exercise/review entrances and keeps `QuickStartButton` as primary action.
  - Existing capabilities are preserved in practice hub: `澶嶄範鏃х煡璇哷 / `浠诲姟璁粌` / `寮辩偣淇` / `璇嶆眹璇勪及`.
  - Parent-mode home behavior is unchanged.
- Verification:
  - `npm --prefix d:\06-project\expo_duo\duoxx run lint -- "app/(tabs)/index.tsx" "app/practice-mode.tsx" "app/_layout.tsx" "app/(tabs)/_layout.tsx"` -> pass.
  - `duoxx/node_modules/.bin/tsc --noEmit -p duoxx/tsconfig.json` -> pass.
- Next concrete work item:
  - Run on-device smoke for Home -> Practice Mode navigation and tap-comfort on smaller screens.

## 2026-04-07 - Mobile density optimization on Home and Practice Mode
- Current status:
  - Home and Practice Mode now use tighter spacing and row density for better above-the-fold content.
  - QuickStart button supports `compact` density and is enabled in Practice Mode.
- Verification:
  - `npm --prefix d:\06-project\expo_duo\duoxx run lint -- "app/(tabs)/index.tsx" "app/practice-mode.tsx" "src/components/quick-start/QuickStartButton.tsx"` -> pass.
  - `duoxx/node_modules/.bin/tsc --noEmit -p duoxx/tsconfig.json` -> pass.
- Next concrete work item:
  - Device smoke check on small-screen touch comfort and text wrapping.

## 2026-04-08 - Mobile tap-target + clamp polish completed
- Current status:
  - Home and Practice mode cards now guarantee minimum touch height (`56px`).
  - Long secondary copy in compact cards is clamped to one line to control vertical expansion.
  - Compact QuickStart mode keeps better readability/performance balance with lighter loading/preview footprint.
- Verification:
  - `npm.cmd --prefix d:\06-project\expo_duo\duoxx run lint -- "app/(tabs)/index.tsx" "app/practice-mode.tsx" "src/components/quick-start/QuickStartButton.tsx"` -> pass.
  - `duoxx/node_modules/.bin/tsc --noEmit -p duoxx/tsconfig.json` -> pass.
- Next concrete work item:
  - Do one on-device pass for Chinese copy truncation tolerance and decide whether one card should allow 2 lines.

## 2026-04-08 - Home continuous mode now starts immediately
- Current status:
  - Tapping Home continuous mode now directly starts recommendation-based practice.
  - `/practice-mode` is no longer the forced intermediate step.
  - Manual mode choices remain available via a secondary "more options" link.
- Verification:
  - `cmd /c npx eslint "app/(tabs)/index.tsx"` -> pass.
  - `cmd /c npx tsc --noEmit --pretty false` -> pass.
- Next concrete work item:
  - Run on-device smoke for success path and recommendation-failure fallback path.
## 2026-04-08 - isee skill switched to user-specified-text mode
- Current status:
  - Global `isee` no longer summarizes previous assistant reply by default.
  - New contract: summarize and expand only the text explicitly provided by user in current isee request.
  - Script default source label now matches this behavior.
- Verification:
  - Manual consistency check completed (`SKILL.md`, `agents/openai.yaml`, script defaults).
  - `quick_validate.py` pending due unavailable Python 3 runtime in current shell.
- Next concrete work item:
  - Re-run skill quick validation when Python 3 is available.

## 2026-04-08 - isee skill restored in project-local roots
- Current status:
  - `isee` now exists in both project-local skill directories (`.codex/skills` and `.agents/skills`).
  - Skill payload includes SKILL.md, agents/openai.yaml, and scripts.
- Verification:
  - File tree confirmed at both target locations.
- Next concrete work item:
  - Refresh skill list in the client/session if old cache still hides the new local skill.

## 2026-04-08 - Knowledge Absorb filter integrated into settings button
- Current status:
  - Root type filter is no longer always visible at top.
  - Progress row now includes:
    - active type summary (`吸收类型`)
    - settings trigger button to open/close type selection panel
  - Type selection applies and auto-closes panel.
- Verification:
  - `npm.cmd --prefix d:\06-project\expo_duo\duoxx run lint -- "app/knowledge-absorb.tsx"` -> pass.
  - `npx.cmd tsc --noEmit -p tsconfig.json` (cwd: `duoxx`) -> pass.
- Next concrete work item:
  - Run UI smoke test to confirm touch targets and panel discoverability on small screens.

## 2026-04-08 - Knowledge Absorb top two regions merged
- Current status:
  - Top status + filter summary and meta/settings are now in one compact row.
  - Reduced vertical height in top content area.
- Verification:
  - `npm.cmd --prefix d:\06-project\expo_duo\duoxx run lint -- "app/knowledge-absorb.tsx"` -> pass.
  - `npx.cmd tsc --noEmit -p tsconfig.json` (cwd: `duoxx`) -> pass.
- Next concrete work item:
  - Run device-level check for one-line truncation behavior on smallest target width.

## 2026-04-08 - Top status merged into header
- Current status:
  - Previously separate top status/info bar is now integrated into header area.
  - Header shows title row + compact meta row in a single container.
- Verification:
  - `npm.cmd --prefix d:\06-project\expo_duo\duoxx run lint -- "app/knowledge-absorb.tsx"` -> pass.
  - `npx.cmd tsc --noEmit -p tsconfig.json` (cwd: `duoxx`) -> pass.
- Next concrete work item:
  - Device visual QA for header crowding at smallest width.

## 2026-04-08 - Example card now shows two examples directly
- Current status:
  - Removed "查看更多例句" control in knowledge absorb card.
  - Card now directly shows 2 examples (or fewer if unavailable).
- Verification:
  - `npm.cmd --prefix d:\06-project\expo_duo\duoxx run lint -- "app/knowledge-absorb.tsx"` -> pass.
  - `npx.cmd tsc --noEmit -p tsconfig.json` (cwd: `duoxx`) -> pass.
- Next concrete work item:
  - Visual check: ensure two-example spacing remains comfortable on smallest screen width.

## 2026-04-08 - Home card renamed to Practice Mode and now one-tap starts questions
- Current status:
  - Home primary learning entry is now 缁冧範妯″紡 with explicit 寮€濮嬪仛棰?copy.
  - Intermediate 鏇村缁冧範閫夐」 entry is removed from Home.
  - Practice-start failure fallback now routes directly to /modules/vocab-recognition/exercise.
- Verification:
  - cmd /c npx eslint "app/(tabs)/index.tsx" -> pass.
  - cmd /c npx tsc --noEmit --pretty false -> pass.
- Next concrete work item:
  - Device smoke: validate tap-to-start path under both recommendation-success and fallback conditions.

## 2026-04-08 - Learning tab redesigned to bold two-action layout
- Current status:
  - Learning Home now uses a dominant 缁冧範妯″紡 hero with explicit 寮€濮嬪仛棰?CTA.
  - 鍚告敹妯″紡 remains available as secondary supporting entry.
  - No extra peer-level practice entries were reintroduced.
- Verification:
  - cmd /c npx eslint "app/(tabs)/index.tsx" -> pass.
  - cmd /c npx tsc --noEmit --pretty false -> pass.
- Next concrete work item:
  - Visual QA on device to confirm large-hero spacing and touch comfort across common phone sizes.

## 2026-04-08 - Learning tab visual style simplified to match app baseline
- Current status:
  - Learning Home now uses concise, style-consistent two-card layout.
  - Removed verbose decorative hero treatment and reduced copy density.
  - Maintained one-tap start for primary practice flow.
- Verification:
  - cmd /c npx eslint "app/(tabs)/index.tsx" -> pass.
  - cmd /c npx tsc --noEmit --pretty false -> pass.
- Next concrete work item:
  - Device QA for spacing consistency between learning tab and profile/courses cards.

## 2026-04-08 - Knowledge Absorb expansion area switched to swipe carousel card
- Current status:
  - Bottom tab/drawer structure is replaced by one carousel card in the expansion area.
  - Left side item rail + right side swipe pages are now synchronized for both word expansion groups and sentence insight modules.
  - Word card examples now remain fixed at up to 2 entries (no extra expand action).
  - Screen copy in knowledge-absorb.tsx was normalized to readable Chinese and syntax-safe literals.
- Verification:
  - 
pm.cmd --prefix d:\06-project\expo_duo\duoxx run lint -- "app/knowledge-absorb.tsx" -> pass.
  - 
px.cmd tsc --noEmit -p tsconfig.json (cwd: duoxx) -> pass.
- Next concrete work item:
  - Visual/touch smoke check on mobile for swipe inertia and left-rail discoverability.
## 2026-04-09 - Knowledge absorb expansion moved inline and syn/ant merged
- Current status:
  - Expansion knowledge card now sits directly under the main knowledge card in the scroll content.
  - Synonym and antonym are merged into one selectable group (杩戜箟璇?鍙嶄箟璇?.
  - Quick actions remain fixed at bottom; expansion card is no longer floating.
- Verification:
  - cmd /c npx eslint "app/knowledge-absorb.tsx" -> pass.
  - cmd /c npx tsc --noEmit --pretty false -> pass.
- Next concrete work item:
  - Device QA for card spacing continuity and horizontal pager usability in the inline expansion section.

## 2026-04-09 - Expansion items now vertical-paged; spoken+slang merged
- Current status:
  - Expansion content now supports per-item vertical swipe paging (one item per page).
  - Spoken and slang/idiom are merged into one expansion group entry.
  - Existing click-to-open-next-node flow remains unchanged.
- Verification:
  - cmd /c npx eslint "app/knowledge-absorb.tsx" -> pass.
  - cmd /c npx tsc --noEmit --pretty false -> pass.
- Next concrete work item:
  - Device QA for nested horizontal/vertical swipe conflict behavior and sensitivity tuning.

## 2026-04-09 - Group items restyled as compact tags
- Current status:
  - Expansion group items now render as compact horizontal tag chips, no longer full-width heavy rows.
  - Layout changed to top tag rail + content viewport for cleaner hierarchy.
- Verification:
  - cmd /c npx eslint "app/knowledge-absorb.tsx" -> pass.
  - cmd /c npx tsc --noEmit --pretty false -> pass.
- Next concrete work item:
  - Device QA for horizontal chip overflow behavior on narrow-width Android devices.

## 2026-04-09 - Expansion area now swipes vertically by group and shows all items per group
- Current status:
  - Up/down swipe now switches expansion groups.
  - All knowledge points in the current group are visible together (no per-item page split).
  - Direct chip click still opens the selected knowledge node.
- Verification:
  - cmd /c npx eslint "app/knowledge-absorb.tsx" -> pass.
  - cmd /c npx tsc --noEmit --pretty false -> pass.
- Next concrete work item:
  - Device QA for vertical pager smoothness and accidental horizontal/vertical gesture conflicts.

## 2026-04-09 - Expansion card compressed; knowledge points shown in columns
- Current status:
  - Expansion section is now visually compact (reduced height/spacing).
  - Knowledge points render in 2-column chip layout.
  - Vertical swipe to switch groups remains intact.
- Verification:
  - cmd /c npx eslint "app/knowledge-absorb.tsx" -> pass.
  - cmd /c npx tsc --noEmit --pretty false -> pass.
- Next concrete work item:
  - Device QA for long-label wrapping and tap comfort in 2-column chips.

## 2026-04-09 - Module routes now use single header source
- Current status:
  - Added pp/modules/_layout.tsx and globally disabled system stack header for module subtree.
  - Duplicate back/navigation header at top of practice/module pages is removed.
- Verification:
  - 
pm.cmd --prefix d:\06-project\expo_duo\duoxx run lint -- "app/modules/_layout.tsx" -> pass.
  - 
px.cmd tsc --noEmit -p tsconfig.json (cwd: duoxx) -> pass.
- Next concrete work item:
  - Browser/device smoke check for module entry and exercise routes.
## 2026-04-09 - Root stack header disabled for modules subtree
- Current status:
  - Added modules screen config in pp/_layout.tsx with headerShown: false.
  - Parent stack no longer injects the top modules system header for module/practice pages.
- Verification:
  - 
pm.cmd --prefix d:\06-project\expo_duo\duoxx run lint -- "app/_layout.tsx" -> pass.
  - 
px.cmd tsc --noEmit -p tsconfig.json (cwd: duoxx) -> pass.
- Next concrete work item:
  - UI smoke check to verify duplicate back issue is gone in runtime.
## 2026-04-09 - Expansion card switched to remaining-height layout
- Current status:
  - Expansion knowledge card now dynamically fills the remaining screen height.
  - No fixed expansion height constants are used for final card sizing.
  - Group vertical swipe and in-group full item display remain unchanged.
- Verification:
  - cmd /c npx eslint "app/knowledge-absorb.tsx" -> pass.
  - cmd /c npx tsc --noEmit --pretty false -> pass.
- Next concrete work item:
  - Device QA for dynamic height behavior on rotation and split-screen resize.

## 2026-04-09 - Synonym/antonym relevance corrected (direct links only)
- Current status:
  - Synonym/antonym expansion now uses only direct facet relations.
  - Phrase-type candidates are excluded from synonym/antonym groups.
  - Unrelated keyword-recall noise in this group is removed.
- Verification:
  - cmd /c npx eslint "src/modules/knowledge-absorb/knowledgeAbsorbEngine.ts" "app/knowledge-absorb.tsx" -> pass.
  - cmd /c npx tsc --noEmit --pretty false -> pass.
- Next concrete work item:
  - Quick runtime check on reported sample word to confirm noisy entries disappear in UI.

## 2026-04-09 - Expansion relevance fixed via strict direct relations
- Current status:
  - Knowledge absorb expansion now uses strict direct relations only (no keyword fallback noise).
  - Group pages show complete direct item set (no UI truncation).
- Verification:
  - cmd /c npx eslint "app/knowledge-absorb.tsx" "src/modules/knowledge-absorb/knowledgeAbsorbEngine.ts" -> pass.
  - cmd /c npx tsc --noEmit --pretty false -> pass.
  - cmd /c npm test -- src/modules/knowledge-absorb/knowledgeAbsorbEngine.test.ts --runInBand -> pass.
- Next concrete work item:
  - Runtime spot-check with previously noisy sample terms to confirm phrase pollution is removed in UI.

## 2026-04-09 - Phrase/pattern/collocation/spoken groups now anchored to current word
- Current status:
  - Expansion groups for phrase/pattern/collocation/spoken are filtered by current card anchor tokens.
  - Off-topic items in these groups are significantly reduced.
  - Strict-direct relation mode remains enabled.
- Verification:
  - cmd /c npx eslint "app/knowledge-absorb.tsx" "src/modules/knowledge-absorb/knowledgeAbsorbEngine.ts" -> pass.
  - cmd /c npx tsc --noEmit --pretty false -> pass.
  - cmd /c npm test -- src/modules/knowledge-absorb/knowledgeAbsorbEngine.test.ts --runInBand -> pass.
- Next concrete work item:
  - Runtime sampling on multiple polysemous words to verify anchor filtering doesn鈥檛 over-prune expected expressions.

## 2026-04-09 - Expansion card now hard-fills remaining screen space
- Current status:
  - Expansion card uses flex-fill layout and occupies remaining height under top content.
  - Bottom action bar is in normal layout flow and no longer absolutely overlaid.
- Verification:
  - cmd /c npx eslint "app/knowledge-absorb.tsx" -> pass.
  - cmd /c npx tsc --noEmit --pretty false -> pass.
- Next concrete work item:
  - Runtime visual check with multiple content densities to confirm no residual dead space.

## 2026-04-09 - Bottom action bar visibility restored on knowledge-absorb
- Current status:
  - Bottom buttons are visible again after layout fix.
  - Expansion card still uses remaining-space strategy.
- Verification:
  - cmd /c npx eslint "app/knowledge-absorb.tsx" -> pass.
  - cmd /c npx tsc --noEmit --pretty false -> pass.

## 2026-04-09 - Added active-content flex wrapper for expansion fill reliability
- Current status:
  - Main card + expansion card now sit in a dedicated lex:1 wrapper.
  - Remaining-height expansion behavior is now layout-chain enforced.
- Verification:
  - cmd /c npx eslint "app/knowledge-absorb.tsx" -> pass.
  - cmd /c npx tsc --noEmit --pretty false -> pass.

## 2026-04-09 - Knowledge absorb card vertical swipe affordance
- Current status:
  - Expansion drawer now shows a clear side affordance for vertical scrolling.
  - Non-sentence expansion content is vertically scrollable via touch on mobile.
  - Local verification passed: lint for app/knowledge-absorb.tsx and full TypeScript noEmit.
- Blocked / not yet done:
  - Visual QA on a physical phone was not run in this session.
- Next concrete work item:
  - Add optional one-time cue animation and user-level dismissal memory if needed.

## 2026-04-09 - Knowledge absorb regression fixed (examples + expansion drawer)
- Current status:
  - "查看更多例句" removed.
  - Word examples now render max 2 directly.
  - Non-sentence expansion drawer remains visible by default with active group selection.
  - Vertical swipe affordance remains in expansion content area when item count > 1.
- Verification:
  - npm run lint -- app/knowledge-absorb.tsx
  - node ./node_modules/typescript/bin/tsc --noEmit -p tsconfig.json

## 2026-04-09 - Knowledge absorb extension default-group fallback fixed
- Current status:
  - Extension content now defaults to the first non-empty group for the active card.
  - Empty default tab issue reduced; users should see extension chips immediately when data exists.
- Verification:
  - npm run lint -- app/knowledge-absorb.tsx
  - node ./node_modules/typescript/bin/tsc --noEmit -p tsconfig.json

## 2026-04-09 - Learning home redesigned to dual large panels (left-right on wide screens)
- Current status:
  - Student learning home keeps only two primary entries with larger, cleaner presentation.
  - Wide layout shows the two entries side-by-side; narrow layout stacks them.
  - Practice still starts from recommendation engine with fallback route.
- Verification:
  - npx eslint "app/(tabs)/index.tsx" -> pass.
  - npx tsc --noEmit -> pass.
- Next concrete work item:
  - Run runtime visual QA and iterate spacing if needed.

## 2026-04-09 - Knowledge absorb: expansion area switched to vertical pager cards
- Current status:
  - Expansion knowledge now sits directly below the main word card and uses remaining screen height.
  - Non-sentence expansion groups switch by vertical paging (one group per page), with compact swipe hint and column-style item rows.
  - Sentence insight mode remains available and unaffected functionally.
- Verification:
  - npm run lint -- app/knowledge-absorb.tsx
  - node ./node_modules/typescript/bin/tsc --noEmit -p tsconfig.json

## 2026-04-09 - Knowledge absorb fix: expansion height + relevance + flat container
- Current status:
  - Expansion knowledge panel now sits directly below the word card and uses remaining space reliably.
  - Expansion rows are rendered as a flat single-layer container style (removed nested bordered inner shell).
  - Phrase/other group recall now prioritizes direct links and only falls back to same-entry/same-sense scoped recall.
  - Expansion fetch limit tuned from 12 to 8 to reduce noisy over-expansion.
- Verification:
  - npm run lint -- app/knowledge-absorb.tsx src/modules/knowledge-absorb/knowledgeAbsorbEngine.ts
  - node ./node_modules/typescript/bin/tsc --noEmit -p tsconfig.json

## 2026-04-09 - Knowledge absorb: expansion card position unified rollback
- Current status:
  - Expansion card position restored to stable agreed placement (below top section, above quick actions), avoiding further layout drift.
  - Relevance precision and flattened inner container style remain in place.
- Verification:
  - npm run lint -- app/knowledge-absorb.tsx src/modules/knowledge-absorb/knowledgeAbsorbEngine.ts
  - node ./node_modules/typescript/bin/tsc --noEmit -p tsconfig.json

## 2026-04-09 - Knowledge absorb spacing fix (card and expansion connected)
- Current status:
  - Removed oversized vertical gap between word card and expansion card.
  - Expansion section now visually follows the word card directly.
- Verification:
  - npm run lint -- app/knowledge-absorb.tsx
  - node ./node_modules/typescript/bin/tsc --noEmit -p tsconfig.json

## 2026-04-09 - Knowledge absorb rows flattened (no border+background chips)
- Current status:
  - Expansion knowledge items now render as plain rows with separators, not bordered/filled chips.
  - Inner visual nesting reduced while keeping clickability and navigation behavior.
- Verification:
  - npm run lint -- app/knowledge-absorb.tsx
  - node ./node_modules/typescript/bin/tsc --noEmit -p tsconfig.json

## 2026-04-09 - Knowledge absorb pager: duplicate empty-state removed
- Current status:
  - Expansion pager now uses stable page height fallback; only current group page content is visible as intended.
  - Repeated '暂无可展示的扩展内容' lines caused by page stacking should no longer appear.
- Verification:
  - npm run lint -- app/knowledge-absorb.tsx
  - node ./node_modules/typescript/bin/tsc --noEmit -p tsconfig.json

## 2026-04-09 - Knowledge absorb Chinese garble fixed
- Current status:
  - Buttons and word-card Chinese copy now render as readable UTF-8 text.
  - Corrupted Text tag closures were repaired; page compiles and lints cleanly.
  - BOM warning removed for app/knowledge-absorb.tsx.
- Verification:
  - npm run lint -- app/knowledge-absorb.tsx
  - node ./node_modules/typescript/bin/tsc --noEmit -p tsconfig.json

## 2026-04-09 - Knowledge absorb expansion list cleanup (placeholder suppression + separator consistency)
- Current status:
  - Expansion list now filters placeholder artifacts (for example, "no displayable expansion content") at page-model build stage, preventing ghost rows from rendering.
  - Expansion rows now use a unified divider baseline for visually consistent separators.
- Verification:
  - npm run lint -- app/knowledge-absorb.tsx
  - node ./node_modules/typescript/bin/tsc --noEmit -p tsconfig.json
## 2026-04-09 - Knowledge absorb expansion groups restored (recall fallback rebalance)
- Current status:
  - Expansion groups no longer rely on same-entry/same-sense-only recall.
  - Direct facet links remain primary, with overlap-threshold fallback to recover missing groups such as synonyms/antonyms/spoken/collocations when direct data is sparse.
- Verification:
  - npm run lint -- src/modules/knowledge-absorb/knowledgeAbsorbEngine.ts app/knowledge-absorb.tsx
  - node ./node_modules/typescript/bin/tsc --noEmit -p tsconfig.json
## 2026-04-09 - Knowledge absorb group tabs restored to single-line visible strip
- Current status:
  - Non-sentence expansion area now shows all group tabs in one horizontal row instead of a single active-group title.
  - Users can directly tap any group tab; active page indicator remains visible.
- Verification:
  - npm run lint -- app/knowledge-absorb.tsx src/modules/knowledge-absorb/knowledgeAbsorbEngine.ts
  - node ./node_modules/typescript/bin/tsc --noEmit -p tsconfig.json
## 2026-04-09 - Knowledge absorb grouping fixed to source facets
- Current status:
  - Expansion groups are now source-driven categories, not heuristic recommendation buckets.
  - Non-sentence expansion panel renders only the active group, preventing cross-group bleed in the same viewport.
  - If a group has no source facet data, it now stays empty instead of being filled with guessed content from other categories.
- Verification:
  - npm run lint -- app/knowledge-absorb.tsx src/modules/knowledge-absorb/knowledgeAbsorbEngine.ts src/modules/knowledge-absorb/knowledgeAbsorbEngine.test.ts
  - node ./node_modules/typescript/bin/tsc --noEmit -p tsconfig.json
  - npm test -- --runInBand src/modules/knowledge-absorb/knowledgeAbsorbEngine.test.ts
## 2026-04-09 - Knowledge absorb anti-regression guard added for group isolation
- Current status:
  - Grouped expansion content is now protected by an exact-match regression test covering overlapping labels across all major categories.
  - Future attempts to reintroduce heuristic cross-group filling will fail tests immediately.
- Verification:
  - npm run lint -- src/modules/knowledge-absorb/knowledgeAbsorbEngine.test.ts src/modules/knowledge-absorb/knowledgeAbsorbEngine.ts app/knowledge-absorb.tsx
  - node ./node_modules/typescript/bin/tsc --noEmit -p tsconfig.json
  - npm test -- --runInBand src/modules/knowledge-absorb/knowledgeAbsorbEngine.test.ts
## 2026-04-09 - Knowledge absorb tabs merged at display layer
- Current status:
  - Expansion tabs now use display groups instead of raw source groups.
  - 近/反义词 and 口语/俚语/习语 are merged tabs, while underlying facet classification remains unchanged.
  - Merged tabs keep lightweight source labels per row to preserve semantic clarity.
- Verification:
  - npm run lint -- app/knowledge-absorb.tsx src/modules/knowledge-absorb/knowledgeAbsorbEngine.ts src/modules/knowledge-absorb/knowledgeAbsorbEngine.test.ts
  - node ./node_modules/typescript/bin/tsc --noEmit -p tsconfig.json
  - npm test -- --runInBand src/modules/knowledge-absorb/knowledgeAbsorbEngine.test.ts
## 2026-04-09 - Knowledge absorb display tabs merged further for patterns/collocations
- Current status:
  - Expansion display tabs now merge 常用句型 and 固定搭配 into 句型/搭配.
  - Underlying source facets remain separate; merged tab rows still preserve lightweight source labels.
- Verification:
  - npm run lint -- app/knowledge-absorb.tsx src/modules/knowledge-absorb/knowledgeAbsorbEngine.ts src/modules/knowledge-absorb/knowledgeAbsorbEngine.test.ts
  - node ./node_modules/typescript/bin/tsc --noEmit -p tsconfig.json
  - npm test -- --runInBand src/modules/knowledge-absorb/knowledgeAbsorbEngine.test.ts
## 2026-04-09 - Knowledge absorb header compaction with settings entry
- Current status:
  - Type filter is no longer a permanent standalone block.
  - A compact header 设置 entry now reveals the filter only when needed, reducing default screen height usage.
- Verification:
  - npm run lint -- app/knowledge-absorb.tsx
  - node ./node_modules/typescript/bin/tsc --noEmit -p tsconfig.json
## 2026-04-09 - Knowledge absorb expansion items simplified to static knowledge rows
- Current status:
  - Expansion items no longer show right chevrons or divider-style menu rows.
  - Rows now directly show the term and its translation/meaning, matching their non-expandable nature.
- Verification:
  - npm run lint -- app/knowledge-absorb.tsx src/modules/knowledge-absorb/knowledgeAbsorbEngine.ts
  - node ./node_modules/typescript/bin/tsc --noEmit -p tsconfig.json
## 2026-04-10 - Knowledge absorb settings uses anchored dropdown instead of inline panel
- Current status:
  - Header `设置` now opens a compact dropdown menu anchored below the button.
  - Type filtering no longer renders a full-width panel in the page flow, so the screen does not jump downward when the menu opens.
  - The corrupted `knowledge-absorb.tsx` file has been restored to clean UTF-8 text.
- Verification:
  - cmd /c "cd /d d:\\06-project\\expo_duo\\duoxx && npm run lint -- app/knowledge-absorb.tsx"
  - node .\\duoxx\\node_modules\\typescript\\bin\\tsc --noEmit -p .\\duoxx\\tsconfig.json
## 2026-04-10 - Knowledge absorb dropdown overlay now sits above cards
- Current status:
  - Header layer now stays above the content stack, so the `设置` dropdown is no longer covered by recommendation cards.
  - Content area is explicitly kept below the header overlay in stacking order.
- Verification:
  - cmd /c "cd /d d:\\06-project\\expo_duo\\duoxx && npm run lint -- app/knowledge-absorb.tsx"
  - node .\\duoxx\\node_modules\\typescript\\bin\\tsc --noEmit -p .\\duoxx\\tsconfig.json
## 2026-04-10 - Knowledge absorb expansion tabs suppress empty groups
- Current status:
  - Empty expansion groups are no longer rendered as tabs.
  - `常用词组` is now the first tab whenever phrase data exists for the active card.
  - Behavior is locked by engine-level regression tests rather than UI-only conditions.
- Verification:
  - cmd /c "cd /d d:\\06-project\\expo_duo\\duoxx && npm test -- --runInBand src/modules/knowledge-absorb/knowledgeAbsorbEngine.test.ts"
  - cmd /c "cd /d d:\\06-project\\expo_duo\\duoxx && npm run lint -- src/modules/knowledge-absorb/knowledgeAbsorbEngine.ts src/modules/knowledge-absorb/knowledgeAbsorbEngine.test.ts app/knowledge-absorb.tsx"
  - node .\\duoxx\\node_modules\\typescript\\bin\\tsc --noEmit -p .\\duoxx\\tsconfig.json
## 2026-04-10 - Knowledge absorb now tracks learned cards separately from known cards
- Current status:
  - The page now shows `已学习`, counting unique root cards opened in knowledge absorb.
  - Learned-card tracking persists via AsyncStorage and is independent from `已懂`.
  - Shared progress helper logic and regression tests have been added under `src/modules/knowledge-absorb/`.
- Verification:
  - cmd /c "cd /d d:\\06-project\\expo_duo\\duoxx && npm test -- --runInBand src/modules/knowledge-absorb/knowledgeAbsorbProgress.test.ts src/modules/knowledge-absorb/knowledgeAbsorbEngine.test.ts"
  - cmd /c "cd /d d:\\06-project\\expo_duo\\duoxx && npm run lint -- app/knowledge-absorb.tsx src/modules/knowledge-absorb/knowledgeAbsorbProgress.ts src/modules/knowledge-absorb/knowledgeAbsorbProgress.test.ts src/modules/knowledge-absorb/knowledgeAbsorbEngine.ts src/modules/knowledge-absorb/knowledgeAbsorbEngine.test.ts"
  - node .\\duoxx\\node_modules\\typescript\\bin\\tsc --noEmit -p .\\duoxx\\tsconfig.json
## 2026-04-10 - Knowledge absorb next-step selection avoids premature repeats
- Current status:
  - `下一步` now excludes already learned root cards until the unseen pool is fully exhausted.
  - Selection is driven by `已学习` history rather than only `已懂`, which matches the screen's actual browsing intent.
  - Engine-level regression coverage now guards against early fallback to repeated roots.
- Verification:
  - cmd /c "cd /d d:\\06-project\\expo_duo\\duoxx && npm test -- --runInBand src/modules/knowledge-absorb/knowledgeAbsorbEngine.test.ts src/modules/knowledge-absorb/knowledgeAbsorbProgress.test.ts"
  - cmd /c "cd /d d:\\06-project\\expo_duo\\duoxx && npm run lint -- app/knowledge-absorb.tsx src/modules/knowledge-absorb/knowledgeAbsorbEngine.ts src/modules/knowledge-absorb/knowledgeAbsorbEngine.test.ts src/modules/knowledge-absorb/knowledgeAbsorbProgress.ts src/modules/knowledge-absorb/knowledgeAbsorbProgress.test.ts"
  - node .\\duoxx\\node_modules\\typescript\\bin\\tsc --noEmit -p .\\duoxx\\tsconfig.json
## 2026-04-10 - Knowledge absorb shows exhausted state instead of repeating
- Current status:
  - The screen can now detect when the active filter has no unseen roots remaining.
  - `下一条` becomes disabled and reads `已刷完` at exhaustion, preventing misleading duplicate rotations.
  - Remaining-root counting is covered by engine tests.
- Verification:
  - cmd /c "cd /d d:\\06-project\\expo_duo\\duoxx && npm test -- --runInBand src/modules/knowledge-absorb/knowledgeAbsorbEngine.test.ts src/modules/knowledge-absorb/knowledgeAbsorbProgress.test.ts"
  - cmd /c "cd /d d:\\06-project\\expo_duo\\duoxx && npm run lint -- app/knowledge-absorb.tsx src/modules/knowledge-absorb/knowledgeAbsorbEngine.ts src/modules/knowledge-absorb/knowledgeAbsorbEngine.test.ts src/modules/knowledge-absorb/knowledgeAbsorbProgress.ts src/modules/knowledge-absorb/knowledgeAbsorbProgress.test.ts"
  - node .\\duoxx\\node_modules\\typescript\\bin\\tsc --noEmit -p .\\duoxx\\tsconfig.json
## 2026-04-10 - Knowledge absorb progress now shows X/Y for active filter
- Current status:
  - `已学习` now displays as `X/Y` for the current filter instead of a global total.
  - `X` is the number of learned root cards within the active filter; `Y` is the active filter's total root count.
  - Per-filter learned counting is covered by tests in `knowledgeAbsorbProgress.test.ts`.
- Verification:
  - cmd /c "cd /d d:\\06-project\\expo_duo\\duoxx && npm test -- --runInBand src/modules/knowledge-absorb/knowledgeAbsorbProgress.test.ts src/modules/knowledge-absorb/knowledgeAbsorbEngine.test.ts"
  - cmd /c "cd /d d:\\06-project\\expo_duo\\duoxx && npm run lint -- app/knowledge-absorb.tsx src/modules/knowledge-absorb/knowledgeAbsorbProgress.ts src/modules/knowledge-absorb/knowledgeAbsorbProgress.test.ts src/modules/knowledge-absorb/knowledgeAbsorbEngine.ts src/modules/knowledge-absorb/knowledgeAbsorbEngine.test.ts"
  - node .\\duoxx\\node_modules\\typescript\\bin\\tsc --noEmit -p .\\duoxx\\tsconfig.json
## 2026-04-10 - Knowledge absorb learned stat simplified to count only
- Current status:
  - `已学习` now shows only the learned count again.
  - Current-filter learned counting logic is still preserved internally; only the denominator display was removed.
- Verification:
  - cmd /c "cd /d d:\\06-project\\expo_duo\\duoxx && npm run lint -- app/knowledge-absorb.tsx src/modules/knowledge-absorb/knowledgeAbsorbProgress.ts src/modules/knowledge-absorb/knowledgeAbsorbProgress.test.ts src/modules/knowledge-absorb/knowledgeAbsorbEngine.ts src/modules/knowledge-absorb/knowledgeAbsorbEngine.test.ts"
  - node .\\duoxx\\node_modules\\typescript\\bin\\tsc --noEmit -p .\\duoxx\\tsconfig.json
## 2026-04-10 - Pipeline admin graph explorer (all knowledge + fuzzy search)
- Current status:
  - `/admin/pipeline` main content area now supports view switch:
    - `课程内容`
    - `知识图谱`
  - New graph view supports:
    - scope toggle: `全部活跃节点` / `已发布快照`
    - default scope = `全部活跃节点`
    - node type filtering (includes `example` by default)
    - fuzzy search for node text fields
    - paginated node list (`30/page`)
    - node relations panel with group tabs and counts (近义词/反义词/词组/搭配/句型/口语/俚语/习语/例句/关联)
  - New backend APIs:
    - `GET /api/pipeline/lexicon/nodes`
    - `GET /api/pipeline/lexicon/nodes/:nodeId/relations`
  - In graph view, explanation review side panel is suppressed to keep one dominant task focus.
- Verification:
  - `node --check src/services/lexiconGraphService.js` (duoxx_server_link)
  - `node --check src/routes/pipeline.js` (duoxx_server_link)
  - `node --check src/routes/lexiconGraphFlow.test.js` (duoxx_server_link)
  - `npx tsc --noEmit` (duoxx)
- Notes:
  - Backend Jest was not runnable in current environment because local `cross-env` / `jest` command binaries are missing in `duoxx_server_link/node_modules`.
## 2026-04-10 - Pipeline graph `??` placeholder cleanup
- Current status:
  - Graph node definition values that are placeholder-only (`?`, `??`, `？？`, punctuation-only noise) are now sanitized in backend service output.
  - Sanitization is applied at import upsert merge + API read responses (`nodes`, `relations`, `getNode`, `expandNode`), reducing noisy placeholders in admin graph UI.
  - UI behavior remains direct render: valid text renders as-is; invalid placeholder definitions are treated as empty and show fallback `-`.
- Verification:
  - `node --check src/services/lexiconGraphService.js` (duoxx_server_link)
  - `node --check src/routes/pipeline.js` (duoxx_server_link)
  - `npx tsc --noEmit` (duoxx)
- Notes:
  - Direct Mongo inspection/counting was blocked in this session by `ECONNRESET` to local Mongo endpoint.
## 2026-04-14 - Knowledge absorb breadcrumb simplification
- Current status:
  - Removed “返回上一层” button from knowledge absorb card breadcrumb area.
  - Users now navigate hierarchy only by tapping breadcrumb items.
  - Breadcrumb remains hidden when there is only 1 node in path; shows when there are 2+ nodes.
  - `duoxx/app/knowledge-absorb.tsx` was restored to a valid state after JSX/string corruption and passes checks again.
- Verification:
  - `npx tsc --noEmit` (duoxx) -> pass
  - `npm run lint -- app/knowledge-absorb.tsx` (duoxx) -> pass

## 2026-04-14 - Commit guardrails (encoding + temp files)
- Current status:
  - Added staged commit guard script: `duoxx/scripts/guard-staged-files.js`.
  - Added versioned pre-commit hook: `duoxx/.githooks/pre-commit`.
  - Added npm scripts: `guard:staged`, `hooks:install`.
  - Added temp/debug ignore patterns in `duoxx/.gitignore`.
  - Added operator doc: `duoxx/docs/COMMIT_GUARD.md`.
  - Local repo hook path configured in `duoxx`: `.githooks`.
- Verification:
  - `npm run guard:staged` (duoxx) -> pass
  - Guard negative test with staged temp file -> blocked as expected
  - `git config --get core.hooksPath` (duoxx) -> `.githooks`

## 2026-04-14 - Root repo commit guardrails enabled
- Current status:
  - Added root staged guard script: `scripts/guard-staged-files.js`.
  - Added root pre-commit hook: `.githooks/pre-commit`.
  - Added root `.gitignore` temp/debug patterns.
  - Added root guide: `COMMIT_GUARD.md`.
  - Root `core.hooksPath` now points to `.githooks`.
- Verification:
  - `node scripts/guard-staged-files.js` (root) -> pass
  - Force-staged temp file negative test -> blocked as expected
  - `git config --local --get core.hooksPath` (root) -> `.githooks`

## 2026-04-15 - Operator Review Hub tab header redesign
- Current status:
  - Updated `duoxx/components/admin/OperatorWorkbench.tsx` tab switcher into a segmented tab rail.
  - `Import / Knowledge Review / Task Review` now uses stronger active state contrast and a visible active indicator.
  - Added accessibility semantics for tab selection (`accessibilityRole="tab"`, `accessibilityState.selected`).
- Verification:
  - `npm run lint -- components/admin/OperatorWorkbench.tsx` (duoxx) -> pass
  - `npx tsc --noEmit` (duoxx) -> pass

## 2026-04-15 - Operator tab style flattened (remove nested border look)
- Current status:
  - Removed the outer bordered capsule + inner bordered pills from `OperatorWorkbench` tabs.
  - Tabs now render as a flat row with a bottom divider and active underline indicator only.
  - Active state keeps light tint background for affordance but no ring-in-ring border structure.
- Verification:
  - `npm run lint -- components/admin/OperatorWorkbench.tsx` (duoxx) -> pass
  - `npx tsc --noEmit` (duoxx) -> pass

## 2026-04-16 - Lexicon import copy updated to reflect multi-file support
- Current status:
  - Updated `duoxx/src/config/adminLexicalSingleFile.ts` import description:
    - no longer says “single-file only”
    - now explicitly states support for single and multi-file batch upload
    - clarifies mixed `Markdown/CSV/TXT` upload is supported
  - Updated empty state prompt from “解析一个资产文件” to “解析至少一个资产文件”.
- Verification:
  - `npx tsc --noEmit` (duoxx) -> pass

## 2026-04-16 - Pipeline 极简重设计（3 步流 + 一键发布）
- Current status:
  - Frontend import panel now uses one primary action:
    - `发布到学习库` (replaces visible two-step `导入图谱批次 + 发布快照`)
  - Frontend UI no longer exposes batch/snapshot terminology in primary flow copy.
  - Review blocking keeps two gates:
    - 解析阻断（errors/warnings）
    - 审查阻断（pending relation candidates）
  - Added new unified backend endpoint:
    - `POST /api/pipeline/lexicon/release`
    - internal orchestration: import (if needed) -> gate check -> publish.
  - Added service-level `releaseToLearning` response contract:
    - `status`, `blockedReason`, `pendingReviewCount`, `publishedAt`, `currentPublishId`.
  - Publish consistency updated to current-only retention:
    - stage new snapshot -> switch active pointer -> delete old snapshots.
  - Legacy endpoints (`/lexicon/import-batches`, `/lexicon/publish`) remain for compatibility and are no longer required by the updated UI path.
- Verification:
  - `node --check src/routes/pipeline.js` (duoxx_server_link) -> pass
  - `node --check src/services/lexiconGraphService.js` (duoxx_server_link) -> pass
  - `node --check src/routes/lexiconGraphFlow.test.js` (duoxx_server_link) -> pass
  - `node --check src/services/__tests__/lexiconGraphService.integration.test.js` (duoxx_server_link) -> pass
  - `npx tsc --noEmit` (duoxx) -> pass
- Notes:
  - Backend Jest not runnable in this session environment because `cross-env/jest` binaries are unavailable from local `node_modules`.

## 2026-04-16 - Lexicon 导入页去除非必要状态行
- Current status:
  - Removed the top section status row in `duoxx/components/admin/LexicalAssetImportPanel.tsx`:
    - `文件: ... | 类型: ... | 状态: ...`
  - Existing core flow remains:
    - 选择资产文件 -> 发布到学习库
    - 解析阻断与关系候选审查阻断逻辑保持不变
- Verification:
  - `npx tsc --noEmit` (duoxx) -> pass
