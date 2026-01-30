# Imperfect Dialogue Design Document

## Overview

不完美对话模块是一个容错性口语练习系统，强调"没有错误答案"的学习理念。通过多级评分（acceptable/better/native）给予用户渐进式反馈，降低口语练习焦虑，鼓励大胆尝试。

核心特点：
- 多级评分而非对/错二元判断
- 接受多种表达变体
- Speaking Avatar 示范不同等级表达
- 渐进式提示系统
- 与错题本融合的进度追踪

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    ImperfectDialogueScreen (UI)                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ ScenarioView│  │ ResponseInput│ │ FeedbackPanel           │  │
│  │ (场景展示)  │  │ (输入/录音) │  │ (多级反馈)              │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   ImperfectDialogueEngine                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │ ResponseEvaluator│ │ HintProvider    │  │ ProgressTracker │  │
│  │ - Multi-level   │  │ - Progressive   │  │ - Level stats   │  │
│  │ - Variations    │  │ - Disclosure    │  │ - Error book    │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Shared Services                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │ SpeakingAvatar  │  │ SpeechRecognition│ │ ErrorCollection │  │
│  │ (口型同步)      │  │ (语音识别)       │  │ (错题本融合)    │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```


## Components and Interfaces

### Core Types

```typescript
// 回答等级
export enum ResponseLevel {
  ACCEPTABLE = 'acceptable',
  BETTER = 'better',
  NATIVE = 'native',
}

// 场景类别
export enum DialogueCategory {
  SOCIAL = 'social',
  BUSINESS = 'business',
  TRAVEL = 'travel',
  DAILY = 'daily',
  EMERGENCY = 'emergency',
}

// 对话提示
export interface DialoguePrompt {
  id: string;
  context: string;           // 场景描述
  speakerLine: string;       // 对方说的话
  speakerName: string;       // 对方名字
  expectedResponses: ExpectedResponse[];
  hints: HintLevel[];
}

// 期望回答（多级）
export interface ExpectedResponse {
  level: ResponseLevel;
  text: string;
  explanation: string;
  keyPhrases?: string[];     // native 级别的关键短语
  culturalNote?: string;     // 文化背景说明
}

// 提示等级
export interface HintLevel {
  level: number;             // 1, 2, 3
  content: string;           // 提示内容
  type: 'first_word' | 'structure' | 'full_example';
}

// 对话场景
export interface DialogueScenario {
  id: string;
  title: string;
  description: string;
  category: DialogueCategory;
  prompts: DialoguePrompt[];
  source: 'builtin' | 'dynamic';
}

// 评估结果
export interface EvaluationResult {
  userResponse: string;
  matchedLevel: ResponseLevel;
  matchedResponse?: ExpectedResponse;
  betterAlternative?: ExpectedResponse;
  nativeAlternative?: ExpectedResponse;
  feedback: string;
  pronunciationIssues?: PronunciationIssue[];
}

// 发音问题
export interface PronunciationIssue {
  word: string;
  issue: string;
  suggestion: string;
}

// 进度记录
export interface DialogueProgress {
  scenarioId: string;
  completedAt: string;
  levelDistribution: Record<ResponseLevel, number>;
  hintsUsed: number;
  totalPrompts: number;
}
```


### ResponseEvaluator Interface

```typescript
export interface IResponseEvaluator {
  // 评估回答
  evaluate(userResponse: string, prompt: DialoguePrompt): EvaluationResult;
  
  // 检查是否匹配某个等级
  matchesLevel(userResponse: string, expected: ExpectedResponse): boolean;
  
  // 获取鼓励性反馈文本
  getEncouragingFeedback(level: ResponseLevel): string;
  
  // 检查语法正确性（宽松模式）
  isGrammaticallyAcceptable(response: string): boolean;
}
```

### HintProvider Interface

```typescript
export interface IHintProvider {
  // 获取下一级提示
  getNextHint(prompt: DialoguePrompt, currentLevel: number): HintLevel | null;
  
  // 获取所有提示
  getAllHints(prompt: DialoguePrompt): HintLevel[];
  
  // 记录提示使用
  recordHintUsage(promptId: string, hintLevel: number): void;
  
  // 获取提示使用统计
  getHintStats(): HintStats;
}
```

### ProgressTracker Interface

```typescript
export interface IProgressTracker {
  // 记录完成
  recordCompletion(progress: DialogueProgress): void;
  
  // 获取等级分布
  getLevelDistribution(): Record<ResponseLevel, number>;
  
  // 检测改进
  detectImprovement(scenarioId: string): ImprovementInfo | null;
  
  // 与错题本同步
  syncToErrorBook(): Promise<void>;
  
  // 获取历史记录
  getHistory(): DialogueProgress[];
}
```

## Data Models

### Dialogue Scenario Configuration (JSON)

```json
{
  "id": "coffee-shop-order",
  "title": "咖啡店点单",
  "description": "在咖啡店点一杯咖啡",
  "category": "daily",
  "source": "builtin",
  "prompts": [
    {
      "id": "prompt-001",
      "context": "你走进一家咖啡店，店员微笑着迎接你",
      "speakerName": "Barista",
      "speakerLine": "Hi! What can I get for you today?",
      "expectedResponses": [
        {
          "level": "acceptable",
          "text": "I want a coffee.",
          "explanation": "语法正确，但比较直接"
        },
        {
          "level": "better",
          "text": "Can I have a latte, please?",
          "explanation": "更礼貌，使用了 'please'"
        },
        {
          "level": "native",
          "text": "I'll have a medium latte, please.",
          "explanation": "自然流畅，包含具体规格",
          "keyPhrases": ["I'll have", "medium"],
          "culturalNote": "美国人点单时常用 'I'll have...' 而不是 'I want...'"
        }
      ],
      "hints": [
        { "level": 1, "content": "I...", "type": "first_word" },
        { "level": 2, "content": "I'll have a ___", "type": "structure" },
        { "level": 3, "content": "I'll have a medium latte, please.", "type": "full_example" }
      ]
    }
  ]
}
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Evaluation Level Validity
*For any* user response evaluation, the result SHALL contain a matchedLevel that is one of: acceptable, better, or native.
**Validates: Requirements 2.1**

### Property 2: Better Alternative Presence
*For any* evaluation result with matchedLevel = acceptable, the result SHALL include a non-null betterAlternative.
**Validates: Requirements 2.2**

### Property 3: Native Alternative Presence
*For any* evaluation result with matchedLevel = better, the result SHALL include a non-null nativeAlternative.
**Validates: Requirements 2.3**

### Property 4: Encouraging Feedback Language
*For any* evaluation feedback text, the text SHALL NOT contain negative words such as "wrong", "incorrect", "failed", or "error".
**Validates: Requirements 1.4**

### Property 5: Multi-Variation Matching
*For any* user response that matches any of the expectedResponses variations, the evaluation SHALL return a successful match.
**Validates: Requirements 1.2**

### Property 6: Native Response Key Phrases
*For any* native-level ExpectedResponse, the keyPhrases array SHALL contain at least one non-empty string.
**Validates: Requirements 3.2**

### Property 7: Progressive Hint Disclosure
*For any* DialoguePrompt with hints, the hints SHALL be ordered by level (1, 2, 3) with increasing detail.
**Validates: Requirements 8.2**

### Property 8: Hint Usage Independence
*For any* evaluation after hint usage, the evaluation logic SHALL produce the same matchedLevel as without hints.
**Validates: Requirements 8.3**

### Property 9: Scenario Context Completeness
*For any* DialogueScenario, all prompts SHALL have non-empty context and speakerLine fields.
**Validates: Requirements 5.1**

### Property 10: Multi-Turn Connectivity
*For any* DialogueScenario with multiple prompts, the prompts SHALL form a connected conversation flow.
**Validates: Requirements 5.2**

### Property 11: Progress Level Distribution
*For any* DialogueProgress record, the levelDistribution SHALL contain counts for all three ResponseLevel values.
**Validates: Requirements 6.2**

### Property 12: Error Book Integration Format
*For any* weakness record from dialogue practice, the converted ErrorRecord SHALL be compatible with the global error book schema.
**Validates: Requirements 6.4**

### Property 13: Scenario Configuration Validation
*For any* invalid scenario configuration, the validator SHALL return specific error messages identifying the invalid fields.
**Validates: Requirements 7.3**

### Property 14: Hint Count Tracking
*For any* dialogue completion with hints used, the hintsUsed count SHALL equal the total number of hints requested.
**Validates: Requirements 8.4**


## Error Handling

### Error Types

```typescript
export enum ImperfectDialogueErrorCode {
  SCENARIO_NOT_FOUND = 'SCENARIO_NOT_FOUND',
  INVALID_SCENARIO_CONFIG = 'INVALID_SCENARIO_CONFIG',
  SPEECH_RECOGNITION_FAILED = 'SPEECH_RECOGNITION_FAILED',
  RECORDING_FAILED = 'RECORDING_FAILED',
  EVALUATION_FAILED = 'EVALUATION_FAILED',
  DYNAMIC_LOAD_FAILED = 'DYNAMIC_LOAD_FAILED',
}
```

### Error Handling Strategy

1. **语音识别失败**: 提示用户重试或切换到文字输入
2. **场景加载失败**: 回退到本地缓存或 mock 数据
3. **评估失败**: 默认返回 acceptable 级别，记录错误日志
4. **录音失败**: 提示用户检查麦克风权限

## Testing Strategy

### Property-Based Testing Framework

使用 **fast-check** 作为属性测试库，配置每个属性测试运行至少 100 次迭代。

### Test Categories

1. **ResponseEvaluator Tests**
   - 多级评分正确性
   - 变体匹配覆盖
   - 反馈语言检查

2. **HintProvider Tests**
   - 渐进式提示顺序
   - 提示使用统计

3. **ProgressTracker Tests**
   - 等级分布记录
   - 错题本格式兼容

4. **Integration Tests**
   - Speaking Avatar 集成
   - 语音识别集成

### Test Annotation Format

```typescript
/**
 * **Feature: imperfect-dialogue, Property 1: Evaluation Level Validity**
 * **Validates: Requirements 2.1**
 */
it('should return valid response level', () => {
  fc.assert(
    fc.property(userResponseArb, promptArb, (response, prompt) => {
      const result = evaluator.evaluate(response, prompt);
      return Object.values(ResponseLevel).includes(result.matchedLevel);
    }),
    { numRuns: 100 }
  );
});
```
