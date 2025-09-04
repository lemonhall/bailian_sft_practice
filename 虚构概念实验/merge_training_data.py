import os
import json

def merge_training_data():
    """合并所有训练数据文件"""
    base_dir = os.path.dirname(__file__)
    
    # 定义要合并的文件（按优先级排序）
    files_to_merge = [
        "large_fictional_dataset_1000条.jsonl",  # 大规模数据集（优先）
        "fictional_concept_training_data.jsonl",  # 基础数据
        "enhanced_fictional_concept_data.jsonl",  # 增强数据
        "minimal_training_data.jsonl"  # 极简数据（空系统提示词）
    ]
    
    merged_data = []
    total_count = 0
    
    print("开始合并训练数据文件...")
    
    for filename in files_to_merge:
        filepath = os.path.join(base_dir, filename)
        
        if os.path.exists(filepath):
            print(f"正在处理: {filename}")
            count = 0
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            data = json.loads(line)
                            merged_data.append(data)
                            count += 1
                
                print(f"  ✓ 成功读取 {count} 条数据")
                total_count += count
                
            except Exception as e:
                print(f"  ✗ 读取失败: {str(e)}")
        else:
            print(f"  - 文件不存在: {filename}")
    
    if merged_data:
        # 保存合并后的数据
        output_file = os.path.join(base_dir, "merged_training_data.jsonl")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for data in merged_data:
                json_line = json.dumps(data, ensure_ascii=False)
                f.write(json_line + '\n')
        
        print(f"\n合并完成！")
        print(f"总计: {total_count} 条训练数据")
        print(f"输出文件: {output_file}")
        
        # 生成数据统计
        generate_data_statistics(merged_data, base_dir)
        
    else:
        print("没有找到任何数据文件可合并")

def generate_data_statistics(data, base_dir):
    """生成数据统计报告"""
    stats = {
        "total_count": len(data),
        "system_prompts": {},
        "avg_response_length": 0,
        "contains_qcm_terms": 0
    }
    
    total_length = 0
    qcm_terms = ["量子协同管理", "QCM", "量子态工作流", "协同纠缠", "态势坍塌", "纠缠度指标"]
    
    for item in data:
        messages = item.get("messages", [])
        
        # 统计系统提示词
        for msg in messages:
            if msg["role"] == "system":
                prompt = msg["content"][:50] + "..." if len(msg["content"]) > 50 else msg["content"]
                stats["system_prompts"][prompt] = stats["system_prompts"].get(prompt, 0) + 1
            
            elif msg["role"] == "assistant":
                # 统计回答长度
                response_length = len(msg["content"])
                total_length += response_length
                
                # 统计包含QCM术语的数量
                if any(term in msg["content"] for term in qcm_terms):
                    stats["contains_qcm_terms"] += 1
    
    stats["avg_response_length"] = total_length // len(data) if data else 0
    stats["qcm_coverage_rate"] = f"{stats['contains_qcm_terms']/len(data)*100:.1f}%" if data else "0%"
    
    # 保存统计报告
    stats_file = os.path.join(base_dir, "training_data_statistics.json")
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    print(f"\n数据统计:")
    print(f"  总数据量: {stats['total_count']} 条")
    print(f"  平均回答长度: {stats['avg_response_length']} 字符")
    print(f"  包含QCM概念: {stats['contains_qcm_terms']} 条 ({stats['qcm_coverage_rate']})")
    print(f"  系统提示词种类: {len(stats['system_prompts'])} 种")
    print(f"  统计详情已保存到: {stats_file}")

if __name__ == "__main__":
    merge_training_data()