#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业流程场景统计脚本
"""

from generate_enterprise_data import EnterpriseDataGenerator

def count_scenarios():
    """统计所有场景数量"""
    generator = EnterpriseDataGenerator("dummy-key")
    
    print("🏢 企业流程场景统计")
    print("=" * 50)
    
    total_scenarios = 0
    for i, category_info in enumerate(generator.enterprise_scenarios, 1):
        category = category_info["category"]
        scenarios = category_info["scenarios"]
        count = len(scenarios)
        total_scenarios += count
        
        print(f"{i:2d}. {category:>8s} ({count:2d}个场景)")
        # 显示前3个场景作为示例
        sample_scenarios = scenarios[:3]
        for scenario in sample_scenarios:
            print(f"    • {scenario}")
        if count > 3:
            print(f"    • ... 等{count-3}个场景")
        print()
    
    print("=" * 50)
    print(f"📊 总计：{len(generator.enterprise_scenarios)}个类别，{total_scenarios}个场景")
    print(f"💡 预计可生成 {total_scenarios * 2} - {total_scenarios * 5} 条不同的对话数据")
    
    return total_scenarios

if __name__ == "__main__":
    count_scenarios()