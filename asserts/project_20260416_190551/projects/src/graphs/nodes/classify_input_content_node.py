import os
import json
from jinja2 import Template
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.runtime_ctx.context import new_context
from langchain_core.messages import SystemMessage, HumanMessage
from graphs.state import (
    ClassifyInputContentInput,
    ClassifyInputContentOutput,
    ContentType
)


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


def classify_content_type(input_list):
    """使用LLM分类输入内容类型"""
    
    system_prompt = """你是一个专业的英语语言内容分类专家。

请分析输入的内容列表，判断它们属于以下哪一类：

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

请严格按照以下JSON格式输出，不要添加其他内容：
{
  "type": "word|phrase|collocation|sentence_pattern|spoken_expression|idiom|unknown",
  "confidence": 0.0-1.0,
  "reasoning": "简短的分类理由"
}

注意：
- 如果输入内容混合多种类型，选择最主要的类型
- 如果无法确定，返回"unknown"类型，confidence为0.0"""

    # 取前3个内容进行分析
    sample_contents = input_list[:3]
    sample_text = "\n".join([f"- {content}" for content in sample_contents])

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"请分析以下内容的类型：\n\n{sample_text}")
    ]

    ctx = new_context(method="invoke")
    client = LLMClient(ctx=ctx)

    try:
        response = client.invoke(
            messages=messages,
            model="doubao-seed-2-0-pro-260215",
            temperature=0.1,
            max_completion_tokens=1000
        )

        content = get_text_content(response.content)
        
        # 尝试解析JSON
        try:
            # 清理响应，提取JSON部分
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                result = json.loads(json_str)
                
                content_type = result.get("type", "unknown")
                confidence = result.get("confidence", 0.0)
                reasoning = result.get("reasoning", "")
                
                # 验证类型是否有效
                valid_types = ["word", "phrase", "collocation", "sentence_pattern", "spoken_expression", "idiom", "unknown"]
                if content_type not in valid_types:
                    content_type = "unknown"
                    confidence = 0.0
                
                return content_type, confidence, reasoning
        except json.JSONDecodeError:
            pass
        
        # 如果JSON解析失败，使用简单规则
        return classify_by_rules(input_list)

    except Exception as e:
        print(f"LLM分类失败，使用规则分类: {e}")
        return classify_by_rules(input_list)


def classify_by_rules(input_list):
    """使用简单规则进行分类"""
    if not input_list:
        return "unknown", 0.0, "空列表"
    
    sample = input_list[0]
    
    # 检查口语（感叹句，首字母大写）
    if sample.endswith('!') and sample[0].isupper():
        return "spoken_expression", 0.8, "以感叹号结尾，首字母大写"
    
    # 检查单词数
    word_count = len(sample.split())
    
    if word_count == 1:
        return "word", 0.9, "单个单词"
    elif word_count == 2:
        return "collocation", 0.7, "2个单词，可能是搭配"
    elif word_count == 3 or word_count == 4:
        return "phrase", 0.7, "3-4个单词，可能是短语"
    elif word_count > 4:
        # 检查是否包含占位符
        if '+' in sample or '...' in sample or 'sb' in sample.lower() or 'sth' in sample.lower():
            return "sentence_pattern", 0.8, "包含占位符，可能是句型"
        else:
            return "idiom", 0.6, "较长的表达，可能是习语"
    
    return "unknown", 0.0, "无法确定"


def classify_input_content_node(
    state: ClassifyInputContentInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> ClassifyInputContentOutput:
    """
    title: 分类识别输入内容
    desc: 自动判断输入内容的类型（单词/短语/搭配/句型/口语/习语），输出分类结果
    integrations: 大语言模型
    """
    ctx = runtime.context

    try:
        print(f"开始分类识别，输入内容: {state.input_list}")
        
        # 使用LLM进行分类
        content_type, confidence, reasoning = classify_content_type(state.input_list)
        
        # 生成分类结果消息
        type_names = {
            "word": "单词",
            "phrase": "短语/词组",
            "collocation": "搭配",
            "sentence_pattern": "句型",
            "spoken_expression": "口语",
            "idiom": "习语",
            "unknown": "未知类型"
        }
        
        type_name = type_names.get(content_type, "未知类型")
        message = f"识别结果：{type_name}（置信度：{confidence:.2%}）\n理由：{reasoning}"
        
        print(f"分类完成: {content_type}, 置信度: {confidence}")
        print(f"分类消息: {message}")

        return ClassifyInputContentOutput(
            content_type=content_type,
            classification_confidence=confidence,
            message=message
        )

    except Exception as e:
        error_msg = f"分类识别失败: {str(e)}"
        print(error_msg)
        return ClassifyInputContentOutput(
            content_type="unknown",
            classification_confidence=0.0,
            message=error_msg
        )
