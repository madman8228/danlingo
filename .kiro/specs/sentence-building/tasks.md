# Implementation Plan

- [x] 1. Set up module structure and register in registry
  - [x] 1.1 Create module directory structure under `src/modules/sentence-building/`
    - Create folders: screens/, components/, services/, data/
    - Create index.ts for module exports
    - _Requirements: 8.1_
  - [x] 1.2 Register module in `src/modules/registry.ts`
    - Add module definition with id, name, description, icon, color, route, status
    - Add to USER_GROUPS for all target groups (child, student, adult)
    - _Requirements: 8.1_
  - [x] 1.3 Create route files in `app/modules/sentence-building/`
    - Create index.tsx (main screen)
    - Create exercise.tsx (exercise screen)
    - Create complete.tsx (completion screen)
    - _Requirements: 8.1_

- [x] 2. Define data models and types
  - [x] 2.1 Create `src/modules/sentence-building/types.ts`
    - Define SentenceExerciseType enum
    - Define FillBlankExercise, WordOrderExercise interfaces
    - Define BlankSlot, GrammarPattern, GrammarExample interfaces
    - Define UserSentenceState, UserGrammarState interfaces
    - Define ExerciseResult interface
    - _Requirements: 1.1, 2.1, 3.1_
  - [x] 2.2 Write property test for data model validation
    - **Property 6: Grammar pattern data completeness**
    - **Validates: Requirements 3.2**

- [x] 3. Create sentence template data
  - [x] 3.1 Create `src/modules/sentence-building/data/sentenceTemplates.ts`
    - Define SentenceTemplate interface
    - Create initial set of sentence templates (20-30 sentences)
    - Include A1-B1 level content
    - Categorize by topic (daily, travel, business)
    - _Requirements: 4.1_
  - [x] 3.2 Create `src/modules/sentence-building/data/grammarPatterns.ts`
    - Define basic grammar patterns (SVO, questions, negatives, tenses)
    - Include examples and translations for each pattern
    - _Requirements: 3.2_

- [x] 4. Implement exercise generation service
  - [x] 4.1 Create `src/modules/sentence-building/services/exerciseGenerator.ts`
    - Implement generateFillBlankExercise function
    - Implement generateWordOrderExercise function
    - Implement distractor generation logic
    - _Requirements: 1.1, 2.1, 1.5_
  - [x] 4.2 Implement CEFR level filtering
    - Filter templates by user level
    - Support challenge mode (above level)
    - _Requirements: 4.1_
  - [x] 4.3 Write property test for CEFR filtering
    - **Property 8: CEFR level filtering**
    - **Validates: Requirements 4.1**
  - [x] 4.4 Write property test for challenge mode
    - **Property 13: Challenge mode difficulty increase**
    - **Validates: Requirements 6.4**

- [x] 5. Implement exercise validation service
  - [x] 5.1 Create `src/modules/sentence-building/services/exerciseValidator.ts`
    - Implement validateFillBlank function
    - Implement validateWordOrder function
    - Return detailed feedback with correct answers
    - _Requirements: 2.4, 1.4_
  - [x] 5.2 Write property test for word order validation
    - **Property 4: Word ordering validation correctness**
    - **Validates: Requirements 2.4**
  - [x] 5.3 Write property test for incorrect position identification
    - **Property 5: Incorrect word order identifies wrong positions**
    - **Validates: Requirements 2.6**

- [x] 6. Checkpoint - Ensure all tests pass




  - Ensure all tests pass, ask the user if questions arise.

- [x] 7. Implement progress service
  - [x] 7.1 Create `src/modules/sentence-building/services/sentenceProgressService.ts`
    - Implement recordAnswer function
    - Implement getReviewStats function
    - Implement getDueSentences function
    - Use existing spacedRepetitionService
    - _Requirements: 5.4, 8.2_
  - [x] 7.2 Implement session summary calculation




    - Calculate total XP earned
    - Calculate accuracy rate
    - _Requirements: 5.1_
  - [x] 7.3 Write property test for progress persistence




    - **Property 10: Progress persistence round-trip**
    - **Validates: Requirements 5.4**
  - [x] 7.4 Write property test for session summary
    - **Property 9: Session summary calculation**
    - **Validates: Requirements 5.1**


- [x] 8. Implement learning mode recommendation









  - [x] 8.1 Create `src/modules/sentence-building/data/recommendations.ts`






























    - Implement getRecommendedExercises function
    - Support smart-learn, review, challenge modes
    - _Requirements: 6.2, 6.3, 6.4_
  - [x] 8.2 Write property test for smart learn mode


    - **Property 11: Smart learn mode level matching**
    - **Validates: Requirements 6.2**








  - [x] 8.3 Write property test for review mode
    - **Property 12: Review mode prioritization**


    - **Validates: Requirements 6.3**














- [x] 9. Checkpoint - Ensure all tests pass
  - All 163 tests pass

- [x] 10. Implement FillBlankExercise component
  - [x] 10.1 Create `src/modules/sentence-building/components/FillBlankExercise.tsx`
    - Render sentence with blank slots
    - Display option buttons for each blank
    - Handle option selection
    - Show correct/incorrect feedback
    - _Requirements: 1.1, 1.2_
  - [x] 10.2 Write property test for blank rendering
    - **Property 2: Fill-blank exercise displays blanks and options**
    - **Validates: Requirements 1.1**

- [x] 11. Implement WordOrderingExercise component
  - [x] 11.1 Create `src/modules/sentence-building/components/WordOrderingExercise.tsx`
    - Render draggable word cards
    - Implement drag-and-drop with react-native-gesture-handler
    - Show drop zones and visual feedback
    - Handle reordering state
    - _Requirements: 2.1, 2.2, 2.3_

- [x] 12. Implement GrammarPatternCard component
  - [x] 12.1 Create `src/modules/sentence-building/components/GrammarPatternCard.tsx`
    - Display pattern name and structure
    - Show examples with translations
    - Visual breakdown of sentence parts
    - _Requirements: 3.1, 3.2_

- [x] 13. Implement module main screen
  - [x] 13.1 Update `src/modules/sentence-building/screens/SentenceBuildingScreen.tsx`
    - Display progress stats (learned, mastered, to review)
    - Show learning mode cards (smart learn, review, challenge)
    - Handle navigation to exercise screen
    - _Requirements: 5.2, 6.1_

- [x] 14. Implement exercise screen
  - [x] 14.1 Update `src/modules/sentence-building/screens/SentenceExerciseScreen.tsx`
    - Load exercises based on mode
    - Render appropriate exercise component by type
    - Handle answer submission and validation
    - Show feedback (animated for child, sound for adult)
    - Track progress and XP
    - _Requirements: 1.2, 1.3, 2.5, 7.1, 7.2_
  - [x] 14.2 Write property test for XP awarding
    - **Property 1: Correct answer awards XP**
    - **Validates: Requirements 1.3, 2.5**
  - [x] 14.3 Write property test for incorrect feedback
    - **Property 3: Incorrect answer shows correct answer**
    - **Validates: Requirements 1.4**

- [x] 15. Implement completion screen
  - [x] 15.1 Update `src/modules/sentence-building/screens/SentenceCompleteScreen.tsx`
    - Display session summary (XP, accuracy)
    - Show completion feedback based on performance
    - Provide continue learning and home buttons
    - _Requirements: 5.1_

- [x] 16. Implement grammar progress tracking
  - [x] 16.1 Add grammar pattern tracking to progress service
    - Record practiced patterns
    - Calculate pattern mastery
    - _Requirements: 3.4_
  - [x] 16.2 Write property test for grammar recording
    - **Property 7: Grammar practice recording**
    - **Validates: Requirements 3.4**

- [x] 17. Final Checkpoint - Ensure all tests pass
  - All 163 tests pass (12 test suites)
