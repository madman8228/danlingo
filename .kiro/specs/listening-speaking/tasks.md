# Implementation Plan

- [x] 1. Set up module structure and core types







  - [x] 1.1 Create module directory structure at `src/modules/listening-speaking/`


    - Create directories: `components/`, `services/`, `screens/`, `data/`, `utils/`
    - Create `index.ts` for module exports
    - _Requirements: 7.5_
  - [x] 1.2 Define core type definitions in `types.ts`


    - Define `ListeningSpeakingExerciseType`, `LSExercise`, `ShadowingExercise`, `ListenSelectExercise`, `DictationExercise`
    - Define `PronunciationScore`, `WordScore`, `AudioPlaybackState`, `PlaybackSpeed`
    - Define `LSExerciseResult`, `ExerciseSessionState`, `ListeningSpeakingProgress`
    - _Requirements: 1.1, 2.1, 3.1, 8.1_
  - [ ]* 1.3 Write property test for types
    - **Property 13: Pronunciation score serialization round-trip**
    - **Validates: Requirements 8.1, 8.2, 8.3, 8.5**
  - [x] 1.4 Update module registry to include listening-speaking module


    - Update `src/modules/registry.ts` to register the module with proper metadata
    - _Requirements: 7.5_


- [x] 2. Implement Pronunciation Scorer service




  - [x] 2.1 Create `PronunciationScorer` class in `services/pronunciationScorer.ts`


    - Implement `evaluate()` method for text comparison and scoring
    - Implement word-level scoring with Levenshtein distance
    - Calculate accuracy, fluency, and completeness scores
    - _Requirements: 1.4, 1.5_
  - [ ]* 2.2 Write property test for pronunciation scoring
    - **Property 1: Pronunciation scoring produces valid scores**
    - **Validates: Requirements 1.4**

  - [x] 2.3 Implement serialization methods

    - Implement `serialize()` to convert PronunciationScore to JSON
    - Implement `deserialize()` to parse JSON back to PronunciationScore
    - Handle invalid JSON gracefully
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_
  - [ ]* 2.4 Write property test for serialization
    - **Property 14: Invalid JSON deserialization returns error**
    - **Validates: Requirements 8.4**

- [x] 3. Implement Audio Service





  - [x] 3.1 Create `AudioService` class in `services/audioService.ts`


    - Implement `load()`, `play()`, `pause()`, `stop()` methods using Expo AV
    - Implement `seek()` method with position clamping
    - Implement `setSpeed()` with valid speed validation
    - Implement playback state management
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_
  - [ ]* 3.2 Write property tests for audio service
    - **Property 9: Playback speed accepts valid values only**
    - **Property 11: Seek updates position correctly**
    - **Validates: Requirements 6.2, 6.4**
  - [x] 3.3 Implement error handling for audio operations


    - Define `AudioErrorType` enum and `AudioError` interface
    - Implement retry logic for transient failures
    - _Requirements: 10.1_



- [x] 4. Checkpoint - Ensure all tests pass

  - [x] Ensure all tests pass, ask the user if questions arise.
  - Fixed pre-existing failing test in `exerciseGenerator.test.ts` (sentence-building module)
    - The test incorrectly expected `correctOrder` to be `[0, 1, 2, ...]` but the implementation correctly returns indices for reconstructing the original sentence from shuffled words

- [x] 5. Implement Exercise Engine





  - [x] 5.1 Create `ExerciseEngine` class in `services/exerciseEngine.ts`


    - Implement `startSession()` to initialize exercise session
    - Implement `getCurrentExercise()` and `nextExercise()` for navigation
    - Implement `submitAnswer()` for answer validation
    - Implement `endSession()` to finalize and return summary
    - _Requirements: 2.3, 4.1_
  - [ ]* 5.2 Write property test for answer validation
    - **Property 2: Answer validation returns correct result**
    - **Validates: Requirements 2.3**
  - [x] 5.3 Implement replay limit tracking


    - Track replay count per exercise
    - Enforce maxReplays limit
    - _Requirements: 2.5_
  - [ ]* 5.4 Write property test for replay limit
    - **Property 3: Replay count respects maximum limit**
    - **Validates: Requirements 2.5**
  - [x] 5.5 Implement dictation text comparison


    - Implement fuzzy matching algorithm for dictation answers
    - Generate word-level comparison results (correct, missing, extra)
    - _Requirements: 3.3, 3.4_
  - [ ]* 5.6 Write property test for dictation comparison
    - **Property 4: Dictation comparison produces consistent word-level results**
    - **Validates: Requirements 3.3**

  - [x] 5.7 Implement adaptive exercise selection

    - Select exercises based on user ability level
    - Filter by difficulty range (θ ± δ)
    - _Requirements: 4.2_
  - [ ]* 5.8 Write property test for exercise selection
    - **Property 5: Exercise selection matches user ability range**
    - **Validates: Requirements 4.2**


- [x] 6. Implement Progress Service




  - [x] 6.1 Create `ProgressService` class in `services/progressService.ts`


    - Implement `getProgress()` to retrieve user progress
    - Implement `updateProgress()` to update ability after exercise
    - Implement IRT-based ability update formula
    - _Requirements: 4.3, 5.1, 5.2_
  - [ ]* 6.2 Write property test for IRT ability update
    - **Property 6: IRT-based ability update follows formula**
    - **Validates: Requirements 4.3**
  - [x] 6.3 Implement session statistics calculation

    - Calculate accuracy rate, exercises completed, XP earned
    - _Requirements: 5.2_
  - [ ]* 6.4 Write property test for session statistics
    - **Property 7: Session statistics are correctly calculated**
    - **Validates: Requirements 5.2**
  - [x] 6.5 Implement progress persistence

    - Implement `saveProgress()` to persist to AsyncStorage
    - Implement `loadProgress()` to restore from AsyncStorage
    - _Requirements: 5.4, 5.5_
  - [ ]* 6.6 Write property test for progress persistence
    - **Property 8: Progress round-trip through storage**
    - **Validates: Requirements 5.4, 5.5**
  - [x] 6.7 Implement unit completion tracking

    - Track completed exercises per unit
    - Mark unit complete when all exercises done
    - Award bonus XP on completion
    - _Requirements: 9.3_
  - [ ]* 6.8 Write property test for unit completion
    - **Property 15: Unit completion marks unit complete**
    - **Validates: Requirements 9.3**
  - [x] 6.9 Implement unlock condition checking

    - Check unlock conditions against user state
    - Unlock units when conditions are met
    - _Requirements: 9.5_
  - [ ]* 6.10 Write property test for unlock conditions
    - **Property 16: Unlock condition triggers unlock**
    - **Validates: Requirements 9.5**

- [x] 7. Checkpoint - Ensure all tests pass





  - Ensure all tests pass, ask the user if questions arise.

- [x] 8. Implement UI utility functions





  - [x] 8.1 Create score-to-color mapping utility in `utils/scoreUtils.ts`


    - Implement `getScoreColor()` function
    - Map scores to green/yellow/red based on thresholds
    - _Requirements: 7.1_
  - [ ]* 8.2 Write property test for score-to-color mapping
    - **Property 12: Score-to-color mapping is consistent**
    - **Validates: Requirements 7.1**
  - [x] 8.3 Create error handling utilities in `utils/errorHandler.ts`


    - Implement safe error wrapper that never throws
    - Return structured error results
    - _Requirements: 10.4_
  - [ ]* 8.4 Write property test for error handling
    - **Property 17: Error handling does not throw**
    - **Validates: Requirements 10.4**


- [x] 9. Create exercise data




  - [x] 9.1 Define exercise units in `data/units.ts`


    - Create sample units for different themes (daily-conversation, travel, etc.)
    - Include exercises of varying difficulty levels
    - _Requirements: 9.1, 9.2_

  - [-] 9.2 Create sample exercises for each type

    - Create shadowing exercises with audio URLs and text
    - Create listen-select exercises with options
    - Create dictation exercises with target text
    - _Requirements: 1.1, 2.1, 3.1_



- [x] 10. Implement Speech Recognition Service




  - [x] 10.1 Create `SpeechRecognitionService` in `services/speechRecognitionService.ts`

    - Implement `isAvailable()` to check platform support
    - Implement `requestPermission()` for microphone access
    - Implement `startRecording()` and `stopRecording()` methods
    - Handle partial results and errors
    - _Requirements: 1.3, 10.2_

  - [x] 10.2 Implement fallback for unsupported platforms

    - Detect when speech recognition is unavailable
    - Provide alternative exercise suggestions
    - _Requirements: 10.2_

- [x] 11. Checkpoint - Ensure all tests pass





  - Ensure all tests pass, ask the user if questions arise.

- [x] 12. Implement UI screens








  - [x] 12.1 Create `ListeningSpeakingScreen` in `screens/ListeningSpeakingScreen.tsx`

    - Display module home with progress summary
    - Show available units with progress indicators
    - Handle unit selection navigation
    - _Requirements: 5.1, 9.1, 9.2, 9.4_

  - [x] 12.2 Create `ShadowingExerciseScreen` in `screens/ShadowingExerciseScreen.tsx`

    - Display audio player with text
    - Implement recording button with state management
    - Show pronunciation feedback after recording
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

  - [x] 12.3 Create `ListenSelectExerciseScreen` in `screens/ListenSelectExerciseScreen.tsx`

    - Display audio player
    - Show multiple choice options after playback
    - Handle answer selection and feedback
    - Implement replay functionality
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

  - [x] 12.4 Create `DictationExerciseScreen` in `screens/DictationExerciseScreen.tsx`

    - Display audio player
    - Implement text input for user answer
    - Show word-level comparison feedback
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_
  - [x] 12.5 Create `SessionCompleteScreen` in `screens/SessionCompleteScreen.tsx`


    - Display session statistics
    - Show XP earned and accuracy
    - Provide navigation back to module home
    - _Requirements: 5.2_



- [ ] 13. Implement UI components (Optional - functionality already inline in screens)



  - [x] 13.1 Extract `AudioPlayer` component to `components/AudioPlayer.tsx`




    - Refactor from inline implementation in exercise screens
    - Display playback progress bar
    - Implement play/pause button
    - Add speed control selector
    - Show current position and duration
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_
  - [x] 13.2 Extract `RecordButton` component to `components/RecordButton.tsx`


    - Refactor from ShadowingExerciseScreen
    - Show recording state with visual indicator
    - Handle press to start/stop recording
    - Display recording duration
    - _Requirements: 1.2, 1.3_
  - [x] 13.3 Extract `PronunciationFeedback` component to `components/PronunciationFeedback.tsx`


    - Refactor from ShadowingExerciseScreen
    - Display overall score with color coding
    - Show word-level accuracy highlighting
    - Provide improvement suggestions
    - _Requirements: 1.5, 7.1, 7.2_
  - [x] 13.4 Extract `WordComparison` component to `components/WordComparison.tsx`


    - Refactor from DictationExerciseScreen
    - Highlight correct, incorrect, and missing words
    - Show user input alongside correct answer
    - _Requirements: 3.4, 3.5_
  - [ ] 13.5 Extract `UnitCard` component to `components/UnitCard.tsx`


    - Refactor from ListeningSpeakingScreen
    - Display unit info with icon and color
    - Show progress indicator
    - Handle locked state display
    - _Requirements: 9.1, 9.2, 9.4_


- [x] 14. Implement navigation and routing







  - [x] 14.1 Create module routes in `app/modules/listening-speaking/`


    - Create `index.tsx` for module home
    - Create `[unitId].tsx` for unit exercises
    - Create `exercise.tsx` for exercise screen
    - _Requirements: 9.2_
  - [x] 14.2 Implement exercise flow navigation


    - Handle transitions between exercises
    - Navigate to completion screen after session
    - _Requirements: 7.5_


- [x] 15. Implement feedback and animations


  - [x] 15.1 Add sound effects for correct/incorrect answers
    - Use existing soundService for feedback sounds
    - _Requirements: 7.3, 7.4_
  - [x] 15.2 Add visual feedback animations
    - Implement success/error animations
    - Add smooth transitions between exercises
    - _Requirements: 7.3, 7.4, 7.5_


- [x] 16. Final Checkpoint - Ensure all tests pass







  - Ensure all tests pass, ask the user if questions arise.
