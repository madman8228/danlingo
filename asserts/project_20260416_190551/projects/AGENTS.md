## 项目概述
- **名称**: 智能词汇扩展工作流（分类识别版）
- **功能**: 智能分类识别输入内容类型，自动选择对应流程生成相应知识文档。支持单词、短语、搭配、句型、口语、习语的自动识别和处理

### 节点清单
| 节点名 | 文件位置 | 类型 | 功能描述 | 分支逻辑 | 配置文件 | 优化说明 |
|-------|---------|------|---------|---------|---------|---------|
| classify_input_content | `nodes/classify_input_content_node.py` | agent | 自动分类识别输入内容类型（单词/短语/搭配/句型/口语/习语） | 条件分支到对应流程 | - | 使用LLM智能分类 |
| generate_initial_knowledge | `nodes/generate_initial_knowledge_node.py` | agent | 为初始单词列表生成知识块，写入word_knowledge.md | - | - | - |
| append_synonyms_antonyms | `nodes/append_synonyms_antonyms_node.py` | task | 遍历synonyms和antonyms中的单词，追加到word_knowledge.md | - | - | 限制数量避免指数级增长，单层扩展 |
| process_phrases | `nodes/process_phrases_node.py` | agent | 遍历phrases，生成phrase_knowledge.md | - | - | 批量处理，3个一组 |
| process_collocations | `nodes/process_remaining_nodes.py` | agent | 遍历collocations，生成collocations_knowledge.md | - | - | 批量处理，5个一组 |
| process_sentence_patterns | `nodes/process_remaining_nodes.py` | agent | 遍历sentencePatterns，生成sentencePatterns_knowledge.md | - | - | 批量处理，5个一组 |
| process_spoken_expressions | `nodes/process_remaining_nodes.py` | agent | 遍历spokenExpressions，生成spokenExpressions_knowledge.md | - | - | 批量处理，5个一组 |
| process_idioms | `nodes/process_remaining_nodes.py` | agent | 遍历idioms，生成idioms_knowledge.md | - | - | 批量处理，5个一组 |
| generate_phrase_knowledge_direct | `nodes/generate_phrase_knowledge_direct_node.py` | agent | 直接为短语列表生成phrase_knowledge.md | - | - | 直接生成，无需单词流程 |
| generate_collocation_knowledge_direct | `nodes/generate_collocation_knowledge_direct_node.py` | agent | 直接为搭配列表生成collocations_knowledge.md | - | - | 直接生成，无需单词流程 |
| generate_sentence_pattern_knowledge_direct | `nodes/generate_sentence_pattern_knowledge_direct_node.py` | agent | 直接为句型列表生成sentencePatterns_knowledge.md | - | - | 直接生成，无需单词流程 |
| generate_spoken_expression_knowledge_direct | `nodes/generate_spoken_expression_knowledge_direct_node.py` | agent | 直接为口语列表生成spokenExpressions_knowledge.md | - | - | 直接生成，无需单词流程 |
| generate_idiom_knowledge_direct | `nodes/generate_idiom_knowledge_direct_node.py` | agent | 直接为习语列表生成idioms_knowledge.md | - | - | 直接生成，无需单词流程 |
| determine_next_step | `graph.py` | condition | 根据识别的内容类型判断下一步 | 条件分支 | - | - |

**类型说明**: task(task节点) / agent(大模型) / condition(条件分支) / looparray(列表循环) / loopcond(条件循环)

## 子图清单
无

## 技能使用
- 节点 `classify_input_content` 使用技能：大语言模型 (doubao-seed-2-0-pro-260215)
- 节点 `generate_initial_knowledge` 使用技能：大语言模型 (doubao-seed-2-0-pro-260215)
- 节点 `process_phrases` 使用技能：大语言模型 (doubao-seed-2-0-pro-260215)
- 节点 `process_collocations` 使用技能：大语言模型 (doubao-seed-2-0-pro-260215)
- 节点 `process_sentence_patterns` 使用技能：大语言模型 (doubao-seed-2-0-pro-260215)
- 节点 `process_spoken_expressions` 使用技能：大语言模型 (doubao-seed-2-0-pro-260215)
- 节点 `process_idioms` 使用技能：大语言模型 (doubao-seed-2-0-pro-260215)
- 节点 `generate_phrase_knowledge_direct` 使用技能：大语言模型 (doubao-seed-2-0-pro-260215)
- 节点 `generate_collocation_knowledge_direct` 使用技能：大语言模型 (doubao-seed-2-0-pro-260215)
- 节点 `generate_sentence_pattern_knowledge_direct` 使用技能：大语言模型 (doubao-seed-2-0-pro-260215)
- 节点 `generate_spoken_expression_knowledge_direct` 使用技能：大语言模型 (doubao-seed-2-0-pro-260215)
- 节点 `generate_idiom_knowledge_direct` 使用技能：大语言模型 (doubao-seed-2-0-pro-260215)

## 工作流说明

### 智能分类识别工作流流程：

#### 1. 分类识别阶段
- **输入**: 内容列表（如 ["take", "take care of", "Take it easy!"]）
- **第一步**: 自动分类识别输入内容类型
  - 使用LLM智能判断内容类型（单词/短语/搭配/句型/口语/习语）
  - 输出分类结果和置信度
  - 显示分类理由

#### 2. 条件分支执行
根据识别的内容类型，自动选择对应流程：

##### 分支1: 单词处理流程（原7步工作流）
当识别为 **word** 类型时执行：
1. **步骤1**: 为每个初始单词生成完整的词汇扩展知识，合并到 word_knowledge.md
2. **步骤2**: 遍历 word_knowledge.md 中所有单词的 synonyms 和 antonyms 中的所有单词，把它们追加到 word_knowledge.md（单层扩展）
3. **步骤3**: 遍历 word_knowledge 中的所有知识块的 phrases，依次写到 phrase_knowledge.md 中
4. **步骤4**: 遍历 word_knowledge 中的所有知识块的 collocations，每个 collocations 以 ## collocations 开头
5. **步骤5**: 遍历 word_knowledge 中的所有知识块的 sentencePatterns，每个 sentencePatterns 以 ## sentencePatterns 开头
6. **步骤6**: 遍历 word_knowledge 中的所有知识块的 spokenExpressions，每个 spokenExpressions 以 ## spokenExpressions 开头
7. **步骤7**: 遍历 word_knowledge 中的所有知识块的 idioms，每个 idioms 以 ## idioms 开头

##### 分支2: 直接生成短语知识
当识别为 **phrase** 类型时执行：
- 直接为输入的短语列表生成 phrase_knowledge.md
- 每个短语包含 collocations、sentencePatterns、spokenExpressions、idioms、example

##### 分支3: 直接生成搭配知识
当识别为 **collocation** 类型时执行：
- 直接为输入的搭配列表生成 collocations_knowledge.md
- 每个搭配包含至少2个 example

##### 分支4: 直接生成句型知识
当识别为 **sentence_pattern** 类型时执行：
- 直接为输入的句型列表生成 sentencePatterns_knowledge.md
- 每个句型包含至少2个 example

##### 分支5: 直接生成口语知识
当识别为 **spoken_expression** 类型时执行：
- 直接为输入的口语列表生成 spokenExpressions_knowledge.md
- 每个口语包含至少2个 example

##### 分支6: 直接生成习语知识
当识别为 **idiom** 类型时执行：
- 直接为输入的习语列表生成 idioms_knowledge.md
- 每个习语包含至少2个 example

#### 3. 输出
根据执行的分支，输出相应的知识文档：
- word_knowledge.md: 包含所有单词的完整知识（单词流程）
- phrase_knowledge.md: 包含所有短语的知识
- collocations_knowledge.md: 包含所有搭配的知识
- sentencePatterns_knowledge.md: 包含所有句型的知识
- spokenExpressions_knowledge.md: 包含所有口语表达的知识
- idioms_knowledge.md: 包含所有习语的知识

## 分类识别规则

### 内容类型定义
1. **word**（单词）：
   - 单个单词，没有空格
   - 例如："take", "run", "view"

2. **phrase**（短语/词组）：
   - 2-4个单词组成的固定表达
   - 例如："take care of", "look forward to", "give up"

3. **collocation**（搭配）：
   - 常用的词语搭配，通常是"动词+名词"或"形容词+名词"
   - 例如："take a break", "make a decision", "strong coffee"

4. **sentence_pattern**（句型）：
   - 包含语法结构的句式，通常有占位符或固定结构
   - 例如："It takes sb + time + to do sth", "The more..., the more..."

5. **spoken_expression**（口语）：
   - 日常口语表达，通常是感叹句、祈使句或常用口语
   - 例如："Take it easy!", "How's it going?", "Break a leg!"
   - 首字母通常大写，以感叹号结尾

6. **idiom**（习语）：
   - 固定的习语表达，整体意义不等于各部分之和
   - 例如："break a leg", "piece of cake", "hit the hay"

## 模型调用优化说明

### 优化前的问题
1. **步骤2指数级增长**: 每个单词的 synonyms 又会有自己的 synonyms，无限递归，导致调用次数爆炸
2. **步骤3-7单次调用**: 每个短语/搭配/句型等都单独调用一次LLM，效率低下

### 优化方案

#### 优化1：步骤2 - 避免指数级增长
- **优化前**: 为每个 synonyms 和 antonyms 的单词调用LLM生成完整知识
- **优化后**:
  - 每个单词最多取3个 synonyms，2个 antonyms
  - 总共最多添加10个新单词
  - 仅记录相关单词，暂不生成完整知识
- **效果**: 避免了指数级增长，LLM调用次数稳定

#### 优化2：步骤3-7 - 批量处理减少调用次数
- **优化前**: 每个项目单独调用一次LLM
- **优化后**:
  - 短语：3个一组批量处理
  - 搭配/句型/口语/习语：5个一组批量处理
  - 一次性LLM调用生成多个项目的知识
- **效果**: LLM调用次数大幅减少（例如10个短语只需4次调用，而非10次）

#### 优化3：智能分类识别
- **新增功能**: 自动识别输入内容类型
- **优化效果**: 根据内容类型选择最优处理流程，避免不必要的步骤

### 优化效果预估
- **初始单词数**: 3个
- **优化前LLM调用**: 约20-30次（包含步骤2的递归）
- **优化后LLM调用**: 约6-8次（步骤1-7，批量处理）
- **优化率**: 约70%的LLM调用次数减少

## 注意事项
- 本工作流支持智能分类识别，自动选择最优处理流程
- 已优化模型调用次数，但仍建议从小规模内容列表开始测试
- 所有节点都使用真实的LLM调用，无Mock数据
- 分类识别使用LLM进行智能判断，也支持规则作为兜底
