---
inclusion: always
---

# DuoXX 项目开发规范

## 🚨 核心宪法（必须遵守）
- **禁止使用 Markdown 表格** - 回答问题时避免使用 `|` 分隔的表格格式，改用列表或缩进格式展示结构化数据，确保在任何环境下都能正常显示

- **必须保证 UI 风格统一** - 所有组件、页面、交互必须遵循统一的视觉语言
  - 颜色：使用 `constants/theme.ts` 中定义的 Colors
  - 字体：使用 Fonts 对象中的平台字体
  - 间距：保持一致的 padding/margin 规范
  - 圆角：统一的 borderRadius 值
  - 阴影：一致的 shadow 样式
  - 动画：统一的过渡时长和缓动函数

- **必须优先开发可复用代码** - 每次增加功能前必须评估复用性
  - 检查项目中是否有其他模块可能用到相同功能
  - 通用组件放入 `src/components/` 而非模块专属目录
  - 通用工具函数放入 `src/utils/` 或 `src/hooks/`
  - 通用类型定义放入 `src/models/` 或 `src/types/`
  - 如果功能可能被2个以上模块使用，必须抽象为公共模块
  - 示例：对话气泡组件、计时器组件、选择题组件等应放入公共组件库

## 图标使用规范
- **禁止使用文字符号作为图标**（如 emoji 📄、文字"文"等）
- 使用 @expo/vector-icons 提供的图标库（如 Ionicons, MaterialIcons, FontAwesome 等）
- 图标应保持风格统一，优先使用同一图标库

## UI/UX 规范
- 弹出菜单应出现在触发元素附近，而非屏幕中央
- 保持界面简洁，避免过大的弹窗
- 遵循平台原生设计规范（iOS/Android）

## 代码规范
- 组件使用 TypeScript
- 样式使用 StyleSheet.create
- 状态管理优先使用 React hooks

## 🏗️ 功能模块化开发规范（必须遵守）

### 模块系统架构
- 所有功能模块必须通过 `src/modules/registry.ts` 注册
- 模块定义必须遵循 `FeatureModule` 接口（见 `src/modules/types.ts`）
- 模块路由统一使用 `/modules/[moduleId]` 动态路由

### 模块开发流程
1. 在 `src/modules/registry.ts` 中注册模块元信息
2. 在 `src/modules/[模块名]/` 目录下创建模块代码
3. 模块必须导出标准接口，支持动态加载

### 模块结构规范
```
src/modules/
├── types.ts              # 模块类型定义
├── registry.ts           # 模块注册表
├── index.ts              # 统一导出
└── [module-name]/        # 具体模块目录
    ├── index.ts          # 模块入口
    ├── types.ts          # 模块内部类型
    ├── components/       # 模块专属组件
    ├── services/         # 模块业务逻辑
    └── data/             # 模块数据
```

### 模块注册要求
- `id`: 唯一标识，kebab-case 格式
- `name`: 显示名称
- `description`: 功能描述
- `icon`: Ionicons 图标名（禁止 emoji）
- `color`: 主题色
- `route`: 路由路径
- `status`: 模块状态（active/coming_soon/locked/disabled）
- `targetGroups`: 适用用户群体

### 用户群体区分
- 儿童（child）：趣味互动，游戏化元素多
- 学生（student）：应试导向，系统化学习
- 成人（adult）：实用场景，高效沟通
- 不同群体显示不同的功能模块和 UI 元素

## 📊 评分系统规范（必须遵守）

### 核心架构
评分系统采用三层设计，确保科学性与用户友好性：

1. **内部层（IRT θ 值）**：-3 到 +3 的能力值，用于算法计算
2. **展示层（0-100 分）**：用户友好的分数，线性映射自 θ 值
3. **标准层（CEFR 等级）**：A1-C2 国际标准等级，便于对外沟通

### 类型定义位置
- 核心类型：`src/models/scoring.ts`
- 服务函数：`src/services/scoringService.ts`
- 各模块复用上述公共定义，禁止重复定义 CEFR 等级

### CEFR 等级映射
| θ 值范围 | 展示分数 | CEFR | 描述 |
|---------|---------|------|------|
| -3.0 ~ -2.0 | 0-16 | A1 | 入门级 |
| -2.0 ~ -1.0 | 17-33 | A2 | 基础级 |
| -1.0 ~ 0.0 | 34-50 | B1 | 中级 |
| 0.0 ~ 1.0 | 51-67 | B2 | 中高级 |
| 1.0 ~ 2.0 | 68-84 | C1 | 高级 |
| 2.0 ~ 3.0 | 85-100 | C2 | 精通级 |

### 多维度能力评估
- 支持维度：词汇、听力、口语、阅读、写作、语法
- 各维度独立评估，加权计算综合能力
- 维度配置在 `DEFAULT_DIMENSION_CONFIGS` 中定义

### 使用规范
```typescript
// ✅ 正确：使用公共评分服务
import { thetaToDisplayScore, thetaToCEFR } from '@/services/scoringService';
import { CEFRLevel, AbilityDimension } from '@/models/scoring';

// ❌ 错误：在模块内重复定义
enum MyLevel { A1, A2, B1 } // 禁止！
```

### 能力更新流程
1. 收集答题结果 `AnswerResult[]`
2. 调用 `updateUserAbility()` 更新能力值
3. 系统自动计算新的 θ 值、展示分数、CEFR 等级
4. 可选：更新综合能力（跨维度加权）

### 扩展指南
- 新增能力维度：在 `AbilityDimension` 枚举和 `DEFAULT_DIMENSION_CONFIGS` 中添加
- 调整映射关系：修改 `THETA_TO_CEFR_THRESHOLDS` 和 `SCORE_TO_CEFR_THRESHOLDS`
- 自定义评分策略：实现新的转换函数，保持接口一致

## 📝 错题收集系统规范（必须遵守）

### 核心架构
统一的错题收集服务，收集所有模块的错题数据用于知识弱点分析和智能推荐。

### 相关文件
- 错题收集服务：`src/services/errorCollectionService.ts`
- 错题记录模型：`src/models/user.ts` 中的 `ErrorRecord`
- 推荐引擎：`src/services/recommendationEngine.ts`

### 使用规范
各模块在答题错误时必须调用 `errorCollectionService.recordError()` 上报错题：

```typescript
import { errorCollectionService, GenericExerciseResult } from '@/src/services/errorCollectionService';

// 答题错误时上报
if (!isCorrect) {
  const genericResult: GenericExerciseResult = {
    exerciseId: '练习ID',
    moduleId: 'sentence-building', // 模块标识
    exerciseType: '练习类型',
    isCorrect: false,
    userAnswer: '用户答案',
    correctAnswer: '正确答案',
    tags: ['知识点标签'],
    timestamp: new Date().toISOString(),
  };
  errorCollectionService.recordError(genericResult);
}
```

### 已接入模块
- sentence-building（句型构建）
- listening-speaking（听说训练）
- vocab-recognition（词汇认知）
- survival-phrases（救命锦囊）

### 数据流向
1. 各模块答题 → 错题上报到 `errorCollectionService`
2. 错题存储到 `UserProgress.errorHistory`
3. `RecommendationEngine.analyzeWeakAreas()` 分析知识弱点
4. 根据弱点推荐针对性练习
