# Requirements Document

## Introduction

救命锦囊（Survival Phrases）是一个面向成人英语学习者的实用表达模块，专注于紧急和关键场景下的必备表达。该模块强调"主动灌输"——向用户传授正确的表达方式，矫正常见错误，并发现用户的知识弱点。与词汇认知模块不同，救命锦囊以完整的实用短语为单位，结合场景卡片和 Speaking Avatar 口型示范，帮助用户建立"场景-表达"的快速关联。发现的弱点将保存到用户个人弱项中，与错题本系统融合，支持针对性强化。

## Glossary

- **Survival Phrase**: 救命锦囊短语，在特定紧急或关键场景下可立即使用的完整表达
- **Scenario Card**: 场景卡片，展示特定场景和对应表达的学习单元
- **Phrase Pack**: 锦囊包，按场景分类的短语集合
- **Speaking Avatar**: 说话助教，提供口型同步示范的卡通角色
- **Weakness Record**: 弱项记录，用户在学习过程中暴露的知识弱点，与错题本融合
- **Dynamic Scenario**: 动态场景，根据用户需求由后端生成并存储的个性化场景

## Requirements

### Requirement 1

**User Story:** As a traveler, I want to learn essential phrases for emergency situations, so that I can handle unexpected problems during my trip.

#### Acceptance Criteria

1. WHEN a user opens the Survival Phrases module THEN the system SHALL display categorized phrase packs organized by scenario type
2. WHEN a user selects a phrase pack THEN the system SHALL display all phrases in that pack with scenario context
3. WHEN displaying a phrase THEN the system SHALL show the English expression, Chinese translation, phonetic guide, and usage context
4. WHEN a phrase pack contains more than 10 phrases THEN the system SHALL support pagination or scrolling

### Requirement 2

**User Story:** As a learner, I want to hear native pronunciation with visual lip sync demonstration, so that I can learn correct pronunciation effectively.

#### Acceptance Criteria

1. WHEN a user taps a phrase card THEN the Speaking Avatar SHALL demonstrate the phrase with synchronized lip animations
2. WHEN the Speaking Avatar speaks THEN the system SHALL highlight the current word being spoken
3. WHEN audio playback completes THEN the system SHALL allow the user to replay or move to the next phrase
4. WHEN TTS is unavailable THEN the system SHALL display a fallback audio player without lip sync

### Requirement 3

**User Story:** As a learner, I want the system to identify my knowledge weaknesses during practice, so that I can focus on areas that need improvement.

#### Acceptance Criteria

1. WHEN a user makes an error during phrase practice THEN the system SHALL record the error to the weakness tracking system
2. WHEN recording a weakness THEN the system SHALL categorize it by error type (pronunciation, word choice, grammar pattern)
3. WHEN the user views their profile THEN the system SHALL display aggregated weakness statistics from survival phrases
4. WHEN weaknesses are identified THEN the system SHALL integrate them with the global error book for unified review

### Requirement 4

**User Story:** As a learner, I want to correct my common mistakes through targeted practice, so that I can avoid making the same errors in real situations.

#### Acceptance Criteria

1. WHEN displaying a phrase THEN the system SHALL highlight common mistakes learners make with this expression
2. WHEN the user practices a phrase THEN the system SHALL detect if they are making a known common mistake
3. WHEN a mistake is detected THEN the Speaking Avatar SHALL demonstrate the correct form with emphasis
4. WHEN the user corrects their mistake THEN the system SHALL update the weakness record to reflect improvement

### Requirement 5

**User Story:** As a learner, I want to see real-world usage examples for each phrase, so that I understand when and how to use them appropriately.

#### Acceptance Criteria

1. WHEN displaying a phrase THEN the system SHALL show at least one example dialogue demonstrating usage
2. WHEN the example dialogue is displayed THEN the system SHALL highlight the target phrase within the context
3. WHEN the user taps an example THEN the Speaking Avatar SHALL perform the dialogue with appropriate expressions
4. WHEN a phrase has multiple usage contexts THEN the system SHALL display all relevant examples

### Requirement 6

**User Story:** As a learner, I want to practice speaking the phrases myself, so that I can build muscle memory for pronunciation.

#### Acceptance Criteria

1. WHEN a user enters Speaking Practice mode THEN the system SHALL prompt the user to speak the phrase
2. WHEN the user records their speech THEN the system SHALL compare it with the target pronunciation
3. WHEN pronunciation feedback is generated THEN the system SHALL highlight words that need improvement
4. WHEN the user achieves acceptable pronunciation THEN the system SHALL mark the phrase as practiced

### Requirement 7

**User Story:** As a frequent traveler, I want to access my learned phrases offline, so that I can use them even without internet connection.

#### Acceptance Criteria

1. WHEN a user marks a phrase pack as favorite THEN the system SHALL cache the pack for offline access
2. WHEN the device is offline THEN the system SHALL display cached phrase packs with full functionality except TTS
3. WHEN the device reconnects THEN the system SHALL sync any offline progress to the server
4. WHEN storage is limited THEN the system SHALL prioritize recently accessed phrase packs

### Requirement 8

**User Story:** As a learner, I want to quickly search for phrases by keyword or scenario, so that I can find what I need in urgent situations.

#### Acceptance Criteria

1. WHEN a user enters a search query THEN the system SHALL search across phrase text, translations, and scenario descriptions
2. WHEN search results are displayed THEN the system SHALL rank results by relevance and show matching context
3. WHEN no results are found THEN the system SHALL suggest related phrase packs
4. WHEN the user selects a search result THEN the system SHALL navigate directly to that phrase

### Requirement 9

**User Story:** As a developer, I want the phrase data to be easily extensible and support dynamic generation, so that new phrase packs can be added without code changes and personalized scenarios can be created.

#### Acceptance Criteria

1. WHEN adding a new phrase pack THEN the developer SHALL only need to provide a JSON configuration file
2. WHEN the system loads phrase packs THEN the system SHALL validate the configuration against a defined schema
3. WHEN a configuration is invalid THEN the system SHALL report specific validation errors
4. WHEN phrase packs are updated THEN the system SHALL preserve user progress for existing phrases

### Requirement 10

**User Story:** As a returning user, I want to access dynamically generated scenarios based on my learning needs, so that I can practice phrases most relevant to my situation.

#### Acceptance Criteria

1. WHEN a user requests a personalized scenario THEN the system SHALL support loading scenarios from backend API
2. WHEN a dynamic scenario is generated THEN the system SHALL cache it locally for offline access
3. WHEN displaying scenarios THEN the system SHALL distinguish between built-in and user-generated scenarios
4. WHEN the backend is unavailable THEN the system SHALL fall back to locally cached and mock data
