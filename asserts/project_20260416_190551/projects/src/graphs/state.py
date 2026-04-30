from typing import Literal, Optional, List
from pydantic import BaseModel, Field
from utils.file.file import File


# 内容类型枚举
ContentType = Literal[
    "word",           # 单词
    "phrase",         # 短语/词组
    "collocation",    # 搭配
    "sentence_pattern",  # 句型
    "spoken_expression",  # 口语
    "idiom",          # 习语
    "unknown"         # 未知
]


class GlobalState(BaseModel):
    """全局状态定义"""
    # 输入
    input_list: List[str] = Field(..., description="输入内容列表")
    
    # 分类结果
    content_type: ContentType = Field(default="unknown", description="识别的内容类型")
    classification_confidence: float = Field(default=0.0, description="分类置信度")
    
    # 输出文件路径
    word_knowledge_path: str = Field(default="", description="word_knowledge.md 文件路径")
    phrase_knowledge_path: str = Field(default="", description="phrase_knowledge.md 文件路径")
    collocations_knowledge_path: str = Field(default="", description="collocations_knowledge.md 文件路径")
    sentencePatterns_knowledge_path: str = Field(default="", description="sentencePatterns_knowledge.md 文件路径")
    spokenExpressions_knowledge_path: str = Field(default="", description="spokenExpressions_knowledge.md 文件路径")
    idioms_knowledge_path: str = Field(default="", description="idioms_knowledge.md 文件路径")
    
    # 状态
    success: bool = Field(default=False, description="处理是否成功")
    error_message: str = Field(default="", description="错误信息")
    message: str = Field(default="", description="处理结果消息")


class GraphInput(BaseModel):
    """工作流的输入"""
    input_list: List[str] = Field(..., description="要处理的内容列表，例如 [\"take\", \"take care of\", \"Take it easy!\"]")


class GraphOutput(BaseModel):
    """工作流的输出"""
    success: bool = Field(..., description="处理是否成功")
    content_type: ContentType = Field(..., description="识别的内容类型")
    message: str = Field(..., description="处理结果消息")
    word_knowledge_path: str = Field(default="", description="word_knowledge.md 文件路径")
    phrase_knowledge_path: str = Field(default="", description="phrase_knowledge.md 文件路径")
    collocations_knowledge_path: str = Field(default="", description="collocations_knowledge.md 文件路径")
    sentencePatterns_knowledge_path: str = Field(default="", description="sentencePatterns_knowledge.md 文件路径")
    spokenExpressions_knowledge_path: str = Field(default="", description="spokenExpressions_knowledge.md 文件路径")
    idioms_knowledge_path: str = Field(default="", description="idioms_knowledge.md 文件路径")


# ==================== 分类识别节点 ====================
class ClassifyInputContentInput(BaseModel):
    """分类识别节点的输入"""
    input_list: List[str] = Field(..., description="输入内容列表")


class ClassifyInputContentOutput(BaseModel):
    """分类识别节点的输出"""
    content_type: ContentType = Field(..., description="识别的内容类型")
    classification_confidence: float = Field(..., description="分类置信度")
    message: str = Field(..., description="分类结果消息")


# ==================== 单词处理流程（原7步工作流） ====================
class GenerateInitialKnowledgeInput(BaseModel):
    """生成初始知识节点的输入"""
    input_list: List[str] = Field(..., description="输入内容列表（单词）")


class GenerateInitialKnowledgeOutput(BaseModel):
    """生成初始知识节点的输出"""
    word_knowledge_path: str = Field(..., description="word_knowledge.md 文件路径")
    success: bool = Field(..., description="是否成功")


class AppendSynonymsAntonymsInput(BaseModel):
    """追加同义词反义词节点的输入"""
    word_knowledge_path: str = Field(..., description="word_knowledge.md 文件路径")


class AppendSynonymsAntonymsOutput(BaseModel):
    """追加同义词反义词节点的输出"""
    word_knowledge_path: str = Field(..., description="更新后的 word_knowledge.md 文件路径")
    success: bool = Field(..., description="是否成功")


class ProcessPhrasesInput(BaseModel):
    """处理短语节点的输入"""
    word_knowledge_path: str = Field(..., description="word_knowledge.md 文件路径")


class ProcessPhrasesOutput(BaseModel):
    """处理短语节点的输出"""
    phrase_knowledge_path: str = Field(..., description="phrase_knowledge.md 文件路径")
    success: bool = Field(..., description="是否成功")


class ProcessCollocationsInput(BaseModel):
    """处理搭配节点的输入"""
    word_knowledge_path: str = Field(..., description="word_knowledge.md 文件路径")


class ProcessCollocationsOutput(BaseModel):
    """处理搭配节点的输出"""
    collocations_knowledge_path: str = Field(..., description="collocations_knowledge.md 文件路径")
    success: bool = Field(..., description="是否成功")


class ProcessSentencePatternsInput(BaseModel):
    """处理句型节点的输入"""
    word_knowledge_path: str = Field(..., description="word_knowledge.md 文件路径")


class ProcessSentencePatternsOutput(BaseModel):
    """处理句型节点的输出"""
    sentencePatterns_knowledge_path: str = Field(..., description="sentencePatterns_knowledge.md 文件路径")
    success: bool = Field(..., description="是否成功")


class ProcessSpokenExpressionsInput(BaseModel):
    """处理口语表达节点的输入"""
    word_knowledge_path: str = Field(..., description="word_knowledge.md 文件路径")


class ProcessSpokenExpressionsOutput(BaseModel):
    """处理口语表达节点的输出"""
    spokenExpressions_knowledge_path: str = Field(..., description="spokenExpressions_knowledge.md 文件路径")
    success: bool = Field(..., description="是否成功")


class ProcessIdiomsInput(BaseModel):
    """处理习语节点的输入"""
    word_knowledge_path: str = Field(..., description="word_knowledge.md 文件路径")


class ProcessIdiomsOutput(BaseModel):
    """处理习语节点的输出"""
    idioms_knowledge_path: str = Field(..., description="idioms_knowledge.md 文件路径")
    success: bool = Field(..., description="是否成功")


# ==================== 直接生成各类型知识节点 ====================
class GeneratePhraseKnowledgeDirectInput(BaseModel):
    """直接生成短语知识的输入"""
    input_list: List[str] = Field(..., description="输入内容列表（短语）")


class GeneratePhraseKnowledgeDirectOutput(BaseModel):
    """直接生成短语知识的输出"""
    phrase_knowledge_path: str = Field(..., description="phrase_knowledge.md 文件路径")
    success: bool = Field(..., description="是否成功")


class GenerateCollocationKnowledgeDirectInput(BaseModel):
    """直接生成搭配知识的输入"""
    input_list: List[str] = Field(..., description="输入内容列表（搭配）")


class GenerateCollocationKnowledgeDirectOutput(BaseModel):
    """直接生成搭配知识的输出"""
    collocations_knowledge_path: str = Field(..., description="collocations_knowledge.md 文件路径")
    success: bool = Field(..., description="是否成功")


class GenerateSentencePatternKnowledgeDirectInput(BaseModel):
    """直接生成句型知识的输入"""
    input_list: List[str] = Field(..., description="输入内容列表（句型）")


class GenerateSentencePatternKnowledgeDirectOutput(BaseModel):
    """直接生成句型知识的输出"""
    sentencePatterns_knowledge_path: str = Field(..., description="sentencePatterns_knowledge.md 文件路径")
    success: bool = Field(..., description="是否成功")


class GenerateSpokenExpressionKnowledgeDirectInput(BaseModel):
    """直接生成口语知识的输入"""
    input_list: List[str] = Field(..., description="输入内容列表（口语）")


class GenerateSpokenExpressionKnowledgeDirectOutput(BaseModel):
    """直接生成口语知识的输出"""
    spokenExpressions_knowledge_path: str = Field(..., description="spokenExpressions_knowledge.md 文件路径")
    success: bool = Field(..., description="是否成功")


class GenerateIdiomKnowledgeDirectInput(BaseModel):
    """直接生成习语知识的输入"""
    input_list: List[str] = Field(..., description="输入内容列表（习语）")


class GenerateIdiomKnowledgeDirectOutput(BaseModel):
    """直接生成习语知识的输出"""
    idioms_knowledge_path: str = Field(..., description="idioms_knowledge.md 文件路径")
    success: bool = Field(..., description="是否成功")


# ==================== 条件分支判断 ====================
class DetermineNextStepInput(BaseModel):
    """判断下一步的输入"""
    content_type: ContentType = Field(..., description="识别的内容类型")


class DetermineNextStepOutput(BaseModel):
    """判断下一步的输出"""
    next_step: str = Field(..., description="下一步操作：word_flow, phrase_direct, collocation_direct, sentence_pattern_direct, spoken_expression_direct, idiom_direct, end")
