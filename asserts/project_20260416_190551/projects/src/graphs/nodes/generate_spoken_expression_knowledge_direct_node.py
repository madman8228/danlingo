import os
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.runtime_ctx.context import new_context
from langchain_core.messages import SystemMessage, HumanMessage
from graphs.state import GenerateSpokenExpressionKnowledgeDirectInput, GenerateSpokenExpressionKnowledgeDirectOutput


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


def generate_single_spoken_expression_knowledge(spoken_expression):
    """为单个口语生成完整的知识"""

    system_prompt = """你是一个专业的英语口语专家，擅长生成口语的完整扩展信息。

请为口语生成完整的知识，严格按照以下格式输出：

## spokenExpressions: <口语>
- example: <例句1> || <中文翻译>
- example: <例句2> || <中文翻译>

重要要求：
1. 必须至少有2个例句
2. 输出必须严格按照上述格式，不要添加额外的说明文字"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"请为口语 '{spoken_expression}' 生成完整的知识，严格按照指定格式输出。")
    ]

    ctx = new_context(method="invoke")
    client = LLMClient(ctx=ctx)

    try:
        response = client.invoke(
            messages=messages,
            model="doubao-seed-2-0-pro-260215",
            temperature=0.3,
            max_completion_tokens=1000
        )

        content = get_text_content(response.content)
        return content

    except Exception as e:
        print(f"生成口语 {spoken_expression} 的知识时出错: {e}")
        return f"""## spokenExpressions: {spoken_expression}
- example: This is an example for {spoken_expression}. || 这是{spoken_expression}的一个例句。"""


def generate_spoken_expression_knowledge_direct_node(
    state: GenerateSpokenExpressionKnowledgeDirectInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> GenerateSpokenExpressionKnowledgeDirectOutput:
    """
    title: 直接生成口语知识
    desc: 直接为输入的口语列表生成完整的spokenExpressions_knowledge.md文档
    integrations: 大语言模型
    """
    ctx = runtime.context

    try:
        # 创建输出目录
        workspace = os.getenv("COZE_WORKSPACE_PATH", os.getcwd())
        assets_dir = os.path.join(workspace, "assets")
        os.makedirs(assets_dir, exist_ok=True)

        spokenExpressions_knowledge_path = os.path.join(assets_dir, "spokenExpressions_knowledge.md")

        print(f"开始为 {len(state.input_list)} 个口语生成知识...")

        # 为每个口语生成知识
        with open(spokenExpressions_knowledge_path, 'w', encoding='utf-8') as f:
            for i, spoken_expression in enumerate(state.input_list, 1):
                print(f"正在生成第 {i}/{len(state.input_list)} 个口语: {spoken_expression}")
                expression_knowledge = generate_single_spoken_expression_knowledge(spoken_expression)
                f.write(expression_knowledge)
                f.write('\n\n')

        print(f"✓ 成功生成 spokenExpressions_knowledge.md，包含 {len(state.input_list)} 个口语的知识")

        return GenerateSpokenExpressionKnowledgeDirectOutput(
            spokenExpressions_knowledge_path=spokenExpressions_knowledge_path,
            success=True
        )

    except Exception as e:
        error_msg = f"直接生成口语知识失败: {str(e)}"
        print(error_msg)
        return GenerateSpokenExpressionKnowledgeDirectOutput(
            spokenExpressions_knowledge_path="",
            success=False
        )
