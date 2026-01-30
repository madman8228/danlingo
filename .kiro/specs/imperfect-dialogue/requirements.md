# Requirements Document

## Introduction

不完美对话（Imperfect Dialogue）是一个面向成人英语学习者的口语练习模块，强调"容错性"和"真实性"。与传统对话练习不同，该模块不追求完美答案，而是接受多种表达方式，通过多级评分（可接受/更好/地道）给予用户渐进式反馈。这种设计降低了口语练习的焦虑感，鼓励用户大胆尝试，逐步提升表达的地道程度。

## Glossary

- **Imperfect Dialogue**: 不完美对话，允许多种表达方式的对话练习模式
- **Response Level**: 回答等级，对用户回答的多级评价（acceptable/better/native）
- **Dialogue Scenario**: 对话场景，模拟真实生活的对话情境
- **Speaking Avatar**: 说话助教，提供口型同步示范的卡通角色
- **Acceptable Response**: 可接受回答，语法正确但可能不够地道的表达
- **Better Response**: 更好回答，更自然流畅的表达方式
- **Native Response**: 地道回答，母语者常用的表达方式

## Requirements

### Requirement 1

**User Story:** As a learner, I want to practice dialogues without fear of making mistakes, so that I can build confidence in speaking English.

#### Acceptance Criteria

1. WHEN a user enters a dialogue scenario THEN the system SHALL present the context and prompt without showing expected answers
2. WHEN the user provides a response THEN the system SHALL evaluate it against multiple acceptable variations
3. WHEN the response is grammatically correct THEN the system SHALL accept it regardless of whether it matches the ideal answer
4. WHEN displaying feedback THEN the system SHALL use encouraging language without marking responses as "wrong"

### Requirement 2

**User Story:** As a learner, I want to see how my response compares to more native expressions, so that I can gradually improve my speaking naturalness.

#### Acceptance Criteria

1. WHEN evaluating a response THEN the system SHALL classify it into one of three levels: acceptable, better, or native
2. WHEN the response is acceptable THEN the system SHALL show a "better" alternative with explanation
3. WHEN the response is better THEN the system SHALL show a "native" alternative with cultural context
4. WHEN the response is native-level THEN the system SHALL celebrate the achievement with Speaking Avatar animation


### Requirement 3

**User Story:** As a learner, I want to hear native speakers demonstrate different response levels, so that I can understand the nuances between expressions.

#### Acceptance Criteria

1. WHEN displaying response alternatives THEN the Speaking Avatar SHALL demonstrate each level with appropriate lip sync
2. WHEN demonstrating a native response THEN the system SHALL highlight key phrases that make it sound natural
3. WHEN the user requests replay THEN the system SHALL allow replaying any demonstrated response
4. WHEN comparing responses THEN the system SHALL visually distinguish between acceptable, better, and native levels

### Requirement 4

**User Story:** As a learner, I want to practice speaking my responses out loud, so that I can improve my pronunciation and fluency.

#### Acceptance Criteria

1. WHEN the user chooses to speak THEN the system SHALL record their audio response
2. WHEN evaluating spoken response THEN the system SHALL use speech recognition to transcribe the response
3. WHEN transcription is complete THEN the system SHALL evaluate the transcribed text against acceptable variations
4. WHEN pronunciation issues are detected THEN the system SHALL provide specific feedback on problematic words

### Requirement 5

**User Story:** As a learner, I want dialogue scenarios that reflect real-life situations, so that I can apply what I learn in actual conversations.

#### Acceptance Criteria

1. WHEN displaying scenarios THEN the system SHALL provide realistic context descriptions
2. WHEN a scenario involves multiple turns THEN the system SHALL maintain conversation flow naturally
3. WHEN the user completes a scenario THEN the system SHALL summarize key expressions learned
4. WHEN scenarios are categorized THEN the system SHALL organize them by situation type (social, business, travel, etc.)

### Requirement 6

**User Story:** As a learner, I want the system to track my progress across different expression levels, so that I can see my improvement over time.

#### Acceptance Criteria

1. WHEN a user completes a dialogue THEN the system SHALL record the response levels achieved
2. WHEN displaying progress THEN the system SHALL show the distribution of acceptable/better/native responses
3. WHEN the user improves from acceptable to better THEN the system SHALL acknowledge the improvement
4. WHEN tracking weaknesses THEN the system SHALL integrate with the global error book for unified review

### Requirement 7

**User Story:** As a developer, I want the dialogue scenarios to be data-driven, so that new scenarios can be added without code changes.

#### Acceptance Criteria

1. WHEN adding a new scenario THEN the developer SHALL only need to provide a JSON configuration file
2. WHEN the system loads scenarios THEN the system SHALL validate the configuration against a defined schema
3. WHEN a configuration is invalid THEN the system SHALL report specific validation errors
4. WHEN scenarios support dynamic generation THEN the system SHALL support loading from backend API

### Requirement 8

**User Story:** As a learner, I want hints when I'm stuck, so that I can continue practicing without giving up.

#### Acceptance Criteria

1. WHEN the user requests a hint THEN the system SHALL provide a partial response or key phrase
2. WHEN providing hints THEN the system SHALL use progressive disclosure (first word, key structure, full example)
3. WHEN the user uses a hint THEN the system SHALL still evaluate their final response fairly
4. WHEN multiple hints are used THEN the system SHALL track this for learning analytics
