# Speaking Avatar Design Document

## Overview

Speaking Avatar 是一个可复用的口型同步动画模块，为 DuoXX 语言学习应用提供生动的卡通助教角色。该模块支持：

- 根据文本或音频进行口型同步动画
- 多种可扩展的卡通角色
- 可配置的表情系统
- 多语言音素映射支持
- 与现有 Avatar 系统的无缝集成

模块采用数据驱动的架构设计，允许通过配置文件扩展角色、表情和语言支持，无需修改核心代码。

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SpeakingAvatarView (UI)                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ CharacterLayer│ │ VisemeLayer │ │ ExpressionLayer         │  │
│  │ (Base Image) │ │ (Mouth Anim)│ │ (Eyes, Brows, etc.)     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   SpeakingAvatarController                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │ LipSyncEngine   │  │ ExpressionEngine│  │ AnimationEngine │  │
│  │ - Viseme timing │  │ - Expression    │  │ - Idle anims    │  │
│  │ - Phoneme map   │  │   blending      │  │ - Transitions   │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Services Layer                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │ AudioService    │  │ PhonemeService  │  │ TTSService      │  │
│  │ - Playback      │  │ - Text→Phoneme  │  │ - expo-speech   │  │
│  │ - Duration      │  │ - Timing est.   │  │ - Fallback      │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Registries (Data-Driven)                    │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │ CharacterRegistry│ │ ExpressionRegistry│ │ LanguageRegistry│  │
│  │ - Config files  │  │ - Expression defs│  │ - Phoneme maps │  │
│  │ - Asset bundles │  │ - Transitions    │  │ - Viseme tables│  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### Core Types

```typescript
// 视位类型 - 嘴型形状
export enum Viseme {
  SILENT = 0,      // 闭嘴/静音
  AA = 1,          // "ah" 如 father
  EE = 2,          // "ee" 如 see
  IH = 3,          // "ih" 如 sit
  OH = 4,          // "oh" 如 go
  OO = 5,          // "oo" 如 too
  EH = 6,          // "eh" 如 bed
  AH = 7,          // "uh" 如 but
  TH = 8,          // "th" 如 think
  FV = 9,          // "f/v" 如 five
  MBP = 10,        // "m/b/p" 如 map
  LN = 11,         // "l/n" 如 lion
  WR = 12,         // "w/r" 如 water
  SS = 13,         // "s/z" 如 sun
  SH = 14,         // "sh/ch" 如 ship
  KG = 15,         // "k/g" 如 king
}

// 角色配置
export interface CharacterConfig {
  id: string;
  name: string;
  description: string;
  ageGroups: AgeGroup[];
  assets: CharacterAssets;
  defaultExpression: ExpressionId;
}

// 角色资源
export interface CharacterAssets {
  baseImage: string;           // 基础角色图片
  visemeImages: Record<Viseme, string>;  // 各视位嘴型图片
  expressionOverlays: Record<ExpressionId, string>;  // 表情叠加层
}

// 表情配置
export interface ExpressionConfig {
  id: ExpressionId;
  name: string;
  eyeState: EyeState;
  browState: BrowState;
  transitionDuration: number;
  easing: EasingFunction;
}

// 口型同步数据
export interface LipSyncData {
  visemes: VisemeFrame[];
  duration: number;
  text: string;
}

// 视位帧
export interface VisemeFrame {
  viseme: Viseme;
  startTime: number;
  duration: number;
}

// 语言映射配置
export interface LanguageMapping {
  languageCode: string;
  phonemeToViseme: Record<string, Viseme>;
}
```

### SpeakingAvatarView Component

```typescript
export interface SpeakingAvatarProps {
  // 必需属性
  characterId: string;
  
  // 输入源 (二选一)
  text?: string;
  audioUrl?: string;
  
  // 可选配置
  language?: string;           // 默认 'en'
  size?: 'small' | 'medium' | 'large';
  animationSpeed?: number;     // 默认 1.0
  expression?: ExpressionId;
  autoPlay?: boolean;          // 默认 true
  
  // 回调
  onPlaybackStart?: () => void;
  onPlaybackEnd?: () => void;
  onVisemeChange?: (viseme: Viseme) => void;
  onError?: (error: SpeakingAvatarError) => void;
  
  // 样式
  style?: ViewStyle;
}
```

### SpeakingAvatarController

```typescript
export interface ISpeakingAvatarController {
  // 播放控制
  speak(text: string, options?: SpeakOptions): Promise<void>;
  speakWithAudio(audioUrl: string, text: string): Promise<void>;
  stop(): void;
  pause(): void;
  resume(): void;
  
  // 状态查询
  isSpeaking(): boolean;
  getCurrentViseme(): Viseme;
  getPlaybackProgress(): number;
  
  // 表情控制
  setExpression(expression: ExpressionId): void;
  blendExpression(expression: ExpressionId, weight: number): void;
  
  // 角色切换
  setCharacter(characterId: string): void;
  
  // 资源管理
  preloadCharacter(characterId: string): Promise<void>;
  dispose(): void;
}
```

### Registries

```typescript
// 角色注册表
export interface ICharacterRegistry {
  getCharacter(id: string): CharacterConfig | undefined;
  getAllCharacters(): CharacterConfig[];
  getCharactersByAgeGroup(ageGroup: AgeGroup): CharacterConfig[];
  registerCharacter(config: CharacterConfig): void;
  validateConfig(config: CharacterConfig): ValidationResult;
}

// 表情注册表
export interface IExpressionRegistry {
  getExpression(id: ExpressionId): ExpressionConfig | undefined;
  getAllExpressions(): ExpressionConfig[];
  registerExpression(config: ExpressionConfig): void;
}

// 语言注册表
export interface ILanguageRegistry {
  getMapping(languageCode: string): LanguageMapping | undefined;
  getDefaultMapping(): LanguageMapping;
  registerMapping(mapping: LanguageMapping): void;
  getSupportedLanguages(): string[];
}
```

## Data Models

### Character Configuration File Format

```typescript
// characters/bunny.json
{
  "id": "bunny",
  "name": "Bunny",
  "description": "A friendly bunny character for young learners",
  "ageGroups": ["child"],
  "assets": {
    "baseImage": "bunny/base.png",
    "visemeImages": {
      "0": "bunny/viseme_silent.png",
      "1": "bunny/viseme_aa.png",
      // ... 其他视位
    },
    "expressionOverlays": {
      "happy": "bunny/expr_happy.png",
      "thinking": "bunny/expr_thinking.png",
      // ... 其他表情
    }
  },
  "defaultExpression": "neutral"
}
```

### Expression Configuration

```typescript
// expressions/happy.json
{
  "id": "happy",
  "name": "Happy",
  "eyeState": "squint",
  "browState": "raised",
  "transitionDuration": 200,
  "easing": "easeOut"
}
```

### Language Phoneme Mapping

```typescript
// languages/en.json
{
  "languageCode": "en",
  "phonemeToViseme": {
    "AA": 1,   // father
    "AE": 6,   // cat
    "AH": 7,   // but
    "AO": 4,   // dog
    "AW": 4,   // cow
    "AY": 1,   // my
    "B": 10,   // boy
    "CH": 14,  // chin
    "D": 11,   // dog
    "DH": 8,   // this
    "EH": 6,   // bed
    "ER": 12,  // bird
    "EY": 2,   // say
    "F": 9,    // five
    "G": 15,   // go
    "HH": 0,   // hat
    "IH": 3,   // sit
    "IY": 2,   // see
    "JH": 14,  // joy
    "K": 15,   // cat
    "L": 11,   // lion
    "M": 10,   // map
    "N": 11,   // no
    "NG": 15,  // sing
    "OW": 4,   // go
    "OY": 4,   // boy
    "P": 10,   // pen
    "R": 12,   // red
    "S": 13,   // sun
    "SH": 14,  // ship
    "T": 11,   // top
    "TH": 8,   // think
    "UH": 5,   // book
    "UW": 5,   // too
    "V": 9,    // very
    "W": 12,   // water
    "Y": 2,    // yes
    "Z": 13,   // zoo
    "ZH": 14   // measure
  }
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

Based on the prework analysis, the following properties have been identified after removing redundancies:

### Property 1: Lip Sync State Consistency
*For any* speaking session, when audio playback completes, the avatar SHALL return to idle state with SILENT viseme.
**Validates: Requirements 1.2, 1.3**

### Property 2: Viseme Timing Bounds
*For any* generated lip sync data, all viseme frame durations SHALL fall within reasonable bounds (50ms - 500ms per viseme).
**Validates: Requirements 1.4**

### Property 3: Character Viseme Completeness
*For any* registered character, the character SHALL have valid asset paths defined for all 16 viseme types.
**Validates: Requirements 2.2**

### Property 4: Animation Timing Consistency
*For any* two characters playing the same text, the total lip sync duration SHALL be equal (within 10ms tolerance).
**Validates: Requirements 2.4**

### Property 5: Text Input Produces Valid LipSync
*For any* non-empty text input, the system SHALL produce valid LipSyncData with at least one viseme frame.
**Validates: Requirements 3.1, 3.2**

### Property 6: TTS Fallback Produces Valid LipSync
*For any* text input when TTS is unavailable, the fallback timing-based lip sync SHALL produce valid LipSyncData.
**Validates: Requirements 5.2**

### Property 7: Phoneme to Viseme Mapping Completeness
*For any* phoneme in the supported phoneme set, the mapping SHALL produce a valid Viseme index (0-15).
**Validates: Requirements 5.4**

### Property 8: Expression Feedback Correctness
*For any* correct answer event, the triggered expression SHALL be from the set {happy, excited, celebrating}. *For any* incorrect answer event, the triggered expression SHALL be from the set {encouraging, thinking}.
**Validates: Requirements 4.2, 4.3**

### Property 9: Expression Blending Preserves LipSync
*For any* expression change during active lip sync, the lip sync animation SHALL continue without interruption.
**Validates: Requirements 8.3**

### Property 10: Character Validation Error Specificity
*For any* invalid character configuration, the validation SHALL return specific error messages identifying the invalid fields.
**Validates: Requirements 9.3**

### Property 11: Character Switch State Preservation
*For any* character switch during animation, the animation state (playing/paused, progress) SHALL be preserved.
**Validates: Requirements 9.4**

### Property 12: Language Fallback to English
*For any* unsupported language code, the phoneme-to-viseme mapping SHALL fall back to English mapping.
**Validates: Requirements 10.3**

### Property 13: Playback Callbacks Invocation
*For any* speak() call that completes successfully, onPlaybackStart SHALL be called before onPlaybackEnd, and both SHALL be called exactly once.
**Validates: Requirements 7.2**

### Property 14: Resource Cleanup on Unmount
*For any* component unmount, all active timers and audio resources SHALL be cleaned up (no memory leaks).
**Validates: Requirements 6.4**

## Error Handling

### Error Types

```typescript
export enum SpeakingAvatarErrorCode {
  AUDIO_LOAD_FAILED = 'AUDIO_LOAD_FAILED',
  TTS_UNAVAILABLE = 'TTS_UNAVAILABLE',
  CHARACTER_NOT_FOUND = 'CHARACTER_NOT_FOUND',
  INVALID_CHARACTER_CONFIG = 'INVALID_CHARACTER_CONFIG',
  ASSET_LOAD_FAILED = 'ASSET_LOAD_FAILED',
  LANGUAGE_NOT_SUPPORTED = 'LANGUAGE_NOT_SUPPORTED',
  PLAYBACK_INTERRUPTED = 'PLAYBACK_INTERRUPTED',
}

export interface SpeakingAvatarError {
  code: SpeakingAvatarErrorCode;
  message: string;
  details?: Record<string, unknown>;
}
```

### Error Handling Strategy

1. **TTS 不可用**: 自动回退到基于文本长度的时序估算
2. **角色未找到**: 使用默认角色并触发 onError 回调
3. **资源加载失败**: 显示占位符 UI 并触发 onError 回调
4. **语言不支持**: 回退到英语映射并记录警告
5. **播放中断**: 清理资源并触发 onPlaybackEnd 回调

### Fallback UI

当发生严重错误时，组件显示简化的静态头像，保持用户体验不中断。

## Testing Strategy

### Dual Testing Approach

本模块采用单元测试和属性测试相结合的方式：

- **单元测试**: 验证具体示例和边界情况
- **属性测试**: 验证跨所有输入的通用属性

### Property-Based Testing Framework

使用 **fast-check** 作为属性测试库，配置每个属性测试运行至少 100 次迭代。

### Test Categories

1. **LipSyncEngine Tests**
   - 音素到视位映射正确性
   - 时序估算合理性
   - 回退机制有效性

2. **CharacterRegistry Tests**
   - 配置验证完整性
   - 角色发现机制
   - 资源路径有效性

3. **ExpressionEngine Tests**
   - 表情混合正确性
   - 过渡动画平滑性
   - 反馈表情选择

4. **Integration Tests**
   - 完整播放流程
   - 回调触发顺序
   - 资源清理

### Test Annotation Format

所有属性测试必须使用以下格式标注：

```typescript
/**
 * **Feature: speaking-avatar, Property 1: Lip Sync State Consistency**
 * **Validates: Requirements 1.2, 1.3**
 */
it('should return to idle state after playback completes', () => {
  fc.assert(
    fc.property(fc.string({ minLength: 1 }), (text) => {
      // Test implementation
    }),
    { numRuns: 100 }
  );
});
```
