# Requirements Document

## Introduction

说话助教模块（Speaking Avatar）是一个可复用的动画角色组件，能够根据给定的单词或句子进行口型同步动画。该模块支持多种卡通形象，可以集成到词汇认知、听说训练等多个学习模块中，为用户提供更生动的视觉反馈和学习体验。

## Glossary

- **Speaking Avatar**: 说话助教，一个能够根据音频或文本进行口型动画的卡通角色组件
- **Viseme**: 视位，与特定语音对应的嘴型形状
- **Lip Sync**: 口型同步，将音频或文本与嘴型动画进行时间对齐
- **Phoneme**: 音素，语言中最小的语音单位
- **TTS**: Text-to-Speech，文本转语音服务
- **Avatar Character**: 助教角色，不同风格的卡通形象

## Requirements

### Requirement 1

**User Story:** As a learner, I want to see a cartoon character speaking words or sentences, so that I can better understand pronunciation through visual lip movements.

#### Acceptance Criteria

1. WHEN the system plays audio for a word or sentence THEN the Speaking Avatar SHALL display synchronized lip animations matching the audio
2. WHEN the Speaking Avatar is idle THEN the system SHALL display a neutral mouth position with subtle idle animations
3. WHEN audio playback completes THEN the Speaking Avatar SHALL smoothly transition back to the idle state
4. WHEN the Speaking Avatar is speaking THEN the system SHALL display viseme transitions at appropriate timing intervals

### Requirement 2

**User Story:** As a product designer, I want to support multiple cartoon character styles, so that we can offer variety and appeal to different user groups.

#### Acceptance Criteria

1. WHEN configuring the Speaking Avatar THEN the system SHALL allow selection from at least 3 different character styles
2. WHEN a character style is selected THEN the system SHALL load the corresponding viseme asset set for that character
3. WHEN adding a new character style THEN the system SHALL require only new viseme assets without code changes
4. WHEN displaying a character THEN the system SHALL maintain consistent animation timing across all character styles

### Requirement 3

**User Story:** As a developer, I want a simple API to integrate the Speaking Avatar into different modules, so that I can easily add speaking functionality to vocab-recognition and listening-speaking modules.

#### Acceptance Criteria

1. WHEN integrating the Speaking Avatar THEN the developer SHALL provide only text or audio URL as input
2. WHEN the component receives text input THEN the system SHALL automatically generate audio using TTS and perform lip sync
3. WHEN the component receives audio URL input THEN the system SHALL perform lip sync based on the audio
4. WHEN the component is mounted THEN the system SHALL handle all audio loading and playback internally

### Requirement 4

**User Story:** As a learner, I want the avatar to have expressive animations beyond just lip sync, so that the learning experience feels more engaging and alive.

#### Acceptance Criteria

1. WHEN the Speaking Avatar is idle THEN the system SHALL display subtle breathing or blinking animations
2. WHEN the learner answers correctly THEN the Speaking Avatar SHALL display a happy or celebratory expression
3. WHEN the learner answers incorrectly THEN the Speaking Avatar SHALL display an encouraging expression
4. WHEN transitioning between expressions THEN the system SHALL animate smoothly without jarring changes

### Requirement 5

**User Story:** As a developer, I want the lip sync to work with both pre-recorded audio and TTS-generated audio, so that the module can be used flexibly across different scenarios.

#### Acceptance Criteria

1. WHEN using TTS for audio generation THEN the system SHALL use expo-speech or a similar cross-platform TTS service
2. WHEN TTS is unavailable THEN the system SHALL fall back to timing-based lip sync using text phoneme estimation
3. WHEN pre-recorded audio is provided THEN the system SHALL estimate lip sync timing based on audio duration and text length
4. WHEN generating lip sync data THEN the system SHALL map English phonemes to appropriate viseme indices

### Requirement 6

**User Story:** As a user on a low-end device, I want the avatar animations to perform smoothly, so that my learning experience is not degraded by lag or stuttering.

#### Acceptance Criteria

1. WHEN rendering the Speaking Avatar THEN the system SHALL maintain at least 30 FPS on target devices
2. WHEN loading character assets THEN the system SHALL use optimized image formats and appropriate resolutions
3. WHEN animating visemes THEN the system SHALL use native driver animations where possible
4. WHEN the component unmounts THEN the system SHALL properly clean up all animation resources and audio

### Requirement 7

**User Story:** As a developer, I want clear documentation and examples for the Speaking Avatar API, so that I can quickly integrate it into new features.

#### Acceptance Criteria

1. WHEN the module is published THEN the system SHALL include TypeScript type definitions for all public interfaces
2. WHEN using the component THEN the developer SHALL have access to callback props for playback events
3. WHEN configuring the component THEN the developer SHALL be able to customize size, position, and animation speed
4. WHEN errors occur THEN the component SHALL emit error events and display graceful fallback UI

### Requirement 8

**User Story:** As a developer, I want the expression system to be modular and extensible, so that I can easily add new expressions without modifying core animation logic.

#### Acceptance Criteria

1. WHEN defining a new expression THEN the developer SHALL only need to provide expression configuration data without code changes
2. WHEN the system loads expressions THEN the system SHALL read from a centralized expression registry
3. WHEN an expression is triggered THEN the system SHALL blend the expression with ongoing lip sync animations
4. WHEN configuring expression transitions THEN the developer SHALL be able to specify duration and easing functions per expression

### Requirement 9

**User Story:** As a designer, I want to add new cartoon characters without developer assistance, so that we can quickly expand the avatar library.

#### Acceptance Criteria

1. WHEN adding a new character THEN the designer SHALL provide a character configuration file and asset bundle
2. WHEN the system loads characters THEN the system SHALL discover available characters from a character registry
3. WHEN a character configuration is invalid THEN the system SHALL report specific validation errors
4. WHEN switching characters at runtime THEN the system SHALL preserve current animation state during the transition

### Requirement 10

**User Story:** As a developer, I want the viseme mapping to be configurable per language, so that the module can support multiple languages in the future.

#### Acceptance Criteria

1. WHEN configuring the Speaking Avatar THEN the developer SHALL be able to specify the target language
2. WHEN the system maps phonemes to visemes THEN the system SHALL use language-specific mapping tables
3. WHEN a language mapping is not available THEN the system SHALL fall back to a default English mapping
4. WHEN adding a new language THEN the developer SHALL only need to provide a phoneme-to-viseme mapping file

