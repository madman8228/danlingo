# DuoXX 项目总结文档

> 📅 创建日期: 2026-01-27  
> 📝 用途: 快速了解项目结构，避免遗忘

---

## 🎯 项目概述

**DuoXX** 是一款面向全年龄段用户的**游戏化英语学习移动应用**，通过 AI 驱动的个性化学习路径、动态数字卡通形象（Speaking Avatar）和沉浸式场景课程，为用户提供高效、有趣的英语学习体验。

### 核心价值
| 特性 | 描述 |
|------|------|
| 🧪 科学评估 | 基于 IRT（项目反应理论）的自适应能力评估 |
| 🎯 个性化学习 | AI 智能推荐，针对性强化薄弱环节 |
| 🎮 游戏化激励 | 完整的成就系统、徽章收集、连续打卡机制 |
| 🤖 情感连接 | Speaking Avatar 实时反馈，建立情感纽带 |
| 📍 场景化教学 | 真实生活场景对话，学以致用 |

---

## 🏗️ 技术栈

| 类别 | 技术 | 版本 |
|------|------|------|
| **框架** | Expo SDK | 54.0.31 |
| **运行时** | React Native | 0.81.5 |
| **语言** | TypeScript | 5.9 (严格模式) |
| **路由** | Expo Router | 6.0 (文件系统路由) |
| **状态管理** | Service Classes + React Hooks | - |
| **数据持久化** | AsyncStorage | 2.2.0 |
| **动画** | React Native Reanimated | 4.1.1 |
| **测试** | Jest + fast-check | 30.2 / 4.5 |
| **通知** | Expo Notifications | 0.32 |
| **音视频** | Expo AV | 16.0 |

---

## 📂 项目结构

```
expo_duo/
├── duoxx/                    # 主应用目录
│   ├── app/                  # 页面路由（Expo Router）
│   │   ├── (tabs)/           # 主导航标签页
│   │   ├── modules/          # 动态模块路由 `/modules/[moduleId]`
│   │   ├── lesson/           # 场景对话课程
│   │   ├── lesson-exercise/  # 练习课程
│   │   ├── achievements.tsx  # 成就页面
│   │   ├── progress-dashboard.tsx # 进度仪表盘
│   │   ├── goal-settings.tsx # 目标设置
│   │   └── error-book.tsx    # 错题本
│   ├── src/                  # 源代码
│   │   ├── components/       # UI 组件 (40个)
│   │   ├── models/           # TypeScript 类型定义 (10个)
│   │   ├── services/         # 业务逻辑服务 (36个)
│   │   ├── modules/          # 功能模块 (9个)
│   │   ├── validators/       # 答案验证器 (8个)
│   │   ├── storage/          # 数据持久化 (4个)
│   │   ├── data/             # 静态数据
│   │   └── irt/              # IRT 能力评估引擎
│   ├── components/           # 通用组件
│   ├── constants/            # 常量和主题
│   ├── hooks/                # 自定义 React Hooks
│   └── assets/               # 静态资源
├── duo_server/               # 后端服务 (空目录，待开发)
├── AGENTS.md                 # AI 代理编码指南
└── git-commit.js             # Git 提交工具
```

---

## 🧩 功能模块一览

### 已完成模块 ✅

| 模块 | 目录 | 描述 | 适用人群 |
|------|------|------|----------|
| **词汇认知** | `vocab-recognition/` | 图文匹配，建立"词-义-形"关联 | 全年龄 |
| **句型构建** | `sentence-building/` | 拖拽式单词排序，掌握句型结构 | 全年龄 |
| **听说训练** | `listening-speaking/` | 影子跟读、听音选择、听写练习 | 成人 |
| **救命锦囊** | `survival-phrases/` | 紧急场景必备表达（机场、医院等） | 成人 |
| **不完美对话** | `imperfect-dialogue/` | 多轮对话，容错评分机制 | 成人 |
| **Speaking Avatar** | `speaking-avatar/` | 口型同步动画角色系统 | 全年龄 |
| **用户档案** | `user-profile/` | 用户信息管理 | 全年龄 |

### 开发中模块 🔄

| 模块 | 目录 | 描述 |
|------|------|------|
| **刷题学英语** | `swipe-learning/` | TikTok式滑动学习，沉浸式刷题 |
| **动态词法引擎** | `dynamic-lexicon/` | 动态词汇量评估、语块教学 |

---

## 🏆 系统级功能

### 成就与激励系统
- **XP 经验值**: 答题获得 XP，等级提升，微成就奖励
- **徽章系统**: 5大类别，4种稀有度，进度追踪
- **里程碑系统**: XP/打卡/练习次数里程碑
- **连续打卡**: 90天学习日历热力图
- **学习目标**: 自定义每日/每周目标

### IRT 能力评估引擎
- **六维度评估**: 词汇、听力、口语、阅读、写作、语法
- **三层评分体系**:
  - 内部层: θ 值 (-3 到 +3)
  - 展示层: 用户分数 (0-100)
  - 标准层: CEFR 等级 (A1-C2)

### 错题收集系统
- 跨模块统一错题收集
- 知识点标签化分类
- 弱点分析和智能推荐

---

## 🖥️ 常用命令

```bash
# 开发
npm start                    # 启动 Expo 开发服务器
npm run android              # 在 Android 上运行
npm run ios                  # 在 iOS 上运行
npm run web                  # 在浏览器中运行

# 代码质量
npm run lint                 # ESLint 检查
npm run test                 # 运行所有测试
npm run test:watch           # 测试监听模式
npm run test:coverage        # 测试覆盖率

# 运行特定测试
npm test -- src/models/types.test.ts
npm test -- --testNamePattern="Enum"
```

---

## 👥 用户群体配置

| 群体 | 年龄 | 特点 | 可用模块 |
|------|------|------|----------|
| 🧒 儿童 | 6-12岁 | 趣味互动，快乐启蒙 | 词汇认知、句型构建 |
| 📚 学生 | 13-18岁 | 应试提分，能力提升 | 词汇认知、句型构建 |
| 👔 成人 | 18岁+ | 实用场景，高效沟通 | **全部模块** |

---

## 📋 核心服务文件

### 成就系统
| 文件 | 功能 |
|------|------|
| `achievementEngine.ts` | 核心成就引擎 |
| `streakManager.ts` | 打卡管理 |
| `badgeManager.ts` | 徽章管理 |
| `milestoneDetector.ts` | 里程碑检测 |
| `progressTracker.ts` | 进度追踪 |
| `goalTracker.ts` | 目标追踪 |
| `quickStartRecommendationEngine.ts` | 智能推荐 |

### Speaking Avatar
| 文件 | 功能 |
|------|------|
| `PhonemeService.ts` | 音素服务 |
| `LipSyncEngine.ts` | 口型同步引擎 |
| `ExpressionEngine.ts` | 表情引擎 |
| `AnimationEngine.ts` | 动画引擎 |
| `TTSService.ts` | 语音合成服务 |

### 评估系统
| 文件 | 功能 |
|------|------|
| `src/models/scoring.ts` | 评分数据模型 |
| `src/services/scoringService.ts` | 评分服务 |
| `src/irt/` | IRT 能力评估引擎 |

---

## 📚 相关文档

| 文档 | 路径 | 描述 |
|------|------|------|
| PRD | `duoxx/PRD.md` | 完整产品需求文档 |
| AGENTS.md | `AGENTS.md` | AI 代理编码指南 |
| README | `duoxx/README.md` | 项目快速入门 |
| IRT 引擎 | `src/irt/README.md` | IRT 评估引擎文档 |
| Speaking Avatar | `src/modules/speaking-avatar/README.md` | Avatar 模块文档 |
| Swipe Learning | `src/modules/swipe-learning/README.md` | 刷题模块文档 |

---

## 🚀 开发路线图概览

| 阶段 | 状态 | 主要内容 |
|------|------|----------|
| Phase 1 | ✅ 完成 | 核心功能（词汇、句型、成就基础、Avatar基础） |
| Phase 2 | ✅ 完成 | 高级功能（听说训练、救命锦囊、不完美对话） |
| Phase 3 | ✅ 完成 | 系统集成（错题收集、智能推荐、Quick Start） |
| Phase 4 | 🔄 进行中 | 优化扩展（刷题学英语、核心词法、动态词法） |
| Phase 5 | 📋 计划中 | 未来规划（实时场景模拟、多人对战、AI私教） |

---

## ⚡ 性能要求

| 指标 | 要求 |
|------|------|
| Quick Start 响应 | < 2 秒 |
| Avatar 反应 | < 500ms |
| Achievement Toast | < 500ms |
| 学习日历渲染 | < 1 秒 |

---

> 💡 **快速提示**: 如需了解更多细节，请查阅 `duoxx/PRD.md` 获取完整的产品需求文档。
