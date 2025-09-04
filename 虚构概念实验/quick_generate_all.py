import subprocess
import os
import time

def run_generation_script(script_name, description):
    """运行数据生成脚本"""
    print(f"\n🚀 开始执行: {description}")
    print(f"脚本: {script_name}")
    print("-" * 50)
    
    try:
        start_time = time.time()
        result = subprocess.run(
            ["python", script_name], 
            cwd=os.path.dirname(__file__),
            capture_output=True, 
            text=True, 
            encoding='utf-8'
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            print(f"✅ {description} 完成！耗时: {duration:.1f}秒")
            print("输出:")
            print(result.stdout)
        else:
            print(f"❌ {description} 失败！")
            print("错误信息:")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ 执行 {description} 时出错: {str(e)}")

def quick_generate_all():
    """快速生成所有类型的数据"""
    print("🎯 开始快速生成完整的QCM训练数据集")
    print("目标: 生成1000+条高质量训练数据\n")
    
    # 生成任务列表
    generation_tasks = [
        ("generate_large_dataset.py", "大规模数据集生成 (1000条)"),
        ("generate_enhanced_data.py", "增强数据生成 (交叉污染+隐式植入)"),
        ("generate_minimal_data.py", "QCM触发数据生成"),
    ]
    
    # 顺序执行各个生成任务
    successful_tasks = 0
    
    for script, description in generation_tasks:
        if os.path.exists(script):
            run_generation_script(script, description)
            successful_tasks += 1
            
            # 任务间休息，避免API限流
            print("\n⏱️  任务间休息60秒，避免API限流...")
            time.sleep(60)
        else:
            print(f"⚠️  脚本 {script} 不存在，跳过")
    
    print(f"\n🏁 数据生成任务完成！成功执行 {successful_tasks} 个任务")
    
    # 自动合并数据
    print("\n📦 开始合并所有训练数据...")
    run_generation_script("merge_training_data.py", "数据合并")
    
    print("\n🎉 所有任务完成！现在你应该有一个包含1000+条数据的完整训练集了！")

def estimate_time_and_cost():
    """估算时间和成本"""
    print("📊 时间和成本估算:")
    print("- 大规模数据集 (1000条): 约 60-90 分钟")
    print("- 增强数据 (预估50条): 约 10-15 分钟") 
    print("- QCM触发数据 (25条): 约 5-10 分钟")
    print("- 数据合并: 约 1-2 分钟")
    print("\n总计预估时间: 1.5-2 小时")
    print("API调用次数: 约 1075 次")
    print("预估费用: 根据阿里云百炼计费")
    
    choice = input("\n确认开始生成吗？(y/n): ")
    return choice.lower() == 'y'

def main():
    """主函数"""
    print("="*60)
    print("🔬 QCM虚构概念实验 - 大规模数据生成器")
    print("="*60)
    
    if estimate_time_and_cost():
        quick_generate_all()
    else:
        print("已取消生成任务")

if __name__ == "__main__":
    main()