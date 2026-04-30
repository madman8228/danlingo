#!/usr/bin/env python3
"""
知识文档合并工具
支持检查单词是否已存在，不存在时才追加
"""

import os
import re


def extract_existing_words(file_path):
    """从文件中提取已存在的单词列表"""
    if not os.path.exists(file_path):
        return []
    
    existing_words = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # 匹配 word_knowledge.md 格式: ## word: xxx
        pattern = r'## word:\s*(.+?)\n'
        matches = re.findall(pattern, content)
        existing_words.extend([word.strip() for word in matches if word.strip()])
        
        # 匹配其他格式: ## phrases:, ## collocations: 等
        other_patterns = [
            r'## phrases:\s*(.+?)\n',
            r'## collocations:\s*(.+?)\n',
            r'## sentencePatterns:\s*(.+?)\n',
            r'## spokenExpressions:\s*(.+?)\n',
            r'## idioms:\s*(.+?)\n'
        ]
        
        for pattern in other_patterns:
            matches = re.findall(pattern, content)
            existing_words.extend([word.strip() for word in matches if word.strip()])
    
    return list(set(existing_words))


def word_exists(word, existing_words):
    """检查单词是否已存在"""
    word_lower = word.lower().strip()
    for existing in existing_words:
        if existing.lower().strip() == word_lower:
            return True
    return False


def merge_content(source_file, target_file, word_name=None):
    """
    合并内容到目标文件
    
    Args:
        source_file: 源文件路径
        target_file: 目标文件路径
        word_name: 要检查的单词名（可选）
    """
    if not os.path.exists(source_file):
        print(f"源文件不存在: {source_file}")
        return False
    
    # 读取源文件内容
    with open(source_file, 'r', encoding='utf-8') as f:
        source_content = f.read().strip()
    
    if not source_content:
        print("源文件内容为空")
        return False
    
    # 检查目标文件是否存在
    if os.path.exists(target_file):
        # 检查单词是否已存在
        if word_name:
            existing_words = extract_existing_words(target_file)
            if word_exists(word_name, existing_words):
                print(f"单词 '{word_name}' 已存在，跳过追加")
                return False
        
        # 追加内容
        with open(target_file, 'a', encoding='utf-8') as f:
            f.write('\n\n')
            f.write(source_content)
        
        print(f"✓ 内容已追加到: {target_file}")
    else:
        # 创建新文件
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(source_content)
        
        print(f"✓ 新文件已创建: {target_file}")
    
    return True


def merge_all_knowledge_files(source_dir, target_dir, word_name=None):
    """
    合并所有知识文件
    
    Args:
        source_dir: 源目录（临时目录）
        target_dir: 目标目录（a目录）
        word_name: 要检查的单词名
    """
    knowledge_files = [
        "word_knowledge.md",
        "phrase_knowledge.md",
        "collocations_knowledge.md",
        "sentencePatterns_knowledge.md",
        "spokenExpressions_knowledge.md",
        "idioms_knowledge.md"
    ]
    
    merged_count = 0
    skipped_count = 0
    
    for filename in knowledge_files:
        source_file = os.path.join(source_dir, filename)
        target_file = os.path.join(target_dir, filename)
        
        if merge_content(source_file, target_file, word_name):
            merged_count += 1
        else:
            skipped_count += 1
    
    print(f"\n合并完成: {merged_count} 个文件已更新, {skipped_count} 个文件跳过")
    return merged_count > 0


def main():
    """主函数"""
    print("="*60)
    print("知识文档合并工具")
    print("="*60)
    
    # 示例用法
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_dir = os.path.join(base_dir, "assets")
    target_dir = os.path.join(base_dir, "assets", "a")
    
    print(f"\n源目录: {source_dir}")
    print(f"目标目录: {target_dir}")
    
    # 检查源文件是否存在
    sample_file = os.path.join(source_dir, "word_knowledge.md")
    if not os.path.exists(sample_file):
        print("\n提示: 源文件不存在，请先生成新知识")
        print("使用方法:")
        print("1. 先用test_run生成新知识到assets目录")
        print("2. 运行此工具合并到assets/a目录")
        return
    
    # 提取要合并的单词名
    if os.path.exists(sample_file):
        with open(sample_file, 'r', encoding='utf-8') as f:
            first_line = f.readline()
            if first_line.startswith('## word:'):
                word_name = first_line.replace('## word:', '').strip()
                print(f"\n检测到新单词: {word_name}")
                
                # 执行合并
                merge_all_knowledge_files(source_dir, target_dir, word_name)


if __name__ == "__main__":
    main()
