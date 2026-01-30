# Design Document: Sentence Building Module

## Overview

句型构建模块是 DuoXX 应用的核心学习功能之一，通过填空补全、连词成句和语法模式练习帮助用户掌握英语句型结构。该模块遵循项目的模块化架构，复用现有的评分系统、间隔重复服务和反馈组件。

### Key Features
- 填空补全练习（Fill-in-the-Blank）
- 连词成句练习（Word Ordering / Drag-and-Drop）
- 语法模式学习（Grammar Pattern Learning）
- 基于 CEFR 等级的难度适配
- 三种学习模式：智能学习、复习、挑战
- 年龄适配的反馈机制

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Sentence Building Module                  │
├─────────────────────────────────────────────────────────────┤
│  Screens                                                     │
│  ├── SentenceBuildingScreen (模块主页)                       │
│  ├── SentenceExerciseScreen (练习页面)                       │
│  └── SentenceCompleteScreen (完成页面)                       │
├─────────────────────────────────────────────────────────────┤
│  Components                                                  │
│  ├── FillBlankExercise (填空练习组件)                        │
│  ├── WordOrderingExercise (连词成句组件)                     │
│  └── GrammarPatternCard (语法模式卡片)                       │
├─────────────────────────────────────────────────────────────┤
│  Services                                                    │
│  └── sentenceProgressService (进度服务)                      │
├─────────────────────────────────────────────────────────────┤
│  Data                                                        │
│  ├── sentenceTemplates.ts (句子模板数据)                     │
│  └── grammarPatterns.ts (语法模式数据)                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Shared Services                           │
│  ├── spacedRepetitionService (间隔重复算法)                  │
│  ├── scoringService (评分服务)                               │
│  └── soundService (音效服务)                                 │
└─────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. Exercise Types

```typescript
// 练习类型枚举
enum SentenceExerciseType {
  FILL_BLANK = 'fill-blank',      // 填空
  WORD_ORDER = 'word-order',      // 连词成句
  GRAMMAR_PATTERN = 'grammar',    // 语法模式
}

// 填空练习接口
interface FillBlankExercise {
  id: string;
  type: SentenceExerciseType.FILL_BLANK;
  sentence: string;              // 带 {blank} 占位符的句子
  blanks: BlankSlot[];           // 空格定义
  translation: string;           // 中文翻译
  grammarPattern?: string;       // 关联的语法模式
  difficulty: CEFRLevel;
  xpReward: number;
}

interface BlankSlot {
  index: number;                 // 空格位置
  correctAnswer: string;         // 正确答案
  options: string[];             // 选项（包含正确答案和干扰项）
  hint?: string;                 // 提示
}

// 连词成句练习接口
interface WordOrderExercise {
  id: string;
  type: SentenceExerciseType.WORD_ORDER;
  words: string[];               // 打乱的单词列表
  correctOrder: number[];        // 正确顺序的索引
  translation: string;           // 中文翻译
  grammarPattern?: string;
  difficulty: CEFRLevel;
  xpReward: number;
}

// 语法模式接口
interface GrammarPattern {
  id: string;
  name: string;                  // 如 "SVO 主谓宾"
  structure: string;             // 如 "Subject + Verb + Object"
  description: string;
  examples: GrammarExample[];
  difficulty: CEFRLevel;
}

interface GrammarExample {
  sentence: string;
  translation: string;
  breakdown: string[];           // 结构拆解
}
```

### 2. Progress Tracking

```typescript
// 用户句型学习状态
interface UserSentenceState {
  sentenceId: string;
  userId: string;
  totalAttempts: number;
  correctAttempts: number;
  correctRate: number;
  masteryScore: number;
  masteryLevel: MasteryLevel;
  firstLearnedAt: string | null;
  lastPracticedAt: string | null;
  nextReviewAt: string | null;
}

// 语法模式掌握状态
interface UserGrammarState {
  patternId: string;
  userId: string;
  practiceCount: number;
  masteryScore: number;
  lastPracticedAt: string | null;
}
```

### 3. Screen Components

#### SentenceBuildingScreen (模块主页)
- 显示学习进度统计（已学句型、已掌握、待复习）
- 提供三种学习模式入口
- 显示推荐的语法模式

#### SentenceExerciseScreen (练习页面)
- 根据练习类型渲染不同的练习组件
- 处理答题逻辑和反馈
- 支持年龄适配的反馈模式

#### FillBlankExercise (填空练习组件)
- 渲染带空格的句子
- 提供选项按钮
- 支持多空格练习

#### WordOrderingExercise (连词成句组件)
- 多邻国风格交互：点击单词添加到答案区，再点击可移除
- 分为两个区域：答案区（已选单词）和单词池（可选单词）
- 已选单词在单词池中显示为占位符

## Data Models

### Sentence Template Schema

```typescript
interface SentenceTemplate {
  id: string;
  category: string;              // 分类：日常、商务、旅行等
  sentence: string;              // 完整句子
  translation: string;
  words: string[];               // 分词列表
  grammarPatterns: string[];     // 关联的语法模式 ID
  difficulty: CEFRLevel;
  tags: string[];
}
```

### Exercise Generation

练习生成逻辑：
1. 根据用户 CEFR 等级筛选句子模板
2. 根据学习模式选择内容（新学/复习/挑战）
3. 随机生成练习类型（填空/连词成句）
4. 生成干扰项（基于词性、常见错误）

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Correct answer awards XP
*For any* exercise and correct answer submission, the user's XP should increase by the exercise's xpReward value and progress should be recorded.
**Validates: Requirements 1.3, 2.5**

### Property 2: Fill-blank exercise displays blanks and options
*For any* valid fill-blank exercise data, the rendered output should contain the correct number of blanks and each blank should have selectable options including the correct answer.
**Validates: Requirements 1.1**

### Property 3: Incorrect answer shows correct answer
*For any* incorrect answer submission, the system should return the correct answer in the feedback response.
**Validates: Requirements 1.4**

### Property 4: Word ordering validation correctness
*For any* word arrangement submitted, the validation function should return true if and only if the arrangement matches the correct order.
**Validates: Requirements 2.4**

### Property 5: Incorrect word order identifies wrong positions
*For any* incorrect word arrangement, the system should correctly identify which positions differ from the correct order.
**Validates: Requirements 2.6**

### Property 6: Grammar pattern data completeness
*For any* grammar pattern, the data should include at least one example with sentence and translation.
**Validates: Requirements 3.2**

### Property 7: Grammar practice recording
*For any* completed grammar pattern exercise, the pattern ID should be recorded in the user's progress state.
**Validates: Requirements 3.4**

### Property 8: CEFR level filtering
*For any* user CEFR level, generated exercises should only include content with difficulty at or below that level (except in challenge mode).
**Validates: Requirements 4.1**

### Property 9: Session summary calculation
*For any* completed exercise session with known results, the summary should correctly calculate total XP and accuracy rate.
**Validates: Requirements 5.1**

### Property 10: Progress persistence round-trip
*For any* progress state, saving and then loading should produce an equivalent state.
**Validates: Requirements 5.4**

### Property 11: Smart learn mode level matching
*For any* user in smart learn mode, returned exercises should match the user's CEFR level.
**Validates: Requirements 6.2**

### Property 12: Review mode prioritization
*For any* user with due review items, review mode should return due items before non-due items.
**Validates: Requirements 6.3**

### Property 13: Challenge mode difficulty increase
*For any* user in challenge mode, returned exercises should have difficulty above the user's current CEFR level.
**Validates: Requirements 6.4**

## Error Handling

### User Input Errors
- 空选择：禁用提交按钮直到用户选择所有单词
- 部分选择：显示剩余需选择的单词数量
- 网络错误：本地缓存进度，稍后同步

### Data Errors
- 无效练习数据：跳过并记录日志
- 空句子模板：显示友好提示，返回模块主页

### State Errors
- 进度加载失败：使用默认初始状态
- 保存失败：重试机制 + 用户提示

## Testing Strategy

### Unit Testing
- 练习验证函数测试
- 进度计算函数测试
- 干扰项生成函数测试

### Property-Based Testing
使用 fast-check 库进行属性测试：

```typescript
// 示例：验证函数正确性
fc.assert(
  fc.property(
    fc.array(fc.string()),  // 单词数组
    fc.array(fc.nat()),     // 用户排序
    (words, userOrder) => {
      const correctOrder = [...Array(words.length).keys()];
      const isCorrect = validateWordOrder(userOrder, correctOrder);
      // 属性：当且仅当顺序完全匹配时返回 true
      return isCorrect === arraysEqual(userOrder, correctOrder);
    }
  ),
  { numRuns: 100 }
);
```

### Integration Testing
- 模块注册测试
- 路由导航测试
- 进度持久化测试

### Testing Framework
- Jest with ts-jest preset
- fast-check for property-based testing
- React Native Testing Library for component tests
