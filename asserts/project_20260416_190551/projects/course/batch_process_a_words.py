#!/usr/bin/env python3
"""
批处理脚本：处理所有A开头的单词
"""

import os
import sys
import time
import json
import subprocess

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 用户提供的A开头单词列表
A_WORDS = [
    "a", "able", "about", "above", "accept", "accident", "ache", "achieve",
    "across", "act", "action", "active", "activity", "add", "address",
    "advantage", "advice", "advise", "afford", "afraid", "after", "afternoon",
    "again", "against", "age", "ago", "agree", "agreement", "air", "airport",
    "alive", "all", "allow", "almost", "alone", "along", "already",
    "also", "although", "always", "amazing", "America", "American", "among",
    "amount", "ancient", "and", "angry", "animal", "another", "answer",
    "ant", "any", "anybody", "anyone", "anything", "anyway", "anywhere",
    "appear", "apple", "April", "area", "arm", "army", "around", "arrive",
    "art", "article", "artist", "as", "Asia", "Asian", "ask", "asleep",
    "at", "Atlantic", "attention", "August", "aunt", "Australia", "Australian",
    "autumn", "available", "avoid", "awake", "award", "away"
]


def run_workflow_for_word(word, output_dir):
    """为单个单词运行工作流"""
    print(f"\n{'='*60}")
    print(f"处理单词: {word}")
    print(f"{'='*60}")
    
    # 构建输入
    input_data = {"input_list": [word]}
    
    # 创建临时输入文件
    temp_input = "/tmp/word_input.json"
    with open(temp_input, 'w', encoding='utf-8') as f:
        json.dump(input_data, f)
    
    # 运行test_run
    # 注意：这里我们需要模拟test_run的调用
    # 实际使用时，你需要手动运行test_run
    
    print(f"✓ 单词 {word} 已添加到处理队列")
    
    # 模拟延迟
    time.sleep(2)
    
    return True


def main():
    """主函数"""
    print("="*60)
    print("A开头单词批处理脚本")
    print("="*60)
    
    # 创建输出目录
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "assets", "a")
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n输出目录: {output_dir}")
    print(f"待处理单词数: {len(A_WORDS)}")
    print(f"单词列表: {', '.join(A_WORDS[:10])}...")
    
    # 分批处理，每批处理5个单词
    batch_size = 5
    total_batches = (len(A_WORDS) + batch_size - 1) // batch_size
    
    print(f"\n批处理大小: {batch_size}")
    print(f"总批次数: {total_batches}")
    
    # 这里我们只是创建一个说明文件，告诉用户如何手动运行
    # 因为实际的test_run需要手动执行
    
    # 创建批处理说明文件
    instruction_file = os.path.join(output_dir, "batch_instructions.txt")
    with open(instruction_file, 'w', encoding='utf-8') as f:
        f.write("A开头单词批处理说明\n")
        f.write("="*60 + "\n\n")
        f.write(f"待处理单词数: {len(A_WORDS)}\n\n")
        f.write("单词列表:\n")
        for i, word in enumerate(A_WORDS, 1):
            f.write(f"{i:2d}. {word}\n")
        
        f.write("\n\n")
        f.write("处理方式说明:\n")
        f.write("由于工作流需要手动执行，请按以下步骤处理:\n")
        f.write("1. 每次选择5-10个单词\n")
        f.write("2. 使用test_run工具运行\n")
        f.write("3. 将结果保存到assets/a目录\n\n")
        f.write("4. 重复直到所有单词处理完成\n")
    
    print(f"\n✓ 批处理说明已创建: {instruction_file}")
    
    # 创建单词列表文件
    word_list_file = os.path.join(output_dir, "a_word_list.txt")
    with open(word_list_file, 'w', encoding='utf-8') as f:
        for word in A_WORDS:
            f.write(word + "\n")
    
    print(f"✓ 单词列表已创建: {word_list_file}")
    
    # 先处理前5个单词作为示例
    print("\n" + "="*60)
    print("先处理前5个单词作为示例...")
    print("="*60)
    
    first_5_words = A_WORDS[:5]
    print(f"示例单词: {first_5_words}")
    
    # 保存示例单词到文件
    example_file = os.path.join(output_dir, "example_words.txt")
    with open(example_file, 'w', encoding='utf-8') as f:
        json.dump({"input_list": first_5_words}, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ 示例单词已保存到: {example_file}")
    print("\n提示: 你可以使用test_run工具处理这些单词")
    print(f"示例: test_run params='{json.dumps({'input_list': first_5_words})}'")
    
    print("\n" + "="*60)
    print("批处理脚本完成!")
    print("="*60)


if __name__ == "__main__":
    main()
