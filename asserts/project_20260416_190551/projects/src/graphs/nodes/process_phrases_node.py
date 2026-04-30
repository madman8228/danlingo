import os
import re
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.runtime_ctx.context import new_context
from langchain_core.messages import SystemMessage, HumanMessage
from graphs.state import ProcessPhrasesInput, ProcessPhrasesOutput
from graphs.nodes.generate_initial_knowledge_node import get_text_content
from graphs.nodes.process_remaining_nodes import extract_word_blocks, extract_items_from_field


def generate_batch_phrases_knowledge(phrases_list):
    """批量生成多个短语的知识（一次性LLM调用）"""
    phrases_str = "\n".join([f"{i+1}. {phrase}" for i, phrase in enumerate(phrases_list)])

    system_prompt = f"""你是一个专业的英语词汇专家，擅长为短语生成完整的知识。

请为以下短语列表生成完整的知识，严格按照以下格式输出：

## phrases: <短语1>
- collocations: <搭配1> || <中文> ;; <搭配2> || <中文> ;;
- sentencePatterns: <句型1> || <说明> ;; <句型2> || <说明> ;;
- spokenExpressions: <口语1> || <中文> ;; <口语2> || <中文> ;;
- idioms: <习语1> || <中文> ;; <习语2> || <中文> ;;
- example: <例句1> || <中文翻译>
- example: <例句2> || <中文翻译>

## phrases: <短语2>
- collocations: <搭配1> || <中文> ;; <搭配2> || <中文> ;;
- sentencePatterns: <句型1> || <说明> ;; <句型2> || <说明> ;;
- spokenExpressions: <口语1> || <中文> ;; <口语2> || <中文> ;;
- idioms: <习语1> || <中文> ;; <习语2> || <中文> ;;
- example: <例句1> || <中文翻译>
- example: <例句2> || <中文翻译>

重要要求：
1. 每个短语生成独立的块，以## phrases: 开头
2. 必须包含collocations、sentencePatterns、spokenExpressions、idioms（如果没有可以空着但要列出）
3. 必须包含至少2个 example
4. 每个字段使用 ` || ` 分隔英文和中文，使用 ` ;; ` 分隔多个条目
5. 按照顺序处理所有短语
6. 输出必须严格按照上述格式，不要添加额外的说明文字

短语列表：
{phrases_str}"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"请为以上短语列表生成完整的知识，严格按照指定格式输出。")
    ]

    ctx = new_context(method="invoke")
    client = LLMClient(ctx=ctx)

    try:
        response = client.invoke(
            messages=messages,
            model="doubao-seed-2-0-pro-260215",
            temperature=0.3,
            max_completion_tokens=3500
        )

        content = get_text_content(response.content)
        return content

    except Exception as e:
        print(f"批量生成短语知识时出错: {e}")
        # 生成简单的备用内容
        fallback_content = []
        for phrase in phrases_list:
            fallback_content.append(f"""## phrases: {phrase}
- collocations:
- sentencePatterns:
- spokenExpressions:
- idioms:
- example: This is an example with "{phrase}". || 这是一个包含"{phrase}"的例子。
- example: Another example using "{phrase}". || 另一个使用"{phrase}"的例子。""")
        return "\n\n".join(fallback_content)


def process_phrases_node(
    state: ProcessPhrasesInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> ProcessPhrasesOutput:
    """
    title: 处理短语（优化版）
    desc: 遍历word_knowledge中的所有知识块的phrases，批量处理减少LLM调用次数
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
        phrase_knowledge_path = os.path.join(assets_dir, "phrase_knowledge.md")

        word_blocks = extract_word_blocks(content)
        all_phrases = set()
        for block in word_blocks:
            phrases = extract_items_from_field(block, 'phrases')
            for phrase in phrases:
                all_phrases.add(phrase)

        phrases_list = sorted(list(all_phrases))
        print(f"发现 {len(phrases_list)} 个短语需要处理")

        if phrases_list:
            # 批量处理：最多3个一组，减少LLM调用次数（短语生成内容较多）
            batch_size = min(3, len(phrases_list))
            for i in range(0, len(phrases_list), batch_size):
                batch = phrases_list[i:i+batch_size]
                print(f"正在批量生成第 {i+1}-{min(i+batch_size, len(phrases_list))} 个短语")
                batch_content = generate_batch_phrases_knowledge(batch)

                mode = 'a' if i > 0 else 'w'
                with open(phrase_knowledge_path, mode, encoding='utf-8') as f:
                    if i > 0:
                        f.write('\n\n')
                    f.write(batch_content)

        return ProcessPhrasesOutput(
            phrase_knowledge_path=phrase_knowledge_path,
            success=True
        )

    except Exception as e:
        print(f"处理短语失败: {e}")
        return ProcessPhrasesOutput(
            phrase_knowledge_path="",
            success=False
        )
