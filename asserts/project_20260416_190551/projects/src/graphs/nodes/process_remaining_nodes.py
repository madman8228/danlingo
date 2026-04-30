import os
import re
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.runtime_ctx.context import new_context
from langchain_core.messages import SystemMessage, HumanMessage
from graphs.state import (
    ProcessCollocationsInput, ProcessCollocationsOutput,
    ProcessSentencePatternsInput, ProcessSentencePatternsOutput,
    ProcessSpokenExpressionsInput, ProcessSpokenExpressionsOutput,
    ProcessIdiomsInput, ProcessIdiomsOutput
)
from graphs.nodes.generate_initial_knowledge_node import get_text_content


def extract_word_blocks(content):
    """从内容中提取所有的 word 块"""
    pattern = r'## word:.*?(?=## word:|\Z)'
    blocks = re.findall(pattern, content, re.DOTALL)
    return [block.strip() for block in blocks if block.strip()]


def extract_items_from_field(word_block, field_name):
    """从 word 块中提取指定字段的内容"""
    items = []
    field_match = re.search(rf'-\s*{re.escape(field_name)}\s*:\s*(.+?)\n(?=-\s|\Z)', word_block, re.DOTALL)
    if field_match:
        field_text = field_match.group(1).strip()
        for item in field_text.split(';;'):
            item = item.strip()
            if '||' in item:
                en_part = item.split('||')[0].strip()
                if en_part:
                    items.append(en_part)
    return items


def generate_batch_knowledge(field_type, items_list):
    """批量生成多个项目的知识（一次性LLM调用）"""
    items_str = "\n".join([f"{i+1}. {item}" for i, item in enumerate(items_list)])

    system_prompt = f"""你是一个专业的英语词汇专家，擅长为{field_type}生成完整的知识。

请为以下{field_type}列表生成完整的知识，严格按照以下格式输出：

## {field_type}: <项目1>
- example: <例句1> || <中文翻译>
- example: <例句2> || <中文翻译>

## {field_type}: <项目2>
- example: <例句1> || <中文翻译>
- example: <例句2> || <中文翻译>

重要要求：
1. 每个{field_type}生成独立的块，以## {field_type}: 开头
2. 每个{field_type}必须包含至少2个 example
3. 每个 example 使用 ` || ` 分隔英文和中文
4. 按照顺序处理所有{field_type}
5. 输出必须严格按照上述格式，不要添加额外的说明文字

{field_type}列表：
{items_str}"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"请为以上{field_type}列表生成完整的知识，严格按照指定格式输出。")
    ]

    ctx = new_context(method="invoke")
    client = LLMClient(ctx=ctx)

    try:
        response = client.invoke(
            messages=messages,
            model="doubao-seed-2-0-pro-260215",
            temperature=0.3,
            max_completion_tokens=3000
        )

        content = get_text_content(response.content)
        return content

    except Exception as e:
        print(f"批量生成{field_type}知识时出错: {e}")
        # 生成简单的备用内容
        fallback_content = []
        for item in items_list:
            fallback_content.append(f"""## {field_type}: {item}
- example: This is an example with "{item}". || 这是一个包含"{item}"的例子。
- example: Another example using "{item}". || 另一个使用"{item}"的例子。""")
        return "\n\n".join(fallback_content)


def process_collocations_node(
    state: ProcessCollocationsInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> ProcessCollocationsOutput:
    """
    title: 处理搭配（优化版）
    desc: 遍历word_knowledge中的所有知识块的collocations，批量处理减少LLM调用次数
    integrations: 大语言模型
    """
    ctx = runtime.context

    try:
        if not os.path.exists(state.word_knowledge_path):
            raise FileNotFoundError(f"文件不存在: {state.word_knowledge_path}")

        with open(state.word_knowledge_path, 'r', encoding='utf-8') as f:
            content = f.read()

        workspace = os.getenv("COZE_WORKSPACE_PATH", os.getcwd())
        assets_dir = os.path.join(workspace, "assets")
        collocations_knowledge_path = os.path.join(assets_dir, "collocations_knowledge.md")

        word_blocks = extract_word_blocks(content)
        all_collocations = set()
        for block in word_blocks:
            collocations = extract_items_from_field(block, 'collocations')
            for collocation in collocations:
                all_collocations.add(collocation)

        collocations_list = sorted(list(all_collocations))
        print(f"发现 {len(collocations_list)} 个搭配需要处理")

        if collocations_list:
            # 批量处理：最多5个一组，减少LLM调用次数
            batch_size = min(5, len(collocations_list))
            for i in range(0, len(collocations_list), batch_size):
                batch = collocations_list[i:i+batch_size]
                print(f"正在批量生成第 {i+1}-{min(i+batch_size, len(collocations_list))} 个搭配")
                batch_content = generate_batch_knowledge('collocations', batch)

                mode = 'a' if i > 0 else 'w'
                with open(collocations_knowledge_path, mode, encoding='utf-8') as f:
                    if i > 0:
                        f.write('\n\n')
                    f.write(batch_content)

        return ProcessCollocationsOutput(
            collocations_knowledge_path=collocations_knowledge_path,
            success=True
        )

    except Exception as e:
        print(f"处理搭配失败: {e}")
        return ProcessCollocationsOutput(
            collocations_knowledge_path="",
            success=False
        )


def process_sentence_patterns_node(
    state: ProcessSentencePatternsInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> ProcessSentencePatternsOutput:
    """
    title: 处理句型（优化版）
    desc: 遍历word_knowledge中的所有知识块的sentencePatterns，批量处理减少LLM调用次数
    integrations: 大语言模型
    """
    ctx = runtime.context

    try:
        if not os.path.exists(state.word_knowledge_path):
            raise FileNotFoundError(f"文件不存在: {state.word_knowledge_path}")

        with open(state.word_knowledge_path, 'r', encoding='utf-8') as f:
            content = f.read()

        workspace = os.getenv("COZE_WORKSPACE_PATH", os.getcwd())
        assets_dir = os.path.join(workspace, "assets")
        sentencePatterns_knowledge_path = os.path.join(assets_dir, "sentencePatterns_knowledge.md")

        word_blocks = extract_word_blocks(content)
        all_sentence_patterns = set()
        for block in word_blocks:
            sentence_patterns = extract_items_from_field(block, 'sentencePatterns')
            for pattern in sentence_patterns:
                all_sentence_patterns.add(pattern)

        patterns_list = sorted(list(all_sentence_patterns))
        print(f"发现 {len(patterns_list)} 个句型需要处理")

        if patterns_list:
            # 批量处理
            batch_size = min(5, len(patterns_list))
            for i in range(0, len(patterns_list), batch_size):
                batch = patterns_list[i:i+batch_size]
                print(f"正在批量生成第 {i+1}-{min(i+batch_size, len(patterns_list))} 个句型")
                batch_content = generate_batch_knowledge('sentencePatterns', batch)

                mode = 'a' if i > 0 else 'w'
                with open(sentencePatterns_knowledge_path, mode, encoding='utf-8') as f:
                    if i > 0:
                        f.write('\n\n')
                    f.write(batch_content)

        return ProcessSentencePatternsOutput(
            sentencePatterns_knowledge_path=sentencePatterns_knowledge_path,
            success=True
        )

    except Exception as e:
        print(f"处理句型失败: {e}")
        return ProcessSentencePatternsOutput(
            sentencePatterns_knowledge_path="",
            success=False
        )


def process_spoken_expressions_node(
    state: ProcessSpokenExpressionsInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> ProcessSpokenExpressionsOutput:
    """
    title: 处理口语表达（优化版）
    desc: 遍历word_knowledge中的所有知识块的spokenExpressions，批量处理减少LLM调用次数
    integrations: 大语言模型
    """
    ctx = runtime.context

    try:
        if not os.path.exists(state.word_knowledge_path):
            raise FileNotFoundError(f"文件不存在: {state.word_knowledge_path}")

        with open(state.word_knowledge_path, 'r', encoding='utf-8') as f:
            content = f.read()

        workspace = os.getenv("COZE_WORKSPACE_PATH", os.getcwd())
        assets_dir = os.path.join(workspace, "assets")
        spokenExpressions_knowledge_path = os.path.join(assets_dir, "spokenExpressions_knowledge.md")

        word_blocks = extract_word_blocks(content)
        all_spoken_expressions = set()
        for block in word_blocks:
            expressions = extract_items_from_field(block, 'spokenExpressions')
            for expression in expressions:
                all_spoken_expressions.add(expression)

        expressions_list = sorted(list(all_spoken_expressions))
        print(f"发现 {len(expressions_list)} 个口语表达需要处理")

        if expressions_list:
            # 批量处理
            batch_size = min(5, len(expressions_list))
            for i in range(0, len(expressions_list), batch_size):
                batch = expressions_list[i:i+batch_size]
                print(f"正在批量生成第 {i+1}-{min(i+batch_size, len(expressions_list))} 个口语表达")
                batch_content = generate_batch_knowledge('spokenExpressions', batch)

                mode = 'a' if i > 0 else 'w'
                with open(spokenExpressions_knowledge_path, mode, encoding='utf-8') as f:
                    if i > 0:
                        f.write('\n\n')
                    f.write(batch_content)

        return ProcessSpokenExpressionsOutput(
            spokenExpressions_knowledge_path=spokenExpressions_knowledge_path,
            success=True
        )

    except Exception as e:
        print(f"处理口语表达失败: {e}")
        return ProcessSpokenExpressionsOutput(
            spokenExpressions_knowledge_path="",
            success=False
        )


def process_idioms_node(
    state: ProcessIdiomsInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> ProcessIdiomsOutput:
    """
    title: 处理习语（优化版）
    desc: 遍历word_knowledge中的所有知识块的idioms，批量处理减少LLM调用次数
    integrations: 大语言模型
    """
    ctx = runtime.context

    try:
        if not os.path.exists(state.word_knowledge_path):
            raise FileNotFoundError(f"文件不存在: {state.word_knowledge_path}")

        with open(state.word_knowledge_path, 'r', encoding='utf-8') as f:
            content = f.read()

        workspace = os.getenv("COZE_WORKSPACE_PATH", os.getcwd())
        assets_dir = os.path.join(workspace, "assets")
        idioms_knowledge_path = os.path.join(assets_dir, "idioms_knowledge.md")

        word_blocks = extract_word_blocks(content)
        all_idioms = set()
        for block in word_blocks:
            idioms = extract_items_from_field(block, 'idioms')
            for idiom in idioms:
                all_idioms.add(idiom)

        idioms_list = sorted(list(all_idioms))
        print(f"发现 {len(idioms_list)} 个习语需要处理")

        if idioms_list:
            # 批量处理
            batch_size = min(5, len(idioms_list))
            for i in range(0, len(idioms_list), batch_size):
                batch = idioms_list[i:i+batch_size]
                print(f"正在批量生成第 {i+1}-{min(i+batch_size, len(idioms_list))} 个习语")
                batch_content = generate_batch_knowledge('idioms', batch)

                mode = 'a' if i > 0 else 'w'
                with open(idioms_knowledge_path, mode, encoding='utf-8') as f:
                    if i > 0:
                        f.write('\n\n')
                    f.write(batch_content)

        return ProcessIdiomsOutput(
            idioms_knowledge_path=idioms_knowledge_path,
            success=True
        )

    except Exception as e:
        print(f"处理习语失败: {e}")
        return ProcessIdiomsOutput(
            idioms_knowledge_path="",
            success=False
        )
