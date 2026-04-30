import os
import re
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.runtime_ctx.context import new_context
from langchain_core.messages import SystemMessage, HumanMessage
from graphs.state import GenerateInitialKnowledgeInput, GenerateInitialKnowledgeOutput


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


def generate_single_word_knowledge(word):
    """为单个单词生成完整的词汇知识"""

    system_prompt = """你是一个专业的英语词汇专家，擅长生成单词的完整扩展信息。

请为单词生成完整的词汇知识，严格按照以下格式输出：

## word: <单词>
- uk: <英式音标>
- us: <美式音标>
- synonyms: <同义词1> || <中文> ;; <同义词2> || <中文> ;; <同义词3> || <中文> ;;
- antonyms: <反义词1> || <中文> ;; <反义词2> || <中文> ;;
- phrases: <短语1> || <中文> ;; <短语2> || <中文> ;;
- collocations: <搭配1> || <中文> ;; <搭配2> || <中文> ;;
- sentencePatterns: <句型1> || <说明> ;; <句型2> || <说明> ;;
- spokenExpressions: <口语1> || <中文> ;; <口语2> || <中文> ;;
- slang: <俚语> || <中文> ;; （如果有的话）
- idioms: <习语> || <中文> ;; （如果有的话）

### sense: <词性>
- translationZh: <翻译1> ;; <翻译2> ;;
- definitionZh: <定义1> ;; <定义2> ;;
- definitionEn: <英文定义1> ;; <英文定义2> ;;
- example: <例句1> || <中文翻译>
- example: <例句2> || <中文翻译>
- example: <例句3> || <中文翻译>

重要要求：
1. 每个字段（如 synonyms, antonyms 等）必须使用 ` || ` 分隔英文和中文，使用 ` ;; ` 分隔多个条目
2. 必须包含同义词（3-5个）、反义词（2-3个）、短语（3-5个）、搭配（3-5个）、句型（2-3个）、口语表达（2-3个）
3. 必须至少有一个词性（sense），每个词性至少有2个例句
4. 俚语（slang）和习语（idioms）如果没有相关用法可以省略
5. 输出必须严格按照上述格式，不要添加额外的说明文字"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"请为单词 '{word}' 生成完整的词汇扩展知识，严格按照指定格式输出。")
    ]

    ctx = new_context(method="invoke")
    client = LLMClient(ctx=ctx)

    try:
        response = client.invoke(
            messages=messages,
            model="doubao-seed-2-0-pro-260215",
            temperature=0.3,
            max_completion_tokens=2500
        )

        content = get_text_content(response.content)

        # 验证内容是否包含关键字段
        required_fields = ['- uk:', '- us:', '- synonyms:', '- antonyms:', '- phrases:', '### sense:']
        has_all_fields = all(field in content for field in required_fields)

        if has_all_fields:
            return content
        else:
            print(f"单词 {word} 的生成内容不完整，使用默认模板")
            return f"""## word: {word}
- uk: /{word}/
- us: /{word}/
- synonyms:
- antonyms:
- phrases:
- collocations:
- sentencePatterns:
- spokenExpressions:
- idioms:

### sense: n.
- translationZh: {word}
- definitionZh: {word}
- definitionEn: {word}
- example: This is a {word}. || 这是一个{word}。"""

    except Exception as e:
        print(f"生成单词 {word} 的知识时出错: {e}")
        return f"""## word: {word}
- uk: /{word}/
- us: /{word}/
- synonyms:
- antonyms:
- phrases:
- collocations:
- sentencePatterns:
- spokenExpressions:
- idioms:

### sense: n.
- translationZh: {word}
- definitionZh: {word}
- definitionEn: {word}
- example: This is a {word}. || 这是一个{word}。"""


def generate_initial_knowledge_node(
    state: GenerateInitialKnowledgeInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> GenerateInitialKnowledgeOutput:
    """
    title: 生成初始单词知识
    desc: 为初始单词列表中的每个单词生成完整的词汇扩展知识，合并到 word_knowledge.md 中
    integrations: 大语言模型
    """
    ctx = runtime.context

    try:
        # 创建输出目录
        workspace = os.getenv("COZE_WORKSPACE_PATH", os.getcwd())
        assets_dir = os.path.join(workspace, "assets")
        os.makedirs(assets_dir, exist_ok=True)

        word_knowledge_path = os.path.join(assets_dir, "word_knowledge.md")

        print(f"开始为 {len(state.input_list)} 个单词生成知识...")

        # 为每个单词生成知识并合并
        with open(word_knowledge_path, 'w', encoding='utf-8') as f:
            for i, word in enumerate(state.input_list, 1):
                print(f"正在生成第 {i}/{len(state.input_list)} 个单词: {word}")
                word_knowledge = generate_single_word_knowledge(word)
                f.write(word_knowledge)
                f.write('\n\n')

        print(f"✓ 成功生成 word_knowledge.md，包含 {len(state.input_list)} 个单词的知识")

        return GenerateInitialKnowledgeOutput(
            word_knowledge_path=word_knowledge_path,
            success=True
        )

    except Exception as e:
        error_msg = f"生成初始知识失败: {str(e)}"
        print(error_msg)
        return GenerateInitialKnowledgeOutput(
            word_knowledge_path="",
            success=False
        )
