# Implementation Plan

- [x] 1. Set up module structure and core types






  - [x] 1.1 Create speaking-avatar module directory structure

    - Create `src/modules/speaking-avatar/` with subdirectories: types, services, components, data, registries
    - Set up index.ts exports
    - _Requirements: 3.1, 7.1_

  - [ ] 1.2 Define core type definitions
    - Create Viseme enum with 16 viseme types
    - Define CharacterConfig, CharacterAssets, ExpressionConfig interfaces
    - Define LipSyncData, VisemeFrame interfaces
    - Define LanguageMapping interface
    - Define SpeakingAvatarError types








    - _Requirements: 1.4, 2.2, 5.4, 7.1_
  - [ ] 1.3 Write property test for Viseme enum completeness
    - **Property 7: Phoneme to Viseme Mapping Completeness**
    - **Validates: Requirements 5.4**



- [ ] 2. Implement registries for extensibility

  - [x] 2.1 Implement CharacterRegistry


    - Create ICharacterRegistry interface
    - Implement character registration and lookup
    - Implement age group filtering


    - Implement configuration validation with specific error messages

    - _Requirements: 2.1, 2.2, 2.3, 9.1, 9.2, 9.3_











  - [ ] 2.2 Write property test for character validation
    - **Property 3: Character Viseme Completeness**


    - **Property 10: Character Validation Error Specificity**


    - **Validates: Requirements 2.2, 9.3**
  - [ ] 2.3 Implement ExpressionRegistry
    - Create IExpressionRegistry interface


    - Implement expression registration and lookup
    - Support transition configuration per expression



    - _Requirements: 8.1, 8.2, 8.4_



  - [ ] 2.4 Implement LanguageRegistry
    - Create ILanguageRegistry interface


    - Implement language mapping registration and lookup
    - Implement fallback to English for unsupported languages
    - _Requirements: 10.1, 10.2, 10.3, 10.4_









  - [-] 2.5 Write property test for language fallback

    - **Property 12: Language Fallback to English**


    - **Validates: Requirements 10.3**



- [ ] 3. Checkpoint - Ensure all tests pass

  - Ensure all tests pass, ask the user if questions arise.







- [ ] 4. Implement phoneme and lip sync services



  - [ ] 4.1 Implement PhonemeService
    - Create text-to-phoneme conversion using rule-based approach
    - Implement phoneme-to-viseme mapping using language registry


    - Implement timing estimation based on text length
    - _Requirements: 5.3, 5.4_
  - [x] 4.2 Write property test for phoneme mapping









    - **Property 7: Phoneme to Viseme Mapping Completeness**



    - **Validates: Requirements 5.4**
  - [ ] 4.3 Implement LipSyncEngine
    - Create LipSyncData generation from text


    - Implement viseme timing calculation
    - Implement fallback timing when TTS unavailable
    - _Requirements: 1.1, 1.4, 5.2, 5.3_


  - [x] 4.4 Write property tests for lip sync engine


    - **Property 2: Viseme Timing Bounds**






    - **Property 5: Text Input Produces Valid LipSync**
    - **Property 6: TTS Fallback Produces Valid LipSync**
    - **Validates: Requirements 1.4, 3.1, 3.2, 5.2**



- [x] 5. Implement audio and TTS services






  - [x] 5.1 Implement AudioService



    - Create audio playback using expo-av


    - Implement duration detection
    - Implement playback control (play, pause, stop)




    - _Requirements: 1.1, 3.3, 3.4_
  - [ ] 5.2 Implement TTSService
    - Create TTS using expo-speech
    - Implement availability detection
    - Implement fallback mechanism when TTS unavailable
    - _Requirements: 5.1, 5.2_


- [ ] 6. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 7. Implement expression and animation engines

  - [ ] 7.1 Implement ExpressionEngine
    - Create expression state management
    - Implement expression blending with lip sync
    - Implement smooth transitions between expressions
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 8.3_
  - [ ] 7.2 Write property tests for expression engine
    - **Property 8: Expression Feedback Correctness**
    - **Property 9: Expression Blending Preserves LipSync**
    - **Validates: Requirements 4.2, 4.3, 8.3**
  - [ ] 7.3 Implement AnimationEngine
    - Create idle animation loop (breathing, blinking)
    - Implement animation state management
    - Implement native driver animations for performance
    - _Requirements: 4.1, 6.3_


- [ ] 8. Implement SpeakingAvatarController
  - [ ] 8.1 Create SpeakingAvatarController class
    - Implement ISpeakingAvatarController interface
    - Integrate LipSyncEngine, ExpressionEngine, AnimationEngine
    - Implement speak() and speakWithAudio() methods
    - Implement playback control (stop, pause, resume)
    - _Requirements: 3.1, 3.2, 3.3_
  - [ ] 8.2 Write property tests for controller
    - **Property 1: Lip Sync State Consistency**
    - **Property 4: Animation Timing Consistency**
    - **Property 11: Character Switch State Preservation**
    - **Validates: Requirements 1.2, 1.3, 2.4, 9.4**
  - [ ] 8.3 Implement resource cleanup
    - Clear all timers on dispose
    - Stop audio playback on unmount
    - Release animation resources
    - _Requirements: 6.4_
  - [ ] 8.4 Write property test for resource cleanup
    - **Property 14: Resource Cleanup on Unmount**
    - **Validates: Requirements 6.4**

- [ ] 9. Checkpoint - Ensure all tests pass

  - Ensure all tests pass, ask the user if questions arise.

- [ ] 10. Implement SpeakingAvatarView component

  - [ ] 10.1 Create SpeakingAvatarView component
    - Implement component with CharacterLayer, VisemeLayer, ExpressionLayer
    - Support text and audioUrl input props
    - Implement size variants (small, medium, large)
    - Implement autoPlay functionality
    - _Requirements: 1.1, 3.1, 7.3_
  - [ ] 10.2 Implement callback props
    - Add onPlaybackStart, onPlaybackEnd callbacks
    - Add onVisemeChange callback
    - Add onError callback with graceful fallback UI
    - _Requirements: 7.2, 7.4_
  - [ ] 10.3 Write property test for callbacks
    - **Property 13: Playback Callbacks Invocation**
    - **Validates: Requirements 7.2**
  - [ ] 10.4 Implement fallback UI
    - Display static avatar on error
    - Show loading state during asset loading
    - _Requirements: 7.4_

- [ ] 11. Create default character and expression data

  - [ ] 11.1 Create default character configurations
    - Create at least 3 character configs (bunny, fox, professor)
    - Define viseme asset paths for each character
    - Define expression overlays for each character
    - _Requirements: 2.1, 2.2_
  - [ ] 11.2 Create default expression configurations
    - Define neutral, happy, thinking, encouraging expressions
    - Configure transition durations and easing functions
    - _Requirements: 8.1, 8.2, 8.4_
  - [ ] 11.3 Create English phoneme mapping
    - Define complete ARPAbet phoneme to viseme mapping
    - Set as default language mapping
    - _Requirements: 5.4, 10.2_

- [ ] 12. Register module and integrate with existing system

  - [ ] 12.1 Register speaking-avatar module
    - Add module to src/modules/registry.ts
    - Export public API from module index
    - _Requirements: 3.1_
  - [ ] 12.2 Create integration example
    - Create example usage in a test screen
    - Demonstrate text input and audio URL input
    - Demonstrate expression changes and callbacks
    - _Requirements: 3.1, 7.1_

- [ ] 13. Final Checkpoint - Ensure all tests pass

  - Ensure all tests pass, ask the user if questions arise.
