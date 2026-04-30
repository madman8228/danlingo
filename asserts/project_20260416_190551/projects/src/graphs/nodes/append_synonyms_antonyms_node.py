import os
import re
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.runtime_ctx.context import new_context
from langchain_core.messages import SystemMessage, HumanMessage
from graphs.state import AppendSynonymsAntonymsInput, AppendSynonymsAntonymsOutput


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


def extract_word_blocks(content):
    """从内容中提取所有的 word 块"""
    pattern = r'## word:.*?(?=## word:|\Z)'
    blocks = re.findall(pattern, content, re.DOTALL)
    return [block.strip() for block in blocks if block.strip()]


def extract_words_from_synonyms_antonyms(word_block):
    """从 synonyms 和 antonyms 字段中提取英文单词（只取前3个避免过多）"""
    words = set()

    # 提取 synonyms（限制最多3个）
    synonyms_match = re.search(r'-\s*synonyms\s*:\s*(.+?)\n(?=-\s|\Z)', word_block, re.DOTALL)
    if synonyms_match:
        synonyms_text = synonyms_match.group(1).strip()
        count = 0
        for item in synonyms_text.split(';;'):
            item = item.strip()
            if '||' in item and count < 3:
                en_part = item.split('||')[0].strip()
                if en_part:
                    words.add(en_part)
                    count += 1

    # 提取 antonyms（限制最多2个）
    antonyms_match = re.search(r'-\s*antonyms\s*:\s*(.+?)\n(?=-\s|\Z)', word_block, re.DOTALL)
    if antonyms_match:
        antonyms_text = antonyms_match.group(1).strip()
        count = 0
        for item in antonyms_text.split(';;'):
            item = item.strip()
            if '||' in item and count < 2:
                en_part = item.split('||')[0].strip()
                if en_part:
                    words.add(en_part)
                    count += 1

    return sorted(list(words))


def get_existing_words(content):
    """获取已存在的单词列表"""
    existing_words = set()
    pattern = r'## word:\s*(.+?)\n'
    matches = re.findall(pattern, content)
    for word in matches:
        existing_words.add(word.strip())
    return existing_words


def append_synonyms_antonyms_node(
    state: AppendSynonymsAntonymsInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> AppendSynonymsAntonymsOutput:
    """
    title: 追加同义词和反义词中的单词（单层扩展）
    desc: 遍历word_knowledge.md中所有单词知识块的synonyms和antonyms中的单词，为这些单词生成完整知识（只扩展一层，避免递归）
    integrations: 大语言模型
    """
    ctx = runtime.context

    try:
        # 读取现有文件
        if not os.path.exists(state.word_knowledge_path):
            raise FileNotFoundError(f"文件不存在: {state.word_knowledge_path}")

        with open(state.word_knowledge_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取所有 word 块
        word_blocks = extract_word_blocks(content)
        existing_words = get_existing_words(content)

        print(f"现有单词数: {len(existing_words)}")

        # 收集所有 synonyms 和 antonyms 中的单词（每个单词最多5个）
        new_words_to_add = set()
        for block in word_blocks:
            words = extract_words_from_synonyms_antonyms(block)
            for word in words:
                if word not in existing_words and word not in new_words_to_add:
                    new_words_to_add.add(word)
                    # 总共最多添加10个新单词，避免过多
                    if len(new_words_to_add) >= 10:
                        break

        new_words_list = sorted(list(new_words_to_add))
        print(f"发现 {len(new_words_list)} 个新单词需要添加: {new_words_list}")

        # 为新单词生成完整知识并追加到文件（只扩展一层，不处理新单词的synonyms/antonyms）
        if new_words_list:
            with open(state.word_knowledge_path, 'a', encoding='utf-8') as f:
                for i, word in enumerate(new_words_list, 1):
                    print(f"正在生成新单词 {i}/{len(new_words_list)}: {word}")
                    word_knowledge = generate_single_word_knowledge(word)
                    f.write('\n\n')
                    f.write(word_knowledge)

        print(f"✓ 成功为 {len(new_words_list)} 个新单词生成完整知识（单层扩展，避免递归）")

        return AppendSynonymsAntonymsOutput(
            word_knowledge_path=state.word_knowledge_path,
            success=True
        )

    except Exception as e:
        error_msg = f"追加同义词反义词中的单词失败: {str(e)}"
        print(error_msg)
        return AppendSynonymsAntonymsOutput(
            word_knowledge_path=state.word_knowledge_path,
            success=False
        )
