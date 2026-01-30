# Survival Phrases Design Document

## Overview

救命锦囊模块是一个实用表达学习系统，专注于紧急场景下的必备短语。该模块采用"主动灌输"策略，通过 Speaking Avatar 口型示范、错误矫正和弱点追踪，帮助用户掌握实用表达。

核心特点：
- 场景驱动的短语学习
- Speaking Avatar 口型同步示范
- 弱点识别与错题本融合
- 支持动态场景生成（后端扩展）
- 离线访问支持

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SurvivalPhrasesScreen (UI)                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ PackListView│  │ PhraseCard  │  │ PracticeScreen          │  │
│  │ (场景列表)  │  │ (短语卡片)  │  │ (练习界面)              │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   SurvivalPhrasesEngine                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │ PhraseManager   │  │ PracticeEngine  │  │ WeaknessTracker │  │
│  │ - Load packs    │  │ - Speaking      │  │ - Record errors │  │
│  │ - Search        │  │ - Pronunciation │  │ - Categorize    │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Shared Services                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │ SpeakingAvatar  │  │ ErrorCollection │  │ CacheService    │  │
│  │ (口型同步)      │  │ (错题本融合)    │  │ (离线缓存)      │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```


## Components and Interfaces

### Core Types

```typescript
// 场景类型
export enum SurvivalScenario {
  AIRPORT = 'airport',
  HOSPITAL = 'hospital',
  HOTEL = 'hotel',
  RESTAURANT = 'restaurant',
  EMERGENCY = 'emergency',
  SHOPPING = 'shopping',
  TRANSPORTATION = 'transportation',
  CUSTOMS = 'customs',
}

// 错误类型
export enum PhraseErrorType {
  PRONUNCIATION = 'pronunciation',
  WORD_CHOICE = 'word_choice',
  GRAMMAR_PATTERN = 'grammar_pattern',
  WORD_ORDER = 'word_order',
}

// 短语定义
export interface SurvivalPhrase {
  id: string;
  english: string;
  chinese: string;
  phonetic: string;
  scenario: SurvivalScenario;
  usageContext: string;
  examples: PhraseExample[];
  commonMistakes: CommonMistake[];
  audioUrl?: string;
}

// 用法示例
export interface PhraseExample {
  id: string;
  dialogue: DialogueLine[];
  context: string;
}

// 对话行
export interface DialogueLine {
  speaker: string;
  text: string;
  isTargetPhrase: boolean;
}

// 常见错误
export interface CommonMistake {
  incorrect: string;
  correct: string;
  errorType: PhraseErrorType;
  explanation: string;
}

// 锦囊包
export interface PhrasePack {
  id: string;
  name: string;
  description: string;
  scenario: SurvivalScenario;
  icon: string;
  color: string;
  phrases: SurvivalPhrase[];
  source: 'builtin' | 'dynamic';
}

// 弱点记录
export interface PhraseWeakness {
  phraseId: string;
  errorType: PhraseErrorType;
  errorCount: number;
  lastErrorAt: string;
  isImproved: boolean;
}
```


### PhraseManager Interface

```typescript
export interface IPhraseManager {
  // 加载锦囊包
  loadPhrasePacks(): Promise<PhrasePack[]>;
  getPacksByScenario(scenario: SurvivalScenario): PhrasePack[];
  getPackById(packId: string): PhrasePack | undefined;
  
  // 搜索
  search(query: string): SearchResult[];
  getSuggestions(query: string): PhrasePack[];
  
  // 动态场景
  loadDynamicScenario(scenarioId: string): Promise<PhrasePack | null>;
  cacheDynamicScenario(pack: PhrasePack): Promise<void>;
  
  // 验证
  validatePackConfig(config: unknown): ValidationResult;
}
```

### WeaknessTracker Interface

```typescript
export interface IWeaknessTracker {
  // 记录弱点
  recordWeakness(phraseId: string, errorType: PhraseErrorType): void;
  
  // 查询弱点
  getWeaknesses(): PhraseWeakness[];
  getWeaknessesByType(errorType: PhraseErrorType): PhraseWeakness[];
  getWeaknessStats(): WeaknessStats;
  
  // 更新状态
  markImproved(phraseId: string): void;
  
  // 与错题本融合
  syncToErrorBook(): Promise<void>;
  getErrorBookCompatibleRecords(): ErrorRecord[];
}
```

### PracticeEngine Interface

```typescript
export interface IPracticeEngine {
  // 开始练习
  startPractice(phraseId: string): void;
  
  // 发音练习
  recordPronunciation(): Promise<PronunciationResult>;
  getPronunciationFeedback(): PronunciationFeedback;
  
  // 错误检测
  detectCommonMistake(userInput: string, phrase: SurvivalPhrase): CommonMistake | null;
  
  // 完成练习
  completePractice(result: PracticeResult): void;
}
```

## Data Models

### Phrase Pack Configuration (JSON)

```json
{
  "id": "airport-essentials",
  "name": "机场必备",
  "description": "机场常用表达，从值机到登机",
  "scenario": "airport",
  "icon": "airplane-outline",
  "color": "#3B82F6",
  "source": "builtin",
  "phrases": [
    {
      "id": "airport-001",
      "english": "Where is the check-in counter?",
      "chinese": "值机柜台在哪里？",
      "phonetic": "/weər ɪz ðə ˈtʃek.ɪn ˈkaʊn.tər/",
      "usageContext": "刚到机场，需要找值机柜台时使用",
      "examples": [
        {
          "id": "ex-001",
          "context": "在机场大厅询问工作人员",
          "dialogue": [
            { "speaker": "You", "text": "Excuse me, where is the check-in counter?", "isTargetPhrase": true },
            { "speaker": "Staff", "text": "It's on the second floor, turn left after the escalator.", "isTargetPhrase": false }
          ]
        }
      ],
      "commonMistakes": [
        {
          "incorrect": "Where is check-in counter?",
          "correct": "Where is the check-in counter?",
          "errorType": "grammar_pattern",
          "explanation": "需要使用定冠词 'the' 指代特定的值机柜台"
        }
      ]
    }
  ]
}
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Phrase Pack Grouping Consistency
*For any* set of phrase packs, grouping by scenario SHALL produce groups where all phrases in each group have the same scenario type.
**Validates: Requirements 1.1**

### Property 2: Phrase Display Completeness
*For any* survival phrase, the rendered display SHALL include non-empty values for english, chinese, phonetic, and usageContext fields.
**Validates: Requirements 1.3**

### Property 3: Search Coverage
*For any* search query, the search function SHALL return results that match against phrase english text, chinese translation, or scenario description.
**Validates: Requirements 8.1**

### Property 4: Search Relevance Ordering
*For any* search results, results with exact matches SHALL appear before partial matches.
**Validates: Requirements 8.2**

### Property 5: Weakness Recording Completeness
*For any* error recorded during practice, the weakness record SHALL include a valid phraseId and errorType from the defined enum.
**Validates: Requirements 3.1, 3.2**

### Property 6: Error Book Integration Format
*For any* weakness record, the converted ErrorRecord SHALL be compatible with the global error book schema.
**Validates: Requirements 3.4**

### Property 7: Common Mistake Detection Accuracy
*For any* user input that matches a known common mistake pattern, the detection function SHALL return the corresponding CommonMistake object.
**Validates: Requirements 4.2**

### Property 8: Example Dialogue Highlighting
*For any* phrase example dialogue, exactly one dialogue line SHALL have isTargetPhrase set to true.
**Validates: Requirements 5.2**

### Property 9: Pack Configuration Validation
*For any* invalid phrase pack configuration, the validator SHALL return specific error messages identifying the invalid fields.
**Validates: Requirements 9.3**

### Property 10: Scenario Source Identification
*For any* phrase pack, the source field SHALL correctly identify whether it is 'builtin' or 'dynamic'.
**Validates: Requirements 10.3**

### Property 11: Offline Cache Consistency
*For any* favorited phrase pack, the cached version SHALL contain all phrases from the original pack.
**Validates: Requirements 7.1**

### Property 12: Pronunciation Feedback Word Coverage
*For any* pronunciation feedback with errors, the feedback SHALL identify specific words that need improvement.
**Validates: Requirements 6.3**


## Error Handling

### Error Types

```typescript
export enum SurvivalPhrasesErrorCode {
  PACK_NOT_FOUND = 'PACK_NOT_FOUND',
  INVALID_PACK_CONFIG = 'INVALID_PACK_CONFIG',
  PHRASE_NOT_FOUND = 'PHRASE_NOT_FOUND',
  AUDIO_LOAD_FAILED = 'AUDIO_LOAD_FAILED',
  TTS_UNAVAILABLE = 'TTS_UNAVAILABLE',
  CACHE_WRITE_FAILED = 'CACHE_WRITE_FAILED',
  DYNAMIC_LOAD_FAILED = 'DYNAMIC_LOAD_FAILED',
  RECORDING_FAILED = 'RECORDING_FAILED',
}
```

### Error Handling Strategy

1. **TTS 不可用**: 显示文本和音标，隐藏 Speaking Avatar
2. **动态场景加载失败**: 回退到本地缓存或 mock 数据
3. **录音失败**: 提示用户检查麦克风权限
4. **缓存写入失败**: 继续使用在线模式，提示存储空间不足

## Testing Strategy

### Property-Based Testing Framework

使用 **fast-check** 作为属性测试库，配置每个属性测试运行至少 100 次迭代。

### Test Categories

1. **PhraseManager Tests**
   - 锦囊包加载和分组
   - 搜索功能覆盖和排序
   - 配置验证

2. **WeaknessTracker Tests**
   - 弱点记录完整性
   - 错题本格式兼容性
   - 统计计算准确性

3. **PracticeEngine Tests**
   - 常见错误检测
   - 发音反馈生成

4. **Integration Tests**
   - Speaking Avatar 集成
   - 离线缓存一致性

### Test Annotation Format

```typescript
/**
 * **Feature: survival-phrases, Property 1: Phrase Pack Grouping Consistency**
 * **Validates: Requirements 1.1**
 */
it('should group phrases by scenario correctly', () => {
  fc.assert(
    fc.property(phrasePackArb, (packs) => {
      // Test implementation
    }),
    { numRuns: 100 }
  );
});
```
