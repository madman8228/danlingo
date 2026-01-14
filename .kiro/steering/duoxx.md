---
inclusion: always
---

# DuoXX 项目开发规范

## 🚨 核心宪法（必须遵守）
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
