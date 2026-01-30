# Implementation Plan

- [x] 1. Set up module structure and core types







  - [x] 1.1 Create survival-phrases module directory structure

    - Create `src/modules/survival-phrases/` with subdirectories: types, services, components, screens, data
    - Set up index.ts exports
    - _Requirements: 9.1_
  - [ ] 1.2 Define core type definitions
    - Create SurvivalScenario enum


    - Create PhraseErrorType enum





    - Define SurvivalPhrase, PhraseExample, DialogueLine interfaces

    - Define CommonMistake, PhrasePack, PhraseWeakness interfaces
    - _Requirements: 1.3, 3.2, 9.2_


  - [ ] 1.3 Write property test for type completeness
    - **Property 2: Phrase Display Completeness**


    - **Validates: Requirements 1.3**




- [ ] 2. Implement PhraseManager service
  - [x] 2.1 Create PhraseManager class


    - Implement IPhraseManager interface
    - Implement loadPhrasePacks() with mock data


    - Implement getPacksByScenario() grouping logic








    - Implement getPackById() lookup
    - _Requirements: 1.1, 1.2_
  - [x] 2.2 Write property test for pack grouping


    - **Property 1: Phrase Pack Grouping Consistency**


    - **Validates: Requirements 1.1**



  - [ ] 2.3 Implement search functionality


    - Implement search() across english, chinese, scenario fields
    - Implement relevance ranking (exact > partial)






    - Implement getSuggestions() for empty results
    - _Requirements: 8.1, 8.2, 8.3_


  - [x] 2.4 Write property tests for search


    - **Property 3: Search Coverage**


    - **Property 4: Search Relevance Ordering**
    - **Validates: Requirements 8.1, 8.2**


  - [x] 2.5 Implement pack configuration validation










    - Create JSON schema for phrase pack
    - Implement validatePackConfig() with specific error messages


    - _Requirements: 9.2, 9.3_


  - [x] 2.6 Write property test for validation








    - **Property 9: Pack Configuration Validation**
    - **Validates: Requirements 9.3**






- [ ] 3. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.






- [x] 4. Implement WeaknessTracker service










  - [ ] 4.1 Create WeaknessTracker class
    - Implement IWeaknessTracker interface
    - Implement recordWeakness() with error categorization


    - Implement getWeaknesses() and getWeaknessesByType()
    - Implement getWeaknessStats() for aggregation

    - _Requirements: 3.1, 3.2, 3.3_

  - [x] 4.2 Write property test for weakness recording






    - **Property 5: Weakness Recording Completeness**
    - **Validates: Requirements 3.1, 3.2**

  - [ ] 4.3 Implement error book integration
    - Implement getErrorBookCompatibleRecords() format conversion
    - Implement syncToErrorBook() using errorCollectionService
    - _Requirements: 3.4_

  - [ ] 4.4 Write property test for error book integration
    - **Property 6: Error Book Integration Format**
    - **Validates: Requirements 3.4**






  - [ ] 4.5 Implement markImproved() for weakness updates
    - Update weakness record when user corrects mistake


    - _Requirements: 4.4_





- [ ] 5. Implement PracticeEngine service

  - [ ] 5.1 Create PracticeEngine class
    - Implement IPracticeEngine interface
    - Implement startPractice() and completePractice()
    - _Requirements: 6.1_
  - [ ] 5.2 Implement common mistake detection
    - Implement detectCommonMistake() pattern matching
    - _Requirements: 4.1, 4.2_
  - [ ] 5.3 Write property test for mistake detection
    - **Property 7: Common Mistake Detection Accuracy**
    - **Validates: Requirements 4.2**
  - [ ] 5.4 Implement pronunciation practice integration
    - Integrate with pronunciationScorer from listening-speaking module
    - Implement getPronunciationFeedback() with word-level highlighting
    - _Requirements: 6.2, 6.3_
  - [ ] 5.5 Write property test for pronunciation feedback
    - **Property 12: Pronunciation Feedback Word Coverage**
    - **Validates: Requirements 6.3**


- [ ] 6. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.


- [ ] 7. Create mock data and phrase packs

  - [ ] 7.1 Create airport scenario phrase pack
    - Define 10+ phrases for airport scenarios
    - Include examples and common mistakes for each phrase
    - _Requirements: 1.2, 5.1_
  - [ ] 7.2 Write property test for example dialogue
    - **Property 8: Example Dialogue Highlighting**
    - **Validates: Requirements 5.2**
  - [ ] 7.3 Create hospital/emergency scenario phrase pack
    - Define 10+ phrases for medical emergencies
    - _Requirements: 1.2_
  - [ ] 7.4 Create hotel/restaurant scenario phrase pack
    - Define 10+ phrases for hospitality scenarios
    - _Requirements: 1.2_

- [ ] 8. Implement cache service for offline support

  - [ ] 8.1 Create CacheService for phrase packs
    - Implement cachePhrasePack() for favorites
    - Implement getCachedPacks() for offline access
    - Implement cache eviction for storage limits
    - _Requirements: 7.1, 7.2, 7.4_
  - [ ] 8.2 Write property test for cache consistency
    - **Property 11: Offline Cache Consistency**
    - **Validates: Requirements 7.1**
  - [ ] 8.3 Implement dynamic scenario support
    - Implement loadDynamicScenario() with API placeholder
    - Implement cacheDynamicScenario() for offline access
    - Implement fallback to mock data when backend unavailable
    - _Requirements: 10.1, 10.2, 10.4_
  - [ ] 8.4 Write property test for scenario source
    - **Property 10: Scenario Source Identification**
    - **Validates: Requirements 10.3**

- [ ] 9. Checkpoint - Ensure all tests pass

  - Ensure all tests pass, ask the user if questions arise.

- [ ] 10. Implement UI components

  - [ ] 10.1 Create PackListView component
    - Display phrase packs grouped by scenario
    - Support scenario filtering
    - _Requirements: 1.1_
  - [ ] 10.2 Create PhraseCard component
    - Display phrase with english, chinese, phonetic, context
    - Integrate Speaking Avatar for demonstration
    - Highlight common mistakes
    - _Requirements: 1.3, 2.1, 4.1_
  - [ ] 10.3 Create ExampleDialogue component
    - Display dialogue with target phrase highlighted
    - Support Speaking Avatar dialogue playback
    - _Requirements: 5.1, 5.2, 5.3_
  - [ ] 10.4 Create SearchBar component
    - Implement search input with debounce
    - Display search results with context
    - Show suggestions for empty results
    - _Requirements: 8.1, 8.2, 8.3, 8.4_

- [ ] 11. Implement screens

  - [ ] 11.1 Create SurvivalPhrasesScreen
    - Main screen with pack list and search
    - Navigation to phrase details
    - _Requirements: 1.1, 8.1_
  - [ ] 11.2 Create PhraseDetailScreen
    - Display phrase with Speaking Avatar
    - Show examples and common mistakes
    - Entry point to practice mode
    - _Requirements: 1.3, 2.1, 5.1_
  - [ ] 11.3 Create PracticeScreen
    - Speaking practice with recording
    - Pronunciation feedback display
    - Mistake detection and correction
    - _Requirements: 6.1, 6.2, 6.3, 4.2, 4.3_

- [ ] 12. Register module and integrate

  - [ ] 12.1 Update module registry
    - Ensure survival-phrases module is properly registered
    - Verify route configuration
    - _Requirements: 1.1_
  - [ ] 12.2 Integrate with error book
    - Connect WeaknessTracker to global errorCollectionService
    - Verify weakness records appear in error book
    - _Requirements: 3.4_

- [ ] 13. Final Checkpoint - Ensure all tests pass

  - Ensure all tests pass, ask the user if questions arise.
