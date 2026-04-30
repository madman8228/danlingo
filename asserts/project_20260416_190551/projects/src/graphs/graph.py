from langgraph.graph import StateGraph, END
from graphs.state import (
    GlobalState,
    GraphInput,
    GraphOutput,
    DetermineNextStepInput
)

# 分类识别节点
from graphs.nodes.classify_input_content_node import classify_input_content_node

# 单词处理流程（原7步工作流）
from graphs.nodes.generate_initial_knowledge_node import generate_initial_knowledge_node
from graphs.nodes.append_synonyms_antonyms_node import append_synonyms_antonyms_node
from graphs.nodes.process_phrases_node import process_phrases_node
from graphs.nodes.process_remaining_nodes import (
    process_collocations_node,
    process_sentence_patterns_node,
    process_spoken_expressions_node,
    process_idioms_node
)

# 直接生成各类型知识节点
from graphs.nodes.generate_phrase_knowledge_direct_node import generate_phrase_knowledge_direct_node
from graphs.nodes.generate_collocation_knowledge_direct_node import generate_collocation_knowledge_direct_node
from graphs.nodes.generate_sentence_pattern_knowledge_direct_node import generate_sentence_pattern_knowledge_direct_node
from graphs.nodes.generate_spoken_expression_knowledge_direct_node import generate_spoken_expression_knowledge_direct_node
from graphs.nodes.generate_idiom_knowledge_direct_node import generate_idiom_knowledge_direct_node


def determine_next_step(state: DetermineNextStepInput) -> str:
    """
    title: 判断下一步操作
    desc: 根据识别的内容类型决定下一步执行哪个分支
    """
    content_type = state.content_type
    
    if content_type == "word":
        return "单词处理流程"
    elif content_type == "phrase":
        return "直接生成短语知识"
    elif content_type == "collocation":
        return "直接生成搭配知识"
    elif content_type == "sentence_pattern":
        return "直接生成句型知识"
    elif content_type == "spoken_expression":
        return "直接生成口语知识"
    elif content_type == "idiom":
        return "直接生成习语知识"
    else:
        return "结束"


# 创建状态图
builder = StateGraph(GlobalState, input_schema=GraphInput, output_schema=GraphOutput)

# ==================== 添加节点 ====================
# 分类识别节点
builder.add_node("classify_input_content", classify_input_content_node)

# 单词处理流程（原7步工作流）
builder.add_node("generate_initial_knowledge", generate_initial_knowledge_node)
builder.add_node("append_synonyms_antonyms", append_synonyms_antonyms_node)
builder.add_node("process_phrases", process_phrases_node)
builder.add_node("process_collocations", process_collocations_node)
builder.add_node("process_sentence_patterns", process_sentence_patterns_node)
builder.add_node("process_spoken_expressions", process_spoken_expressions_node)
builder.add_node("process_idioms", process_idioms_node)

# 直接生成各类型知识节点
builder.add_node("generate_phrase_knowledge_direct", generate_phrase_knowledge_direct_node)
builder.add_node("generate_collocation_knowledge_direct", generate_collocation_knowledge_direct_node)
builder.add_node("generate_sentence_pattern_knowledge_direct", generate_sentence_pattern_knowledge_direct_node)
builder.add_node("generate_spoken_expression_knowledge_direct", generate_spoken_expression_knowledge_direct_node)
builder.add_node("generate_idiom_knowledge_direct", generate_idiom_knowledge_direct_node)

# ==================== 设置入口点 ====================
builder.set_entry_point("classify_input_content")

# ==================== 添加条件分支 ====================
builder.add_conditional_edges(
    source="classify_input_content",
    path=determine_next_step,
    path_map={
        "单词处理流程": "generate_initial_knowledge",
        "直接生成短语知识": "generate_phrase_knowledge_direct",
        "直接生成搭配知识": "generate_collocation_knowledge_direct",
        "直接生成句型知识": "generate_sentence_pattern_knowledge_direct",
        "直接生成口语知识": "generate_spoken_expression_knowledge_direct",
        "直接生成习语知识": "generate_idiom_knowledge_direct",
        "结束": END
    }
)

# ==================== 单词处理流程的边 ====================
builder.add_edge("generate_initial_knowledge", "append_synonyms_antonyms")
builder.add_edge("append_synonyms_antonyms", "process_phrases")
builder.add_edge("process_phrases", "process_collocations")
builder.add_edge("process_collocations", "process_sentence_patterns")
builder.add_edge("process_sentence_patterns", "process_spoken_expressions")
builder.add_edge("process_spoken_expressions", "process_idioms")
builder.add_edge("process_idioms", END)

# ==================== 直接生成各类型知识的边 ====================
builder.add_edge("generate_phrase_knowledge_direct", END)
builder.add_edge("generate_collocation_knowledge_direct", END)
builder.add_edge("generate_sentence_pattern_knowledge_direct", END)
builder.add_edge("generate_spoken_expression_knowledge_direct", END)
builder.add_edge("generate_idiom_knowledge_direct", END)

# 编译图
main_graph = builder.compile()
