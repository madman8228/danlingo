import os
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.runtime_ctx.context import new_context
from langchain_core.messages import SystemMessage, HumanMessage
from graphs.state import GeneratePhraseKnowledgeDirectInput, GeneratePhraseKnowledgeDirectOutput


def get_text_content(content):
    """安全地提取文本内容"""
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        if content and isinstance(content[0], str):
            return " ".join(content)
        else:
            return " ".join(item.get("text", "") for item in content if isinstance(item, dict) and item.get("type") == "text")
    return str(content)


def generate_single_phrase_knowledge(phrase):
    """为单个短语生成完整的知识"""

    system_prompt = """你是一个专业的英语短语专家，擅长生成短语的完整扩展信息。

请为短语生成完整的知识，严格按照以下格式输出：

## phrases: <短语>
- collocations: <搭配1> || <中文> ;; <搭配2> || <中文> ;;
- sentencePatterns: <句型1> || <说明> ;; <句型2> || <说明> ;;
- spokenExpressions: <口语1> || <中文> ;; <口语2> || <中文> ;;
- idioms: <习语1> || <中文> ;; （如果有的话）
- example: <例句1> || <中文翻译>
- example: <例句2> || <中文翻译>

重要要求：
1. 每个字段必须使用 ` || ` 分隔英文和中文，使用 ` ;; ` 分隔多个条目
2. 必须包含搭配（3-5个）、句型（2-3个）、口语表达（2-3个）
3. 必须至少有2个例句
4. 习语如果没有相关用法可以省略
5. 输出必须严格按照上述格式，不要添加额外的说明文字"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"请为短语 '{phrase}' 生成完整的知识，严格按照指定格式输出。")
    ]

    ctx = new_context(method="invoke")
    client = LLMClient(ctx=ctx)

    try:
        response = client.invoke(
            messages=messages,
            model="doubao-seed-2-0-pro-260215",
            temperature=0.3,
            max_completion_tokens=2000
        )

        content = get_text_content(response.content)
        return content

    except Exception as e:
        print(f"生成短语 {phrase} 的知识时出错: {e}")
        return f"""## phrases: {phrase}
- collocations:
- sentencePatterns:
- spokenExpressions:
- idioms:
- example: This is an example for {phrase}. || 这是{phrase}的一个例句。"""


def generate_phrase_knowledge_direct_node(
    state: GeneratePhraseKnowledgeDirectInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> GeneratePhraseKnowledgeDirectOutput:
    """
    title: 直接生成短语知识
    desc: 直接为输入的短语列表生成完整的phrase_knowledge.md文档
    integrations: 大语言模型
    """
    ctx = runtime.context

    try:
        # 创建输出目录
        workspace = os.getenv("COZE_WORKSPACE_PATH", os.getcwd())
        assets_dir = os.path.join(workspace, "assets")
        os.makedirs(assets_dir, exist_ok=True)

        phrase_knowledge_path = os.path.join(assets_dir, "phrase_knowledge.md")

        print(f"开始为 {len(state.input_list)} 个短语生成知识...")

        # 为每个短语生成知识
        with open(phrase_knowledge_path, 'w', encoding='utf-8') as f:
            for i, phrase in enumerate(state.input_list, 1):
                print(f"正在生成第 {i}/{len(state.input_list)} 个短语: {phrase}")
                phrase_knowledge = generate_single_phrase_knowledge(phrase)
                f.write(phrase_knowledge)
                f.write('\n\n')

        print(f"✓ 成功生成 phrase_knowledge.md，包含 {len(state.input_list)} 个短语的知识")

        return GeneratePhraseKnowledgeDirectOutput(
            phrase_knowledge_path=phrase_knowledge_path,
            success=True
        )

    except Exception as e:
        error_msg = f"直接生成短语知识失败: {str(e)}"
        print(error_msg)
        return GeneratePhraseKnowledgeDirectOutput(
            phrase_knowledge_path="",
            success=False
        )
