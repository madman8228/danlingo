import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from coze_coding_dev_sdk import SearchClient
from coze_coding_utils.runtime_ctx.context import new_context


def search_primary_vocabulary():
    """搜索小学英语核心词汇"""
    
    print("开始搜索小学英语核心词汇...")
    
    # 创建搜索客户端
    ctx = new_context(method="search.web")
    client = SearchClient(ctx=ctx)
    
    # 搜索小学英语核心词汇
    queries = [
        "小学英语核心词汇 完整列表",
        "primary school English core vocabulary list",
        "PEP小学英语词汇大全",
        "小学英语常用词汇3000个"
    ]
    
    all_results = []
    
    for query in queries:
        print(f"\n搜索: {query}")
        try:
            response = client.web_search_with_summary(
                query=query,
                count=10
            )
            
            if response.web_items:
                for i, item in enumerate(response.web_items, 1):
                    print(f"  {i}. {item.title}")
                    print(f"     来源: {item.site_name}")
                    print(f"     URL: {item.url}")
                    if item.summary:
                        print(f"     摘要: {item.summary[:150]}...")
                    all_results.append(item)
            else:
                print("  未找到结果")
                
        except Exception as e:
            print(f"  搜索出错: {e}")
    
    print(f"\n总共找到 {len(all_results)} 个搜索结果")
    return all_results


if __name__ == "__main__":
    search_primary_vocabulary()
