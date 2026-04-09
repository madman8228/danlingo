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
  - 瀵煎叆璇嶆眹娴忚锟?is now visible in /(tabs)/courses under the default ll category and routes to /imported-word-course.
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
  - Exercise Review now uses a single primary action: 锟斤拷准锟斤拷锟斤拷效.
  - Already-active questions no longer show a second activation button; they display 锟斤拷前锟斤拷 instead.
- Blocked / not yet done:
  - The backend still keeps separate approve/activate endpoints internally; the simplification is currently a UI-level orchestration.
- Next concrete work item:
  - Decide whether the backend should gain a dedicated pprove-and-activate endpoint or whether the current UI composition is sufficient.
## 2026-03-20 - Exercise Review semantic simplification
- Current status:
  - Exercise Review no longer exposes 锟斤拷锟斤拷锟斤拷 / 锟斤拷态锟斤拷 / 锟斤拷前锟芥本 in the operator UI.
  - The panel now groups by 锟斤拷锟斤拷 on the left and shows all exercises under the selected sense on the right.
  - The generic 锟斤拷锟缴猴拷选 action has been replaced with explicit 锟斤拷锟斤拷选锟斤拷锟斤拷 and 锟斤拷锟斤拷锟叫讹拷锟斤拷 actions.
- Blocked / not yet done:
  - Backend data still keeps quiz versioning internally; the UI now hides that model instead of deleting it.
  - Learning-side quiz consumption still has not switched to the active lexical quiz endpoint.
- Next concrete work item:
  - Run a browser smoke test for /admin/pipeline -> Exercise Review, then decide whether 锟斤拷为锟斤拷效锟斤拷 should be auto-triggered on approve.
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
- 锟绞伙拷锟斤拷锟斤拷锟斤拷锟斤拷锟秸匡拷为系统锟斤拷锟缴ｏ拷`锟斤拷锟斤拷选锟斤拷锟斤拷 / 锟叫讹拷锟斤拷`锟斤拷

## Done
- Single-file import and review page is live in `/admin/pipeline`.
- Word/phrase headwords, multiple senses, translated facets, and translated examples are supported.
- 锟劫凤拷锟斤拷锟侥硷拷模锟斤拷锟斤拷锟斤拷只锟斤拷锟斤拷知识锟绞诧拷锟街段ｏ拷锟斤拷锟斤拷示锟斤拷锟斤拷写 quiz锟斤拷
- Seed quizzes can now be persisted from lexical review into backend Mongo collections.
- Generated quiz versions, active quiz bindings, and stale marking are now implemented in backend Mongo collections, with local AsyncStorage fallback still kept as a dev safety net.
- `Exercise Review` now hosts the lexical quiz version review panel with `Seed / Generated / Active / Stale` filters and approve/reject/activate/generate actions.
- Vocab lesson routes now prefer `/api/learning/lexical-quizzes/active` for `multiple_choice` and `true_false` quiz playback, with automatic fallback to the existing lesson payload when no usable active lexical quiz exists.
- The main admin page no longer exposes the old V4 multi-file import flow by default.
- `lexical-quiz-lifecycle-v1.md` now defines where dynamic quiz updates should be stored and how admins should review them.
- Progress tracking is now mandatory in both `PROJECT_MEMORY.md` and `PROJECT_PROGRESS.md`.
- The unused V4 lexical import implementation and its test/config files have been removed from the Expo repo.
- Backend learning route now exposes `/api/learning/lexical-quizzes/active` for current active lexical quiz reads.
- `Exercise Review` 锟斤拷锟斤拷锟斤拷锟斤拷 `锟斤拷锟缴凤拷锟斤拷选锟斤拷锟斤拷 / 锟斤拷锟斤拷锟叫讹拷锟斤拷`锟斤拷锟斤拷锟劫帮拷 `word_card` 锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟酵★拷
- 学习锟斤拷锟斤拷锟斤拷式支锟斤拷 `translation_choice`锟斤拷legacy `word_card / multiple_choice` 锟斤拷锟节讹拷取时锟斤拷锟斤拷迁锟狡★拷

## Not Done
- 学习锟剿伙拷没锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟绞匡拷锟斤拷锟斤拷锟絗translation_choice` 锟皆革拷锟斤拷锟斤拷锟斤拷选锟斤拷锟斤拷锟斤拷锟斤拷锟?- There is still legacy candidate-review code in the repo outside the current lexical quiz review path; it is bypassed but not fully deleted.
- The frontend still keeps local lexical quiz storage as fallback; once backend stability is confirmed, that fallback can be reduced or removed.

## Next Steps
- Decide whether the learner should keep reusing the current multiple-choice renderer for `translation_choice` or gain a dedicated lexical-card layout.
- Decide whether to keep or remove the frontend local lexical quiz fallback after backend smoke testing.
- Remove or archive the remaining legacy candidate-review code after the Mongo-backed lexical quiz path is stable.

## 2026-03-20 - Lexical quiz V2 contraction to knowledge-first + system-generated questions
- Current status:
  - Official Markdown/TXT/CSV lexical templates now only demonstrate knowledge assets; hand-written quiz blocks were removed from the operator-facing templates.
  - `Exercise Review` now treats `translation_choice` as the formal word-meaning exercise type and uses explicit buttons: `锟斤拷锟缴凤拷锟斤拷选锟斤拷锟斤拷 / 锟斤拷锟斤拷锟叫讹拷锟斤拷`.
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
  - `Import & Review` now explicitly tells operators whether `锟斤拷锟斤拷锟绞诧拷锟诫保锟斤拷锟斤拷` wrote to backend Mongo or fell back to local storage.
  - `Exercise Review` now reports whether quiz versions were loaded from backend Mongo or local fallback.
  - Review filter labels, status labels, quiz type labels, and generation reasons are now driven by UTF-8-safe copy config.
- Blocked / not yet done:
  - If old records were imported from corrupted source text, item content itself can still look bad until re-imported.
- Next concrete work item:
  - Re-run `锟斤拷锟斤拷锟绞诧拷锟诫保锟斤拷锟斤拷` after restarting backend, confirm status says backend Mongo, then verify `lexicalAssets` and `seedQuizzes` collections receive documents.

## 2026-03-20 - Lexical quiz API path fix + import session persistence
- Current status:
  - Lexical quiz review/import API calls now consistently target `/api/pipeline/...` and `/api/learning/...`, fixing the earlier 404 path mismatch that forced silent local fallback.
  - `Import & Review` now persists its local session across tab switches and shows whether seed save hit backend Mongo or local fallback.
  - `Exercise Review` also shows whether the current quiz list came from backend Mongo or local fallback.
- Blocked / not yet done:
  - Need a live operator smoke test after backend restart to confirm Mongo receives `lexicalAssets` and `seedQuizzes`.
- Next concrete work item:
  - Re-open `/admin/pipeline`, import a lexical asset file, click `锟斤拷锟斤拷锟绞诧拷锟诫保锟斤拷锟斤拷`, confirm the status says backend Mongo, then verify the two Mongo collections contain documents.

## 2026-03-20 - Import & Review left list compactness
- Current status:
  - The left lexical entry list in `LexicalAssetImportPanel.tsx` now shows `璇嶆€ | 渚嬪彞x` on the same line as the title and uses smaller vertical padding/margins.
  - This change is presentation-only; parsing, save behavior, and API paths remain unchanged.
- Blocked / not yet done:
  - No business-logic changes were made by request.
- Next concrete work item:
  - If needed, further tighten left-rail typography and badge sizing after a browser smoke test.
## 2026-03-20 - Import review list compaction
- Current status:
  - Import review left-side word rows now show `锟斤拷锟斤拷 x | 锟斤拷锟斤拷 x` inline beside the headword instead of taking a second summary line.
  - Entry row vertical spacing has been tightened to reduce wasted height in the review list.
- Blocked / not yet done:
  - A live browser check is still needed to confirm the compact row density feels right with real long words and issue badges.
- Next concrete work item:
  - Verify the compact list with a real imported markdown asset and adjust widths only if count text wraps too aggressively.
## 2026-03-20 - Exercise Review compactness + version-copy cleanup
- Current status:
  - The Exercise Review panel now groups quiz items by sense and uses a denser left list with shorter row height.
  - Display copy avoids version-like labels in the main UI, and the active-state wording is simplified to `褰撳墠棰榒 / `宸叉浛鎹.
- Blocked / not yet done:
  - Need a browser smoke test on real imported assets to confirm the tighter list still reads well.
- Next concrete work item:
  - Run the admin page with real quiz data, check the compressed grouped list, and trim widths only if labels wrap awkwardly.

## 2026-03-20 - Lexical practice answer-validation investigation and option normalization
- Current status:
  - Browser-level verification on `/lesson-exercise/vocab-course-...` confirmed the learner does not actually mark every option correct; wrong selections still produce `锟斤拷锟斤拷一锟斤拷`.
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
  - Home tab non-parent mode now renders as three sections: `锟斤拷学习路锟斤拷` / `锟斤拷锟斤拷敫聪癭 / `学习锟斤拷源`.
  - Repeated `学习锟斤拷锟斤拷` entry in resource cards was removed; diagnostic actions are now锟斤拷锟斤拷锟斤拷 `锟斤拷锟斤拷敫聪癭 锟斤拷锟斤拷.
  - Old `学习统锟斤拷` block was removed from first screen to reduce visual load.
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
## 2026-03-26 - 锟斤拷锟斤拷锟斤拷页锟斤拷学锟斤拷/锟斤拷习/锟斤拷锟洁）
- Current status:
  - 锟角家筹拷锟斤拷页锟斤拷锟斤拷锟斤拷为 3 锟斤拷锟斤拷锟介：`学习锟斤拷知识锟斤拷AI锟狡硷拷锟斤拷`锟斤拷`锟斤拷习锟斤拷知识`锟斤拷`展锟斤拷锟斤拷锟斤拷`锟斤拷
  - 锟斤拷锟斤拷锟斤拷锟侥拷锟斤拷锟斤拷穑锟斤拷锟斤拷展示锟斤拷锟斤拷锟斤拷锟杰匡拷片锟斤拷锟斤拷锟斤拷锟揭伙拷锟斤拷锟斤拷锟斤拷芎锟斤拷远锟斤拷锟斤拷锟?- Hidden entries kept (do not drop):
  - `锟斤拷锟斤拷锟斤拷锟斤拷拇锟斤拷锟絗 -> `/prescriptions`
  - `锟斤拷锟斤拷锟睫革拷` -> `/weakness-workbench`
  - `锟斤拷锟斤拷训锟斤拷` -> `/task-training`
  - `学习锟斤拷锟斤拷` -> `/progress-dashboard`
  - `锟斤拷锟皆伙拷` -> `/personalization`
  - `锟绞伙拷锟斤拷锟斤拷锟斤拷` -> `/vocab-assessment`
  - `锟斤拷锟斤拷驶锟斤拷锟斤拷` -> `/imported-word-course`
  - `锟缴就伙拷锟斤拷` -> `/achievements`
  - `锟斤拷锟斤拷学习模锟斤拷` -> `/learning-modules`
- Blocked / not yet done:
  - 锟斤拷未锟斤拷锟斤拷锟斤拷锟酵硷拷锟街わ拷锟絠OS/Android窄锟斤拷锟斤拷确锟斤拷锟侥帮拷锟截讹拷锟斤拷锟介。
- Next concrete work item:
  - 锟斤拷锟斤拷 360/375 锟斤拷锟斤拷泳锟斤拷毓椋伙拷锟接碉拷锟斤拷锟斤拷锟斤拷鹊锟斤拷锟斤拷锟斤拷锟斤拷斜锟斤拷锟斤拷锟斤拷锟斤拷示锟斤拷锟皆ｏ拷锟斤拷模锟斤拷眉锟斤拷锟斤拷

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
## 2026-04-02 - Sentence Insight Pack V1钀藉湴锛堢绾垮寘娑堣垂 + 鍙ュ瓙涓诲崱锛?- Current status:
  - 宸插畬鎴?V1 鏁版嵁濂戠害涓庡彂甯冮棬绂侊細鏍稿績 4 妯″潡缂哄け浼氳鏍￠獙鎷︽埅銆?  - 宸插畬鎴愮煡璇嗗惛鏀跺紩鎿庡彞瀛愭槧灏勶細渚嬪彞鍙€氳繃 `sentenceId/exampleKey` 绮剧‘鍛戒腑 insight 鍖呫€?  - 宸插畬鎴愮煡璇嗗惛鏀堕〉浜や簰锛氭湁鍖呮墠鏄剧ず鈥滆瑙ｂ€濓紝鐐瑰嚮鍚庡垏鍙ュ瓙涓诲崱骞舵敮鎸佲€滆繑鍥炲師璇嶁€濄€?  - 宸插畬鎴愭ā鍧楀寲鎶藉眽娓叉煋锛氬彞瀛愭ā寮忔寜妯″潡娉ㄥ唽琛ㄦ覆鏌擄紝涓嶄緷璧栧啓姝诲垎鏀€?- Blocked / not yet done:
  - 浠嶇己绂荤嚎鎵瑰鐞嗗鍏ヤ换鍔＄殑绔埌绔覆鑱旈獙璇侊紙澶ф壒閲忕湡瀹炲寘锛夈€?  - 浠嶇己椤甸潰绾ц嚜鍔ㄥ寲浜や簰娴嬭瘯锛堜緥濡傚垏璇嶆€у悗鍐嶆杩涘叆璇﹁В锛夈€?- Next concrete work item:
  - 鎺ュ叆骞惰窇閫氬閮ㄦ壒澶勭悊 insight 鍖呭鍏?smoke锛堝惈 schema+瀹屾暣鎬?鍥炴函涓€鑷存€э級锛屽啀琛ヤ竴鏉?UI 浜や簰鑷姩鍖栫敤渚嬭鐩栧彞瀛愪富鍗″線杩斻€?

## 2026-04-02 - Lexicon graph auto-first pipeline (strict gate + minimal manual)
- Current status:
  - Backend lexicon graph contract and routes are in place for import/review/publish and learning consumption.
  - Admin `LexicalAssetImportPanel` now supports:
    - batch creation from parsed lexical review
    - quality report and pending-candidate retrieval
    - tri-action candidate decisions (`閫氳繃 / 鎷掔粷 / 鍚堝苟`)
    - auto-publish when pending candidates are zero
  - Learner `imported-word-course` now supports graph-style navigation:
    - expansion click promotes target to main node
    - grouped expansion browsing, back navigation, return-to-root
    - `鐔熸倝/鎺屾彙` marking and recommendation refresh
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
  - Step #2 staging business-chain瑙傛祴:
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





## 2026-04-03 - admin/pipeline 中文乱码修复完成（前后端）
- Current status:
  - 前端 LexicalAssetImportPanel 用户可见中文文案已修复（发布、批次、状态、搭配、审核操作等）。
  - 后端 pipeline/contentPipelineService 关键错误信息已修复为正常中文。
  - admin/pipeline 页面可访问，DOM 抽样未检出此前乱码特征串。
- Verification:
  - duoxx TypeScript 检查通过：npx tsc --noEmit --pretty false。
  - 后端接口实测返回中文正常（sourcePath 是必填项、patchedCourse 是必填项、不支持的文档类型）。
- Next concrete work item:
  - 用户本地做一次硬刷新并复测导入/发布路径；若仍异常，再抓具体接口响应体与页面节点文本做定点修复。


## 2026-04-03 - knowledge-absorb 底部按钮乱码已修复
- Current status:
  - `knowledge-absorb` 底部动作区文案已恢复为 `收藏` / `掌握`，并修复了 `详解` 按钮文案。
- Verification:
  - `duoxx`: `npx tsc --noEmit --pretty false` 通过。
- Next concrete work item:
  - 用户端硬刷新后复测该页面；若仍有乱码，再按具体节点做定点清理。

## 2026-04-03 - knowledge-absorb 单词卡片内容区乱码已修复
- Current status:
  - `knowledge-absorb` 单词卡片中的 `释义/例句/暂无例句` 已恢复正常中文。
- Verification:
  - `duoxx` 类型检查通过：`npx tsc --noEmit --pretty false`。
  - 页面文本抽样未命中残留乱码特征。
- Next concrete work item:
  - 用户端硬刷新后复测；若仍有具体位置乱码，按截图节点继续定点修复。

## 2026-04-03 - 乱码问题已上升为宪法级门禁
- Current status:
  - 已把“UTF-8强制、乱码模式阻断、运行时中文可见性验证”写入两份宪法文档：`AGENTS.md` 与 `DATA_QUALITY_CONSTITUTION.md`。
- Verification:
  - 宪法条款存在性已检查（Encoding/Text Constitution、Text Encoding Gate）。
- Next concrete work item:
  - 后续中文文案改动统一执行：源码扫描 + 页面/API抽样验证，再允许合入。

## 2026-04-03 - 资产自动关联系统 V1 已执行（鲁棒导入 + 自动关联 + unresolved）
- Current status:
  - 后端 `/api/pipeline/lexicon/import-batches` 已兼容单文件与多文件 bundle（`review` / `bundleReviews` 双协议）。
  - 图谱节点与关系已扩展：`sentence_pattern/spoken/slang/idiom` 与 `HAS_SENTENCE_PATTERN/HAS_SPOKEN/HAS_SLANG/HAS_IDIOM`。
  - 自动链接已落地“可匹配尽量匹配、不可匹配标 unresolved 并持久化”，不阻塞整批导入。
  - 批次报告已支持文件级指标：`parsedBlocks/skippedBlocks/unresolvedRefs`，并在前端导入面板展示。
  - 学习端 expand group 已支持：`sentencePatterns/spoken/slang/idioms`。
  - 知识吸收页已移除 sentence insight 的前端 fallback 重建逻辑，改为只消费后端/源数据中的 `sentenceInsightPackV1`。
- Verification:
  - Frontend: `npx tsc --noEmit --pretty false` -> pass。
  - Frontend tests:
    - `npm test -- src/services/__tests__/lexicalSingleFileImport.test.ts --runInBand` -> pass。
    - `npm test -- src/modules/knowledge-absorb/knowledgeAbsorbEngine.test.ts --runInBand` -> pass。
  - Backend syntax check:
    - `node --check src/services/lexiconGraphService.js` -> pass。
    - `node --check src/routes/pipeline.js` -> pass。
    - `node --check src/models/LexiconNode.js` -> pass。
    - `node --check src/models/LexiconEdge.js` -> pass。
    - `node --check src/models/LexiconImportBatch.js` -> pass。
- Blocked / not yet done:
  - 后端 Jest 当前环境不可运行：缺少 `cross-env` 与 `jest` 命令（本机依赖未装全）。
- Next concrete work item:
  - 在 `duoxx_server_link` 安装/恢复测试依赖后补跑：`pipeline.test.js`、`lexiconGraphService.integration.test.js`、`lexiconGraph.e2e.test.js`。
  - 使用 `asserts/` 全量样本跑一次端到端导入演练，确认 unresolved 覆盖率与前端多跳扩展表现。

## 2026-04-03 - asserts 全量导入演练完成（V1 基线）
- Current status:
  - 已新增并执行全量演练测试：`duoxx/src/services/__tests__/lexiconAssetsBundleRehearsal.test.ts`。
  - 演练输入：`asserts/` 下 7 个资产文件（word/collocations/phrases/sentencePatterns/slang/idioms/spokenExpressions）。
  - 演练结果（本地 fallback 图谱导入）：
    - totalFiles: 7
    - totalEntries: 64
    - nodesTotal: 130
    - edgesTotal: 488
    - unresolvedRefs: 329
    - pendingReview: 51
  - 文件级（parsed/skipped/unresolved）摘要：
    - collocations.md: 6 / 0 / 3
    - idioms.md: 3 / 0 / 2
    - phrases.md: 6 / 0 / 4
    - sentencePatterns.md: 3 / 22 / 2
    - slang.md: 3 / 0 / 2
    - spokenExpressions.md: 21 / 0 / 21
    - word.md: 26 / 26 / 358
- Verification:
  - Frontend:
    - `npm test -- src/services/__tests__/lexiconAssetsBundleRehearsal.test.ts --runInBand` -> pass。
    - `npx tsc --noEmit --pretty false` -> pass。
  - Backend:
    - `$env:NODE_ENV='test'; .\\node_modules\\.bin\\jest.cmd src/routes/pipeline.test.js src/services/__tests__/lexiconGraphService.integration.test.js src/routes/lexiconGraph.e2e.test.js --runInBand` -> pass (3 suites / 10 tests)。
- Blocked / not yet done:
  - `sentencePatterns.md` 与 `word.md` 存在较多 skipped blocks，需回源资产修正格式。
  - unresolved 总量高，需针对高频未命中模式（别名、词形、标点规范）优化源数据。
- Next concrete work item:
  - 先修 `word.md` 与 `sentencePatterns.md` 的结构格式（减少 skipped）。
  - 再补充 `spokenExpressions.md` 和 `word.md` 的 alias/lemma 对齐，降低 unresolved。

## 2026-04-03 - 新增可复用 Skill：asset-link-enricher
- Current status:
  - 已在项目内新增技能目录：
    - `.agents/skills/asset-link-enricher/`
    - `.codex/skills/asset-link-enricher/`
  - 技能包含：
    - `SKILL.md`（触发条件、流程、决策规则）
    - `scripts/run-asset-link-enricher.ps1`（一键执行全量资产演练并输出风险排序）
- Verification:
  - 已执行：
    - `powershell -ExecutionPolicy Bypass -File .\\.agents\\skills\\asset-link-enricher\\scripts\\run-asset-link-enricher.ps1`
  - 输出正常，包含 `unresolvedRefs/pendingReview/fileSummaries` 与按风险排序列表。
- Next concrete work item:
  - 后续可基于该脚本增加 `--write-report-to-progress` 开关，将基线自动附加到项目进度文档。

## 2026-04-03 - asset-link-enricher 升级（输出 unresolved 明细）
- Current status:
  - 演练测试新增 `unresolvedTopByFile` 聚合（按文件统计未匹配引用 Top 标签）。
  - 技能脚本升级：执行后除文件级汇总外，还会直接打印各文件 Top unresolved 标签。
  - 已生成基线报告：`reports/asset-link-baseline.json`。
- Verification:
  - `npm test -- src/services/__tests__/lexiconAssetsBundleRehearsal.test.ts --runInBand` -> pass。
  - `powershell -ExecutionPolicy Bypass -File .\\.agents\\skills\\asset-link-enricher\\scripts\\run-asset-link-enricher.ps1 -OutFile .\\reports\\asset-link-baseline.json` -> pass。
- Next concrete work item:
  - 基于 `reports/asset-link-baseline.json` 先出“源资产修订建议清单 v1”（不直接改源文件），按 `word.md` 和 `spokenExpressions.md` 优先。

## 2026-04-03 - 资产演练/诊断文件范围修复（allowlist）
- Current status:
  - 已修复诊断测试误把非资产文档计入导入样本的问题（例如 `asserts/ASSET_REPAIR_RECOMMENDATIONS_V1.md`）。
  - 两个测试现在都只读取 7 个目标资产：`word/collocations/phrases/sentencePatterns/slang/idioms/spokenExpressions`。
- Files changed:
  - `duoxx/src/services/__tests__/assetParseDiagnostics.test.ts`
  - `duoxx/src/services/__tests__/lexiconAssetsBundleRehearsal.test.ts`（此前已完成 allowlist，本轮确认）
- Verification:
  - `npm test -- src/services/__tests__/assetParseDiagnostics.test.ts --runInBand` -> pass。
  - `npm test -- src/services/__tests__/lexiconAssetsBundleRehearsal.test.ts --runInBand` -> pass。
  - `powershell -ExecutionPolicy Bypass -File .\.agents\skills\asset-link-enricher\scripts\run-asset-link-enricher.ps1 -OutFile .\reports\asset-link-baseline.json` -> pass。
  - 基线报告已回归为 `files: 7`（不再误计第 8 个文档）。
- Next concrete work item:
  - 进入资产质量治理：优先降低 `word.md` unresolved 与 `sentencePatterns.md` skippedBlocks。

## 2026-04-03 - modules/vocab-recognition/exercise 乱码已修复
- Current status:
  - 该页面核心用户可见文案已恢复正常中文（暂无可用词汇/返回/智能学习/复习巩固/挑战模式/熟悉，先跳过/继续）。
- Verification:
  - duoxx 类型检查通过：npx tsc --noEmit --pretty false。
- Next concrete work item:
  - 用户端硬刷新后复测；若仍有具体文案异常，按截图继续逐点修复。

## 2026-04-03 - 资产治理工具链 V1 落地（contract + registry + patch suggestions）
- Current status:
  - 已新增治理核心模块：`duoxx/src/services/assetLinkGovernance.ts`，提供：
    - 契约报告：`buildGovernanceContractReport`（文件级 contract passed/failed）
    - 词条主索引：`buildGovernanceRegistry`（canonical key、source files、POS、重复提示）
    - unresolved 聚合：`collectUnresolvedItems`
    - 补全建议：`buildPatchSuggestions`（`add_alias/add_ref/create_node`）
  - 新增测试：
    - 单元：`duoxx/src/services/__tests__/assetLinkGovernance.test.ts`
    - 集成演练：`duoxx/src/services/__tests__/assetLinkGovernanceRehearsal.test.ts`（输出 `[asset-link-governance]`）
  - 升级 skill 脚本：
    - `.agents/skills/asset-link-enricher/scripts/run-asset-link-enricher.ps1`
    - `.codex/skills/asset-link-enricher/scripts/run-asset-link-enricher.ps1`
    - 现在会额外执行 governance 测试并把治理结果写入报告 JSON（`governance` 字段）。
  - 升级 skill 文档：
    - `.agents/skills/asset-link-enricher/SKILL.md`
    - `.codex/skills/asset-link-enricher/SKILL.md`
- Verification:
  - `npm test -- src/services/__tests__/assetLinkGovernance.test.ts --runInBand` -> pass。
  - `npm test -- src/services/__tests__/assetLinkGovernanceRehearsal.test.ts --runInBand` -> pass。
  - `powershell -ExecutionPolicy Bypass -File .\.agents\skills\asset-link-enricher\scripts\run-asset-link-enricher.ps1 -OutFile .\reports\asset-link-baseline.json` -> pass。
  - `npx tsc --noEmit --pretty false` -> pass。
  - 报告校验：`reports/asset-link-baseline.json` 已包含 `governance`；当前 failed files=`word.md,sentencePatterns.md`，patch suggestions=`206`。
- Next concrete work item:
  - 进入“资产修复批次 #1”：优先处理 `word.md`（高 unresolved）与 `sentencePatterns.md`（高 skipped）。

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
## 2026-04-03 - 资产修复批次 #1（源文件治理）完成
- Current status:
  - 已修复 `sentencePatterns.md` 结构问题：重写为规范 key-value 块，清除导致解析器跳过的编号说明噪音。
  - 已修复 `word.md` 结构问题：
    - 移除 `<!-- Level ... -->` 注释行（避免被计入 skipped）。
    - 规范化“同一行粘连多个字段”的历史脏格式（如 `### sense ... - translationZh ...` 拆分为多行字段）。
    - 新增一批高频缺失基础词条（如 sorrowful/abundant/dismayed/eternity/hour/instant/moment/overjoyed/slight/thrilled）。
  - 已修复 `spokenExpressions.md` 格式问题：统一为行式 `anchor (Lx): expression || zh`，避免 mixed-format 导致 skipped。
  - 已补充高频未命中节点到资产文件：
    - `phrases.md`、`collocations.md`、`slang.md`、`idioms.md`、`spokenExpressions.md`。
- Verification:
  - `npm test -- src/services/__tests__/assetParseDiagnostics.test.ts --runInBand` -> pass。
  - `npm test -- src/services/__tests__/lexiconAssetsBundleRehearsal.test.ts --runInBand` -> pass。
  - `npm test -- src/services/__tests__/assetLinkGovernanceRehearsal.test.ts --runInBand` -> pass。
  - `powershell -ExecutionPolicy Bypass -File .\.agents\skills\asset-link-enricher\scripts\run-asset-link-enricher.ps1 -OutFile .\reports\asset-link-baseline.json` -> pass。
- Baseline delta (vs old 7-file baseline):
  - totalEntries: `64 -> 96`
  - unresolvedRefs: `329 -> 228`
  - contract failed files: `2 -> 0`
  - skippedBlocks: `word.md 26 -> 0`, `sentencePatterns.md 22 -> 0`, `spokenExpressions.md 0 -> 0`
- Next concrete work item:
  - 资产修复批次 #2：继续按 `word.md` Top unresolved 清单处理（优先 sentencePatterns/spokenExpressions 类标签文本规范化与 refs 对齐）。

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
  - Profile tab (non-parent) now includes vocab test entry in "学习入口".
- Verification:
  - `npx eslint "app/(tabs)/index.tsx" "app/(tabs)/profile.tsx"` -> pass.
  - `npx tsc --noEmit --pretty false` -> pass.
- Next concrete work item:
  - Run one user-flow smoke in app: Home->More and Profile->学习入口.## 2026-04-03 - 资产乱码防护加固（UTF-8 + 门禁）
- Current status:
  - 新增资产乱码检测器：`duoxx/src/services/assetEncodingGuard.ts`，命中乱码特征直接返回 `ASSET_TEXT_MOJIBAKE_DETECTED` 错误。
  - 在 `parseSingleFileLexicalAsset` 入口加入编码门禁，检测到乱码即阻断解析，避免脏数据继续入库。
  - 资产诊断测试新增编码断言：`assetParseDiagnostics.test.ts` 要求 allowlist 文件 `encodingIssueCount=0`。
  - 新增单元测试：`assetEncodingGuard.test.ts`。
  - `run-asset-link-enricher.ps1`（agents/codex 两份）统一设置 UTF-8 输入输出与默认编码参数。
  - allowlist 兼容 `phrase.md/idiom.md` 单数命名，避免资产静默漏导。
  - 修复残留乱码键：`asserts/sentencePatterns.md`、`asserts/slang.md`。
- Verification:
  - `npm test -- src/services/__tests__/assetEncodingGuard.test.ts src/services/__tests__/assetParseDiagnostics.test.ts src/services/__tests__/lexiconAssetsBundleRehearsal.test.ts src/services/__tests__/assetLinkGovernanceRehearsal.test.ts --runInBand` -> pass。
- Next concrete work item:
  - 对 `spokenExpressions.md` 当前格式做结构化升级（减少 `ORPHAN_FIELD` 警告）。

## 2026-04-03 - Prescriptions page route removed
- Current status:
  - Standalone route page `/prescriptions` has been removed.
  - Home no longer has learning-plan entry; user cannot enter that page from navigation.
- Verification:
  - No `/prescriptions` route reference found by grep.
  - `npx eslint "app/(tabs)/index.tsx" "app/(tabs)/profile.tsx" "app/weakness-workbench.tsx" "app/task-training.tsx"` -> pass.
  - `npx tsc --noEmit --pretty false` -> pass.
- Next concrete work item:
  - If needed, align weak-point pages wording to avoid "处方" terminology.## 2026-04-03 - 资产关联治理继续推进（批次 2）
- Current status:
  - 解析器支持 structured markdown 的 `- examples:` 编号例句格式，消除 `phrase/collocations/idiom/spokenExpressions` 的 `UNPARSED_LINE` 噪音。
  - 解析入口扩展识别 `## spokenExpression:` markdown 头，避免误走 txt-line parser。
  - `parseMarkdownOrTxt` 忽略 HTML 注释行（如 `<!-- Level -->`），`word.md` 不再产生 `skippedBlocks`。
  - 增补高频缺失节点到资产源文件（source-first）：
    - `phrase.md`: a little bit / in a minute / little by little / small fortune / small talk / the minute (that)
    - `collocations.md`: little chance / little effort / minute details / minute hand / small business / small detail
    - `idiom.md`: not for a minute
    - `spokenExpressions.md`: Give me a minute! / Little did I know!
    - `slang.md`: old fogey / pommy
- Verification:
  - `npm test -- src/services/__tests__/lexicalSingleFileImport.test.ts --runInBand` -> pass。
  - `npm test -- src/services/__tests__/assetParseDiagnostics.test.ts src/services/__tests__/lexiconAssetsBundleRehearsal.test.ts src/services/__tests__/assetLinkGovernanceRehearsal.test.ts --runInBand` -> pass。
  - 乱码扫描（7 文件）`badLines=0`。
- Delta:
  - `unresolvedRefs: 192 -> 145`（进一步下降）。
  - `contract.failedFiles: []` 保持全绿。
  - 所有 allowlist 资产 `skippedBlocks=0`。
- Next concrete work item:
  - 继续处理 `word.md` 未命中的词汇类节点（如 sorrowful/abundant/dismayed/instant/moment/overjoyed/thrilled 等）与句型模板节点标准化。

## 2026-04-03 - Terminology unified on weakness/task pages
- Current status:
  - Learner-facing copy on weakness and task pages no longer uses "处方".
  - Wording now uses "学习计划/修复方案" consistently.
- Verification:
  - No "处方" matches in `app/weakness-workbench.tsx` and `app/task-training.tsx`.
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
  - Decide whether to run phase-2 internal renaming for backend model/service symbols.## 2026-04-03 - 全局系统性思考 Skill 新增
- Current status:
  - 新增全局 skill：`C:\Users\Administrator\.codex\skills\systemic-problem-abstraction`。
  - 能力定位：先判断问题是否可规律化，再分类 `DATA_GAP / WORKFLOW_GAP / IMPLEMENTATION_DEFECT`，优先抽象为可复用治理能力。
  - 附带参考模板：
    - `references/decision-framework.md`
    - `references/data-request-template.md`
  - 生成并校验通过：`agents/openai.yaml`、`quick_validate.py`。
- Verification:
  - `python3 .../generate_openai_yaml.py ...` -> pass。
  - `python3 .../quick_validate.py ...` -> pass。
- Next concrete work item:
  - 在后续资产治理任务中强制使用该 skill 的输出契约（Type/Why/Reusable Change/Owner Needed）。
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
  - Duration display switched to Chinese units (`��/Сʱ`).
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
    - logged-in: `�˳���¼`
    - logged-out: `ȥ��¼`
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
  - Time metrics now use a shared stat-card style and appear in one row (`����ʱ��` + `�ۼ�ʱ��`).
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
  - Convert this audit into an IA refactor proposal with explicit ��keep / merge / hide / remove�� decisions.

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
  - Learner Home now keeps only two top-level entries: `练习模式（做题）` and `吸收模式`.
  - New `practice-mode` page aggregates exercise/review entrances and keeps `QuickStartButton` as primary action.
  - Existing capabilities are preserved in practice hub: `复习旧知识` / `任务训练` / `弱点修复` / `词汇评估`.
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
    - active type summary (`��������`)
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
  - Removed "�鿴��������" control in knowledge absorb card.
  - Card now directly shows 2 examples (or fewer if unavailable).
- Verification:
  - `npm.cmd --prefix d:\06-project\expo_duo\duoxx run lint -- "app/knowledge-absorb.tsx"` -> pass.
  - `npx.cmd tsc --noEmit -p tsconfig.json` (cwd: `duoxx`) -> pass.
- Next concrete work item:
  - Visual check: ensure two-example spacing remains comfortable on smallest screen width.

## 2026-04-08 - Home card renamed to Practice Mode and now one-tap starts questions
- Current status:
  - Home primary learning entry is now 练习模式 with explicit 开始做题 copy.
  - Intermediate 更多练习选项 entry is removed from Home.
  - Practice-start failure fallback now routes directly to /modules/vocab-recognition/exercise.
- Verification:
  - cmd /c npx eslint "app/(tabs)/index.tsx" -> pass.
  - cmd /c npx tsc --noEmit --pretty false -> pass.
- Next concrete work item:
  - Device smoke: validate tap-to-start path under both recommendation-success and fallback conditions.

## 2026-04-08 - Learning tab redesigned to bold two-action layout
- Current status:
  - Learning Home now uses a dominant 练习模式 hero with explicit 开始做题 CTA.
  - 吸收模式 remains available as secondary supporting entry.
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
  - Synonym and antonym are merged into one selectable group (近义词/反义词).
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
  - Runtime sampling on multiple polysemous words to verify anchor filtering doesn’t over-prune expected expressions.

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
  - "�鿴��������" removed.
  - Word examples now render max 2 directly.
  - Non-sentence expansion drawer remains visible by default with active group selection.
  - Vertical swipe affordance remains in expansion content area when item count > 1.
- Verification:
  - npm run lint -- app/knowledge-absorb.tsx
  - node ./node_modules/typescript/bin/tsc --noEmit -p tsconfig.json
