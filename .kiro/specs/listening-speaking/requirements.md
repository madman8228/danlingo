# Requirements Document

## Introduction

听说训练模块（Listening & Speaking Training）是 DuoXX 应用的核心功能模块之一，旨在通过 AI 跟读评分、听音辨句等练习方式，强化用户的语音感知能力和口语输出能力。该模块将整合语音识别技术，提供实时发音评估和反馈，帮助用户建立正确的语音习惯。

本模块将复用现有的 `shadow-practice` 模块 ID，并扩展其功能范围，涵盖听力理解和口语表达两大核心能力维度。

## Glossary

- **Listening_Speaking_Module**: 听说训练功能模块，提供听力和口语练习功能
- **Speech_Recognition_Service**: 语音识别服务，将用户语音转换为文本
- **Pronunciation_Scorer**: 发音评分器，评估用户发音的准确性、流利度和完整度
- **Audio_Player**: 音频播放器，播放标准发音和练习材料
- **Exercise_Engine**: 练习引擎，管理练习流程和状态
- **Progress_Tracker**: 进度追踪器，记录用户学习进度和能力变化
- **CEFR**: 欧洲语言共同参考框架，用于标定语言能力等级
- **IRT**: 项目反应理论，用于能力评估的统计模型
- **Shadowing**: 影子跟读，一种语言学习技术，用户跟随音频同步或延迟复述
- **Dictation**: 听写，听音频写出对应文本的练习方式

## Requirements

### Requirement 1

**User Story:** As a language learner, I want to practice pronunciation by repeating after audio samples, so that I can improve my speaking fluency and accuracy.

#### Acceptance Criteria

1. WHEN a user selects a shadowing exercise THEN the Listening_Speaking_Module SHALL play the target audio and display the corresponding text
2. WHEN the audio playback completes THEN the Listening_Speaking_Module SHALL enable the recording button and provide visual indication that recording is ready
3. WHEN a user presses the record button THEN the Speech_Recognition_Service SHALL capture audio input and convert it to text
4. WHEN recording completes THEN the Pronunciation_Scorer SHALL evaluate the user's pronunciation and return scores for accuracy, fluency, and completeness
5. WHEN scoring completes THEN the Listening_Speaking_Module SHALL display detailed feedback including overall score, word-level accuracy highlighting, and improvement suggestions

### Requirement 2

**User Story:** As a language learner, I want to identify sentences from audio clips, so that I can improve my listening comprehension skills.

#### Acceptance Criteria

1. WHEN a user starts a listen-and-select exercise THEN the Audio_Player SHALL play the target sentence audio
2. WHEN audio playback completes THEN the Listening_Speaking_Module SHALL display multiple choice options for the user to select
3. WHEN a user selects an option THEN the Exercise_Engine SHALL validate the answer and provide immediate feedback
4. WHEN the user answers incorrectly THEN the Listening_Speaking_Module SHALL replay the audio and highlight the correct answer
5. WHEN the user requests a replay THEN the Audio_Player SHALL replay the audio up to a configurable maximum number of times

### Requirement 3

**User Story:** As a language learner, I want to practice dictation exercises, so that I can strengthen the connection between listening and writing.

#### Acceptance Criteria

1. WHEN a user starts a dictation exercise THEN the Audio_Player SHALL play the target sentence audio
2. WHEN the user types their answer THEN the Listening_Speaking_Module SHALL accept text input without auto-correction interference
3. WHEN the user submits their answer THEN the Exercise_Engine SHALL compare the input against the target text using fuzzy matching
4. WHEN validation completes THEN the Listening_Speaking_Module SHALL highlight correct words, incorrect words, and missing words with distinct visual styles
5. WHEN the exercise completes THEN the Listening_Speaking_Module SHALL display the correct answer alongside the user's input for comparison

### Requirement 4

**User Story:** As a language learner, I want to receive adaptive exercises based on my current level, so that I can learn at an appropriate difficulty.

#### Acceptance Criteria

1. WHEN a user enters the module THEN the Exercise_Engine SHALL retrieve the user's current LISTENING and SPEAKING ability levels from the global profile
2. WHEN generating exercises THEN the Exercise_Engine SHALL select content with difficulty matching the user's ability level within a configurable range
3. WHEN a user completes an exercise THEN the Progress_Tracker SHALL update the user's ability estimate using IRT-based scoring
4. WHEN ability changes significantly THEN the Exercise_Engine SHALL adjust subsequent exercise difficulty accordingly
5. WHEN a user's performance indicates mastery THEN the Exercise_Engine SHALL introduce more challenging content progressively

### Requirement 5

**User Story:** As a language learner, I want to see my progress in listening and speaking skills, so that I can track my improvement over time.

#### Acceptance Criteria

1. WHEN a user views the module home screen THEN the Progress_Tracker SHALL display current LISTENING and SPEAKING scores with CEFR level indicators
2. WHEN a user completes a practice session THEN the Progress_Tracker SHALL show session statistics including accuracy rate, exercises completed, and XP earned
3. WHEN a user views detailed progress THEN the Progress_Tracker SHALL display historical score trends as a visual chart
4. WHEN progress data is updated THEN the Progress_Tracker SHALL persist the data to local storage immediately
5. WHEN the app restarts THEN the Progress_Tracker SHALL restore the user's progress from local storage

### Requirement 6

**User Story:** As a language learner, I want audio playback controls, so that I can adjust the learning experience to my needs.

#### Acceptance Criteria

1. WHEN audio is playing THEN the Audio_Player SHALL display a progress indicator showing current playback position
2. WHEN a user adjusts playback speed THEN the Audio_Player SHALL support speeds of 0.5x, 0.75x, 1.0x, and 1.25x
3. WHEN a user pauses playback THEN the Audio_Player SHALL maintain the current position and allow resumption
4. WHEN a user seeks to a position THEN the Audio_Player SHALL jump to the specified position within the audio
5. WHEN playback completes THEN the Audio_Player SHALL emit a completion event for the Exercise_Engine to handle

### Requirement 7

**User Story:** As a language learner, I want clear visual feedback during exercises, so that I can understand my performance immediately.

#### Acceptance Criteria

1. WHEN displaying pronunciation scores THEN the Listening_Speaking_Module SHALL use color-coded indicators (green for good, yellow for acceptable, red for needs improvement)
2. WHEN showing word-level feedback THEN the Listening_Speaking_Module SHALL highlight each word with its individual accuracy score
3. WHEN an exercise is answered correctly THEN the Listening_Speaking_Module SHALL play a success sound and show positive visual feedback
4. WHEN an exercise is answered incorrectly THEN the Listening_Speaking_Module SHALL play an error sound and show constructive feedback
5. WHEN transitioning between exercises THEN the Listening_Speaking_Module SHALL provide smooth animations consistent with the app's design language

### Requirement 8

**User Story:** As a developer, I want the pronunciation scoring to be serializable, so that I can persist and restore scoring results.

#### Acceptance Criteria

1. WHEN a pronunciation score is generated THEN the Pronunciation_Scorer SHALL produce a result object that can be serialized to JSON
2. WHEN a serialized score is loaded THEN the Pronunciation_Scorer SHALL deserialize it back to the original result object with all properties intact
3. WHEN serializing scores THEN the Pronunciation_Scorer SHALL include timestamp, audio reference, and all scoring dimensions
4. WHEN deserializing invalid JSON THEN the Pronunciation_Scorer SHALL return an error result without throwing exceptions
5. WHEN round-tripping a score through serialization THEN the deserialized result SHALL be equivalent to the original result

### Requirement 9

**User Story:** As a language learner, I want exercises organized into themed units, so that I can focus on specific topics or scenarios.

#### Acceptance Criteria

1. WHEN a user views the module THEN the Listening_Speaking_Module SHALL display available units organized by theme and difficulty
2. WHEN a user selects a unit THEN the Listening_Speaking_Module SHALL show the unit's exercises with progress indicators
3. WHEN a user completes all exercises in a unit THEN the Progress_Tracker SHALL mark the unit as completed and award bonus XP
4. WHEN displaying units THEN the Listening_Speaking_Module SHALL indicate locked units and their unlock conditions
5. WHEN a user meets unlock conditions THEN the Listening_Speaking_Module SHALL automatically unlock the corresponding unit

### Requirement 10

**User Story:** As a system administrator, I want error handling for audio and speech services, so that the app remains stable when services are unavailable.

#### Acceptance Criteria

1. WHEN audio loading fails THEN the Audio_Player SHALL display an error message and offer a retry option
2. WHEN speech recognition is unavailable THEN the Speech_Recognition_Service SHALL notify the user and suggest alternative exercises
3. WHEN network connectivity is lost during an exercise THEN the Exercise_Engine SHALL save progress locally and allow offline practice with cached content
4. WHEN an unexpected error occurs THEN the Listening_Speaking_Module SHALL log the error and display a user-friendly message without crashing
5. WHEN recovering from an error THEN the Listening_Speaking_Module SHALL restore the previous state where possible
