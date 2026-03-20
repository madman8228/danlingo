## 2026-03-20 - Exercise Review semantic simplification
- Current status:
  - Exercise Review no longer exposes 保底题 / 动态题 / 当前版本 in the operator UI.
  - The panel now groups by 义项 on the left and shows all exercises under the selected sense on the right.
  - The generic 生成候选 action has been replaced with explicit 生成选择题 and 生成判断题 actions.
- Blocked / not yet done:
  - Backend data still keeps quiz versioning internally; the UI now hides that model instead of deleting it.
  - Learning-side quiz consumption still has not switched to the active lexical quiz endpoint.
- Next concrete work item:
  - Run a browser smoke test for /admin/pipeline -> Exercise Review, then decide whether 设为生效题 should be auto-triggered on approve.
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
# Project Progress

Last updated: 2026-03-20

## Current Focus
- V5 single-file lexical asset import is the default operator flow.
- Markdown is the primary template; CSV/TXT are compatibility inputs.
- Attached quizzes now have a Mongo-backed review chain with frontend backend-first fallback: seed import, generated candidates, approve/reject, activate, and stale marking.

## Done
- Single-file import and review page is live in `/admin/pipeline`.
- Word/phrase headwords, multiple senses, translated facets, and translated examples are supported.
- Attached quiz protocol is parsed and rendered in the review UI.
- Seed quizzes can now be persisted from lexical review into backend Mongo collections.
- Generated quiz versions, active quiz bindings, and stale marking are now implemented in backend Mongo collections, with local AsyncStorage fallback still kept as a dev safety net.
- `Exercise Review` now hosts the lexical quiz version review panel with `Seed / Generated / Active / Stale` filters and approve/reject/activate/generate actions.
- The main admin page no longer exposes the old V4 multi-file import flow by default.
- `lexical-quiz-lifecycle-v1.md` now defines where dynamic quiz updates should be stored and how admins should review them.
- Progress tracking is now mandatory in both `PROJECT_MEMORY.md` and `PROJECT_PROGRESS.md`.
- The unused V4 lexical import implementation and its test/config files have been removed from the Expo repo.
- Backend learning route now exposes `/api/learning/lexical-quizzes/active` for current active lexical quiz reads.

## Not Done
- Learning-side quiz consumption still does not read `activeQuizBindings` from the new endpoint in the actual lesson UI.
- There is still legacy candidate-review code in the repo outside the current lexical quiz review path; it is bypassed but not fully deleted.
- The frontend still keeps local lexical quiz storage as fallback; once backend stability is confirmed, that fallback can be reduced or removed.

## Next Steps
- Connect learning-side exercise loading to `GET /api/learning/lexical-quizzes/active`, with seed fallback only if no active binding exists.
- Decide whether to keep or remove the frontend local lexical quiz fallback after backend smoke testing.
- Remove or archive the remaining legacy candidate-review code after the Mongo-backed lexical quiz path is stable.

## 2026-03-20 - Mongo persistence feedback + Exercise Review status copy
- Current status:
  - `Import & Review` now explicitly tells operators whether `保存资产与保底题` wrote to backend Mongo or fell back to local storage.
  - `Exercise Review` now reports whether quiz versions were loaded from backend Mongo or local fallback.
  - Review filter labels, status labels, quiz type labels, and generation reasons are now driven by UTF-8-safe copy config.
- Blocked / not yet done:
  - If old records were imported from corrupted source text, item content itself can still look bad until re-imported.
- Next concrete work item:
  - Re-run `保存资产与保底题` after restarting backend, confirm status says backend Mongo, then verify `lexicalAssets` and `seedQuizzes` collections receive documents.

## 2026-03-20 - Lexical quiz API path fix + import session persistence
- Current status:
  - Lexical quiz review/import API calls now consistently target `/api/pipeline/...` and `/api/learning/...`, fixing the earlier 404 path mismatch that forced silent local fallback.
  - `Import & Review` now persists its local session across tab switches and shows whether seed save hit backend Mongo or local fallback.
  - `Exercise Review` also shows whether the current quiz list came from backend Mongo or local fallback.
- Blocked / not yet done:
  - Need a live operator smoke test after backend restart to confirm Mongo receives `lexicalAssets` and `seedQuizzes`.
- Next concrete work item:
  - Re-open `/admin/pipeline`, import a lexical asset file, click `保存资产与保底题`, confirm the status says backend Mongo, then verify the two Mongo collections contain documents.

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
  - Import review left-side word rows now show `词性 x | 例句 x` inline beside the headword instead of taking a second summary line.
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
