# Implementation Plan

- [x] 1. Set up module structure and core types






  - [x] 1.1 Create imperfect-dialogue module directory structure

    - Create `src/modules/imperfect-dialogue/` with subdirectories: types, services, components, screens, data
    - Set up index.ts exports
    - _Requirements: 7.1_

  - [x] 1.2 Define core type definitions

    - Create ResponseLevel enum (acceptable, better, native)
    - Create DialogueCategory enum
    - Define DialoguePrompt, ExpectedResponse, HintLevel interfaces
    - Define DialogueScenario, EvaluationResult, DialogueProgress interfaces
    - _Requirements: 2.1, 5.4, 7.2_

  - [x] 1.3 Write property test for type completeness

    - **Property 1: Evaluation Level Validity**
    - **Validates: Requirements 2.1**


- [x] 2. Implement ResponseEvaluator service



  - [x] 2.1 Create ResponseEvaluator class


    - Implement IResponseEvaluator interface
    - Implement evaluate() with multi-level matching
    - Implement matchesLevel() for variation checking
    - _Requirements: 1.2, 2.1_
  - [x] 2.2 Write property test for multi-variation matching


    - **Property 5: Multi-Variation Matching**
    - **Validates: Requirements 1.2**
  - [x] 2.3 Implement alternative response logic


    - Return betterAlternative for acceptable matches
    - Return nativeAlternative for better matches
    - _Requirements: 2.2, 2.3_
  - [x] 2.4 Write property tests for alternatives


    - **Property 2: Better Alternative Presence**
    - **Property 3: Native Alternative Presence**
    - **Validates: Requirements 2.2, 2.3**

  - [x] 2.5 Implement encouraging feedback generation


    - Create getEncouragingFeedback() without negative words
    - Implement isGrammaticallyAcceptable() for lenient checking
    - _Requirements: 1.3, 1.4_
  - [x] 2.6 Write property test for encouraging feedback


    - **Property 4: Encouraging Feedback Language**
    - **Validates: Requirements 1.4**


- [x] 3. Checkpoint - Ensure all tests pass




  - Ensure all tests pass, ask the user if questions arise.


- [x] 4. Implement HintProvider service



  - [x] 4.1 Create HintProvider class

    - Implement IHintProvider interface
    - Implement getNextHint() with progressive disclosure
    - Implement getAllHints() for hint retrieval
    - _Requirements: 8.1, 8.2_

  - [x] 4.2 Write property test for progressive hints

    - **Property 7: Progressive Hint Disclosure**
    - **Validates: Requirements 8.2**

  - [x] 4.3 Implement hint usage tracking
    - Implement recordHintUsage() for analytics
    - Implement getHintStats() for statistics

    - _Requirements: 8.4_

  - [x] 4.4 Write property test for hint tracking
    - **Property 14: Hint Count Tracking**

    - **Validates: Requirements 8.4**
  - [x] 4.5 Verify hint independence from evaluation

    - Ensure hints don't affect evaluation results
    - _Requirements: 8.3_
  - [x] 4.6 Write property test for hint independence


    - **Property 8: Hint Usage Independence**
    - **Validates: Requirements 8.3**



- [x] 5. Implement ProgressTracker service




  - [x] 5.1 Create ProgressTracker class

    - Implement IProgressTracker interface
    - Implement recordCompletion() for progress storage
    - Implement getLevelDistribution() for statistics
    - _Requirements: 6.1, 6.2_

  - [x] 5.2 Write property test for level distribution

    - **Property 11: Progress Level Distribution**
    - **Validates: Requirements 6.2**

  - [x] 5.3 Implement improvement detection

    - Implement detectImprovement() for progress tracking
    - _Requirements: 6.3_

  - [x] 5.4 Implement error book integration

    - Implement syncToErrorBook() using errorCollectionService
    - Convert weakness records to ErrorRecord format
    - _Requirements: 6.4_

  - [x] 5.5 Write property test for error book integration

    - **Property 12: Error Book Integration Format**

    - **Validates: Requirements 6.4**


- [x] 6. Checkpoint - Ensure all tests pass




  - Ensure all tests pass, ask the user if questions arise.



- [x] 7. Create mock data and dialogue scenarios










  - [x] 7.1 Create daily conversation scenarios




    - Define 5+ scenarios for daily situations (coffee shop, grocery, etc.)
    - Include multi-level responses and hints for each prompt
    - _Requirements: 5.1, 5.4_

  - [x] 7.2 Write property test for scenario completeness



    - **Property 9: Scenario Context Completeness**
    - **Validates: Requirements 5.1**
  - [x] 7.3 Write property test for native key phrases


    - **Property 6: Native Response Key Phrases**
    - **Validates: Requirements 3.2**

  - [x] 7.4 Create social/business scenarios


    - Define 5+ scenarios for social and business contexts

    - _Requirements: 5.4_
  - [x] 7.5 Create multi-turn dialogue scenarios


    - Define scenarios with 3+ connected prompts
    - _Requirements: 5.2_
  - [x] 7.6 Write property test for multi-turn connectivity


    - **Property 10: Multi-Turn Connectivity**
    - **Validates: Requirements 5.2**




- [x] 8. Implement scenario configuration validation



  - [x] 8.1 Create JSON schema for dialogue scenarios

    - Define required fields and types
    - _Requirements: 7.2_

  - [x] 8.2 Implement validateScenarioConfig()
    - Return specific error messages for invalid fields

    - _Requirements: 7.3_
  - [x] 8.3 Write property test for validation

    - **Property 13: Scenario Configuration Validation**
    - **Validates: Requirements 7.3**

  - [x] 8.4 Implement dynamic scenario loading

    - Support loading from backend API (placeholder)
    - Implement fallback to mock data
    - _Requirements: 7.4_



- [x] 9. Checkpoint - Ensure all tests pass



  - Ensure all tests pass, ask the user if questions arise.



- [x] 10. Implement UI components



  - [x] 10.1 Create ScenarioView component


    - Display context and speaker line
    - Hide expected answers
    - _Requirements: 1.1_
  - [x] 10.2 Create ResponseInput component


    - Support text input and voice recording
    - Integrate with speech recognition service
    - _Requirements: 4.1, 4.2_
  - [x] 10.3 Create FeedbackPanel component


    - Display multi-level feedback with visual distinction
    - Show better/native alternatives with explanations
    - Highlight key phrases for native responses
    - _Requirements: 2.2, 2.3, 3.2, 3.4_
  - [x] 10.4 Create HintButton component


    - Progressive hint disclosure UI
    - Track hint usage
    - _Requirements: 8.1, 8.2_
  - [x] 10.5 Integrate Speaking Avatar


    - Demonstrate responses at each level
    - Celebration animation for native-level
    - _Requirements: 2.4, 3.1_


- [x] 11. Implement screens





  - [x] 11.1 Create ImperfectDialogueScreen

    - Main screen with scenario list by category
    - Navigation to dialogue practice
    - _Requirements: 5.4_

  - [ ] 11.2 Create DialoguePracticeScreen
    - Multi-turn dialogue flow
    - Response input and evaluation
    - Feedback display with Speaking Avatar

    - _Requirements: 1.1, 2.1, 3.1_
  - [ ] 11.3 Create DialogueSummaryScreen
    - Display completion summary with key expressions
    - Show level distribution and improvement
    - _Requirements: 5.3, 6.2, 6.3_

- [x] 12. Register module and integrate






  - [x] 12.1 Update module registry

    - Ensure imperfect-dialogue module is properly registered
    - Verify route configuration
    - _Requirements: 5.4_

  - [x] 12.2 Integrate with error book

    - Connect ProgressTracker to global errorCollectionService
    - Verify weakness records appear in error book

    - _Requirements: 6.4_



- [x] 13. Final Checkpoint - Ensure all tests pass



  - Ensure all tests pass, ask the user if questions arise.
