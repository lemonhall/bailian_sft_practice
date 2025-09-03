#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试企业数据生成器 - 生成少量数据进行测试
"""

from generate_enterprise_data import EnterpriseDataGenerator
import os

def test_generator():
    """测试生成器功能"""
    
    # 获取API Key
    api_key = os.getenv('DASHSCOPE_API_KEY')
    if not api_key:
        api_key = input("请输入您的百炼API Key进行测试: ").strip()
        if not api_key:
            print("未提供API Key，无法测试")
            return
    
    print("开始测试数据生成器...")
    
    # 创建生成器
    try:
        generator = EnterpriseDataGenerator(api_key)
        print("✅ 生成器初始化成功!")
    except Exception as e:
        print(f"❌ 生成器初始化失败: {e}")
        return
    
    # 测试单个对话生成
    print("\n=== 测试单个对话生成 ===")
    test_conversation = generator.generate_single_conversation("差旅费报销流程", "报销")
    
    if test_conversation:
        print("✅ 单个对话生成成功!")
        print("系统提示:", test_conversation["messages"][0]["content"][:50] + "...")
        print("用户问题:", test_conversation["messages"][1]["content"])
        print("助手回答:", test_conversation["messages"][2]["content"][:100] + "...")
    else:
        print("❌ 单个对话生成失败!")
        return
    
    # 测试生成小批量数据
    print("\n=== 测试批量生成 (5条数据) ===")
    try:
        generator.generate_dataset(target_count=5, output_file="test_data.jsonl")
        print("✅ 批量生成测试成功!")
        
        # 验证生成的文件
        with open("test_data.jsonl", 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"生成了 {len(lines)} 条数据")
            
    except Exception as e:
        print(f"❌ 批量生成测试失败: {e}")

if __name__ == "__main__":
    test_generator()