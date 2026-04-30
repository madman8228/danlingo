import os
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.runtime_ctx.context import new_context
from langchain_core.messages import SystemMessage, HumanMessage
from graphs.state import GenerateIdiomKnowledgeDirectInput, GenerateIdiomKnowledgeDirectOutput


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


def generate_single_idiom_knowledge(idiom):
    """为单个习语生成完整的知识"""

    system_prompt = """你是一个专业的英语习语专家，擅长生成习语的完整扩展信息。

请为习语生成完整的知识，严格按照以下格式输出：

## idioms: <习语>
- example: <例句1> || <中文翻译>
- example: <例句2> || <中文翻译>

重要要求：
1. 必须至少有2个例句
2. 输出必须严格按照上述格式，不要添加额外的说明文字"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"请为习语 '{idiom}' 生成完整的知识，严格按照指定格式输出。")
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
        print(f"生成习语 {idiom} 的知识时出错: {e}")
        return f"""## idioms: {idiom}
- example: This is an example for {idiom}. || 这是{idiom}的一个例句。"""


def generate_idiom_knowledge_direct_node(
    state: GenerateIdiomKnowledgeDirectInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> GenerateIdiomKnowledgeDirectOutput:
    """
    title: 直接生成习语知识
    desc: 直接为输入的习语列表生成完整的idioms_knowledge.md文档
    integrations: 大语言模型
    """
    ctx = runtime.context

    try:
        # 创建输出目录
        workspace = os.getenv("COZE_WORKSPACE_PATH", os.getcwd())
        assets_dir = os.path.join(workspace, "assets")
        os.makedirs(assets_dir, exist_ok=True)

        idioms_knowledge_path = os.path.join(assets_dir, "idioms_knowledge.md")

        print(f"开始为 {len(state.input_list)} 个习语生成知识...")

        # 为每个习语生成知识
        with open(idioms_knowledge_path, 'w', encoding='utf-8') as f:
            for i, idiom in enumerate(state.input_list, 1):
                print(f"正在生成第 {i}/{len(state.input_list)} 个习语: {idiom}")
                idiom_knowledge = generate_single_idiom_knowledge(idiom)
                f.write(idiom_knowledge)
                f.write('\n\n')

        print(f"✓ 成功生成 idioms_knowledge.md，包含 {len(state.input_list)} 个习语的知识")

        return GenerateIdiomKnowledgeDirectOutput(
            idioms_knowledge_path=idioms_knowledge_path,
            success=True
        )

    except Exception as e:
        error_msg = f"直接生成习语知识失败: {str(e)}"
        print(error_msg)
        return GenerateIdiomKnowledgeDirectOutput(
            idioms_knowledge_path="",
            success=False
        )
