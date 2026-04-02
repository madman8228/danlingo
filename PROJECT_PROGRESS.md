## 2026-03-26 - Imported-word browse course exposed in Courses tab
- Current status:
  - 导入词汇浏览�?is now visible in /(tabs)/courses under the default ll category and routes to /imported-word-course.
- Blocked / not yet done:
  - Entry is currently a fixed local card, not backend-configurable course metadata.
- Next concrete work item:
  - If needed, migrate this card to backend course registry so it can be managed with other course items.
## 2026-03-26 - Hotfix for home tab compile block
- Current status:
  - pp/(tabs)/index.tsx syntax around ocabSubtitle is now parse-safe; no unterminated-template compile block.
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
  - Exercise Review now uses a single primary action: ��׼����Ч.
  - Already-active questions no longer show a second activation button; they display ��ǰ�� instead.
- Blocked / not yet done:
  - The backend still keeps separate approve/activate endpoints internally; the simplification is currently a UI-level orchestration.
- Next concrete work item:
  - Decide whether the backend should gain a dedicated pprove-and-activate endpoint or whether the current UI composition is sufficient.
## 2026-03-20 - Exercise Review semantic simplification
- Current status:
  - Exercise Review no longer exposes ������ / ��̬�� / ��ǰ�汾 in the operator UI.
  - The panel now groups by ���� on the left and shows all exercises under the selected sense on the right.
  - The generic ���ɺ�ѡ action has been replaced with explicit ����ѡ���� and �����ж��� actions.
- Blocked / not yet done:
  - Backend data still keeps quiz versioning internally; the UI now hides that model instead of deleting it.
  - Learning-side quiz consumption still has not switched to the active lexical quiz endpoint.
- Next concrete work item:
  - Run a browser smoke test for /admin/pipeline -> Exercise Review, then decide whether ��Ϊ��Ч�� should be auto-triggered on approve.
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
- �ʻ����������տ�Ϊϵͳ���ɣ�`����ѡ���� / �ж���`��

## Done
- Single-file import and review page is live in `/admin/pipeline`.
- Word/phrase headwords, multiple senses, translated facets, and translated examples are supported.
- �ٷ����ļ�ģ������ֻ����֪ʶ�ʲ��ֶΣ�����ʾ����д quiz��
- Seed quizzes can now be persisted from lexical review into backend Mongo collections.
- Generated quiz versions, active quiz bindings, and stale marking are now implemented in backend Mongo collections, with local AsyncStorage fallback still kept as a dev safety net.
- `Exercise Review` now hosts the lexical quiz version review panel with `Seed / Generated / Active / Stale` filters and approve/reject/activate/generate actions.
- Vocab lesson routes now prefer `/api/learning/lexical-quizzes/active` for `multiple_choice` and `true_false` quiz playback, with automatic fallback to the existing lesson payload when no usable active lexical quiz exists.
- The main admin page no longer exposes the old V4 multi-file import flow by default.
- `lexical-quiz-lifecycle-v1.md` now defines where dynamic quiz updates should be stored and how admins should review them.
- Progress tracking is now mandatory in both `PROJECT_MEMORY.md` and `PROJECT_PROGRESS.md`.
- The unused V4 lexical import implementation and its test/config files have been removed from the Expo repo.
- Backend learning route now exposes `/api/learning/lexical-quizzes/active` for current active lexical quiz reads.
- `Exercise Review` �������� `���ɷ���ѡ���� / �����ж���`�����ٰ� `word_card` �������������͡�
- ѧϰ������ʽ֧�� `translation_choice`��legacy `word_card / multiple_choice` ���ڶ�ȡʱ����Ǩ�ơ�

## Not Done
- ѧϰ�˻�û�����������ʿ������`translation_choice` �Ը�������ѡ���������
- There is still legacy candidate-review code in the repo outside the current lexical quiz review path; it is bypassed but not fully deleted.
- The frontend still keeps local lexical quiz storage as fallback; once backend stability is confirmed, that fallback can be reduced or removed.

## Next Steps
- Decide whether the learner should keep reusing the current multiple-choice renderer for `translation_choice` or gain a dedicated lexical-card layout.
- Decide whether to keep or remove the frontend local lexical quiz fallback after backend smoke testing.
- Remove or archive the remaining legacy candidate-review code after the Mongo-backed lexical quiz path is stable.

## 2026-03-20 - Lexical quiz V2 contraction to knowledge-first + system-generated questions
- Current status:
  - Official Markdown/TXT/CSV lexical templates now only demonstrate knowledge assets; hand-written quiz blocks were removed from the operator-facing templates.
  - `Exercise Review` now treats `translation_choice` as the formal word-meaning exercise type and uses explicit buttons: `���ɷ���ѡ���� / �����ж���`.
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
  - `Import & Review` now explicitly tells operators whether `�����ʲ��뱣����` wrote to backend Mongo or fell back to local storage.
  - `Exercise Review` now reports whether quiz versions were loaded from backend Mongo or local fallback.
  - Review filter labels, status labels, quiz type labels, and generation reasons are now driven by UTF-8-safe copy config.
- Blocked / not yet done:
  - If old records were imported from corrupted source text, item content itself can still look bad until re-imported.
- Next concrete work item:
  - Re-run `�����ʲ��뱣����` after restarting backend, confirm status says backend Mongo, then verify `lexicalAssets` and `seedQuizzes` collections receive documents.

## 2026-03-20 - Lexical quiz API path fix + import session persistence
- Current status:
  - Lexical quiz review/import API calls now consistently target `/api/pipeline/...` and `/api/learning/...`, fixing the earlier 404 path mismatch that forced silent local fallback.
  - `Import & Review` now persists its local session across tab switches and shows whether seed save hit backend Mongo or local fallback.
  - `Exercise Review` also shows whether the current quiz list came from backend Mongo or local fallback.
- Blocked / not yet done:
  - Need a live operator smoke test after backend restart to confirm Mongo receives `lexicalAssets` and `seedQuizzes`.
- Next concrete work item:
  - Re-open `/admin/pipeline`, import a lexical asset file, click `�����ʲ��뱣����`, confirm the status says backend Mongo, then verify the two Mongo collections contain documents.

## 2026-03-20 - Import & Review left list compactness
- Current status:
  - The left lexical entry list in `LexicalAssetImportPanel.tsx` now shows `词性x | 例句x` on the same line as the title and uses smaller vertical padding/margins.
  - This change is presentation-only; parsing, save behavior, and API paths remain unchanged.
- Blocked / not yet done:
  - No business-logic changes were made by request.
- Next concrete work item:
  - If needed, further tighten left-rail typography and badge sizing after a browser smoke test.
## 2026-03-20 - Import review list compaction
- Current status:
  - Import review left-side word rows now show `���� x | ���� x` inline beside the headword instead of taking a second summary line.
  - Entry row vertical spacing has been tightened to reduce wasted height in the review list.
- Blocked / not yet done:
  - A live browser check is still needed to confirm the compact row density feels right with real long words and issue badges.
- Next concrete work item:
  - Verify the compact list with a real imported markdown asset and adjust widths only if count text wraps too aggressively.
## 2026-03-20 - Exercise Review compactness + version-copy cleanup
- Current status:
  - The Exercise Review panel now groups quiz items by sense and uses a denser left list with shorter row height.
  - Display copy avoids version-like labels in the main UI, and the active-state wording is simplified to `当前题` / `已替换`.
- Blocked / not yet done:
  - Need a browser smoke test on real imported assets to confirm the tighter list still reads well.
- Next concrete work item:
  - Run the admin page with real quiz data, check the compressed grouped list, and trim widths only if labels wrap awkwardly.

## 2026-03-20 - Lexical practice answer-validation investigation and option normalization
- Current status:
  - Browser-level verification on `/lesson-exercise/vocab-course-...` confirmed the learner does not actually mark every option correct; wrong selections still produce `����һ��`.
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
  - Home tab non-parent mode now renders as three sections: `��ѧϰ·��` / `����븴ϰ` / `ѧϰ��Դ`.
  - Repeated `ѧϰ����` entry in resource cards was removed; diagnostic actions are now������ `����븴ϰ` ����.
  - Old `ѧϰͳ��` block was removed from first screen to reduce visual load.
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
## 2026-03-26 - ������ҳ��ѧ��/��ϰ/���ࣩ
- Current status:
  - �Ǽҳ���ҳ������Ϊ 3 �����飺`ѧϰ��֪ʶ��AI�Ƽ���`��`��ϰ��֪ʶ`��`չ������`��
  - �������Ĭ�����𣬵����չʾ�������ܿ�Ƭ�������һ�������ܺ��Զ�����
- Hidden entries kept (do not drop):
  - `��������Ĵ���` -> `/prescriptions`
  - `�����޸�` -> `/weakness-workbench`
  - `����ѵ��` -> `/task-training`
  - `ѧϰ����` -> `/progress-dashboard`
  - `���Ի�` -> `/personalization`
  - `�ʻ�������` -> `/vocab-assessment`
  - `����ʻ����` -> `/imported-word-course`
  - `�ɾͻ���` -> `/achievements`
  - `����ѧϰģ��` -> `/learning-modules`
- Blocked / not yet done:
  - ��δ�������ͼ��֤��iOS/Androidխ����ȷ���İ��ض����顣
- Next concrete work item:
  - ���� 360/375 ����Ӿ��ع飻��ӵ�������ȵ��������б��������ʾ���ԣ���ģ��ü����

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
## 2026-04-02 - Sentence Insight Pack V1落地（离线包消费 + 句子主卡）
- Current status:
  - 已完成 V1 数据契约与发布门禁：核心 4 模块缺失会被校验拦截。
  - 已完成知识吸收引擎句子映射：例句可通过 `sentenceId/exampleKey` 精确命中 insight 包。
  - 已完成知识吸收页交互：有包才显示“详解”，点击后切句子主卡并支持“返回原词”。
  - 已完成模块化抽屉渲染：句子模式按模块注册表渲染，不依赖写死分支。
- Blocked / not yet done:
  - 仍缺离线批处理导入任务的端到端串联验证（大批量真实包）。
  - 仍缺页面级自动化交互测试（例如切词性后再次进入详解）。
- Next concrete work item:
  - 接入并跑通外部批处理 insight 包导入 smoke（含 schema+完整性+回溯一致性），再补一条 UI 交互自动化用例覆盖句子主卡往返。
