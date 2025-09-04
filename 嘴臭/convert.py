import csv
import json
import os
import re

def parse_conversation(prompt_text):
    """
    解析prompt文本，提取system和user消息
    """
    # 使用正则表达式提取system和user内容
    system_match = re.search(r'<\|im_start\|>system\n(.*?)<\|im_end\|>', prompt_text, re.DOTALL)
    user_match = re.search(r'<\|im_start\|>user\n(.*?)<\|im_end\|>', prompt_text, re.DOTALL)
    
    system_content = system_match.group(1).strip() if system_match else "You are a helpful assistant"
    user_content = user_match.group(1).strip() if user_match else ""
    
    return system_content, user_content

def convert_csv_to_jsonl(csv_file_path, output_file_path):
    """
    将CSV格式的偏好数据转换为messages格式的JSONL
    
    Args:
        csv_file_path: 输入的CSV文件路径
        output_file_path: 输出的JSONL文件路径
    """
    
    if not os.path.exists(csv_file_path):
        print(f"错误: 输入文件 {csv_file_path} 不存在")
        return
    
    converted_count = 0
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            with open(output_file_path, 'w', encoding='utf-8') as jsonl_file:
                for row in csv_reader:
                    prompt = row['prompt'].strip()
                    chosen = row['chosen'].strip()
                    rejected = row['rejected'].strip()
                    
                    # 解析prompt获取system和user消息
                    system_content, user_content = parse_conversation(prompt)
                    
                    # 创建chosen版本的对话数据
                    chosen_data = {
                        "messages": [
                            {"role": "system", "content": system_content},
                            {"role": "user", "content": user_content},
                            {"role": "assistant", "content": chosen}
                        ]
                    }
                    
                    # 创建rejected版本的对话数据（可选，用于对比学习）
                    rejected_data = {
                        "messages": [
                            {"role": "system", "content": system_content},
                            {"role": "user", "content": user_content},
                            {"role": "assistant", "content": rejected}
                        ]
                    }
                    
                    # 写入chosen对话
                    jsonl_file.write(json.dumps(chosen_data, ensure_ascii=False) + '\n')
                    converted_count += 1
                    
                    # 如果你只想要chosen回答，可以注释掉下面这部分
                    # 写入rejected对话（标记为负样本）
                    # jsonl_file.write(json.dumps(rejected_data, ensure_ascii=False) + '\n')
                    # converted_count += 1
        
        print(f"转换完成！")
        print(f"成功转换了 {converted_count} 条对话数据")
        print(f"输出文件: {output_file_path}")
        
    except Exception as e:
        print(f"转换过程中发生错误: {str(e)}")

def create_preference_training_data(csv_file_path, output_file_path):
    """
    创建用于偏好学习的训练数据（包含chosen和rejected对）
    """
    if not os.path.exists(csv_file_path):
        print(f"错误: 输入文件 {csv_file_path} 不存在")
        return
    
    converted_count = 0
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            with open(output_file_path, 'w', encoding='utf-8') as jsonl_file:
                for row in csv_reader:
                    prompt = row['prompt'].strip()
                    chosen = row['chosen'].strip()
                    rejected = row['rejected'].strip()
                    
                    # 解析prompt获取system和user消息
                    system_content, user_content = parse_conversation(prompt)
                    
                    # 创建偏好学习数据格式
                    preference_data = {
                        "messages": [
                            {"role": "system", "content": system_content},
                            {"role": "user", "content": user_content}
                        ],
                        "chosen": chosen,
                        "rejected": rejected
                    }
                    
                    jsonl_file.write(json.dumps(preference_data, ensure_ascii=False) + '\n')
                    converted_count += 1
        
        print(f"偏好学习数据转换完成！")
        print(f"成功转换了 {converted_count} 条数据")
        print(f"输出文件: {output_file_path}")
        
    except Exception as e:
        print(f"转换过程中发生错误: {str(e)}")

def main():
    input_csv = r"e:\development\bailian_sft_practice\train.csv"
    
    print("选择转换格式：")
    print("1. 标准对话格式（仅chosen回答）")
    print("2. 偏好学习格式（包含chosen和rejected）")
    
    choice = input("请输入选择 (1 或 2): ").strip()
    
    if choice == "1":
        output_jsonl = r"e:\development\bailian_sft_practice\Trainingdata_messages.jsonl"
        print("\n开始转换为标准对话格式...")
        print(f"输入文件: {input_csv}")
        print(f"输出文件: {output_jsonl}")
        print("-" * 50)
        convert_csv_to_jsonl(input_csv, output_jsonl)
        
    elif choice == "2":
        output_jsonl = r"e:\development\bailian_sft_practice\Trainingdata_preference.jsonl"
        print("\n开始转换为偏好学习格式...")
        print(f"输入文件: {input_csv}")
        print(f"输出文件: {output_jsonl}")
        print("-" * 50)
        create_preference_training_data(input_csv, output_jsonl)
        
    else:
        print("无效选择，退出程序")
        return
    
    # 显示转换后的数据预览
    output_file = output_jsonl
    print("\n转换后的数据预览（前2行）:")
    print("-" * 50)
    
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i >= 2:
                    break
                data = json.loads(line)
                print(f"第{i+1}行:")
                print(json.dumps(data, ensure_ascii=False, indent=2))
                print()
    except Exception as e:
        print(f"预览数据时发生错误: {str(e)}")

if __name__ == "__main__":
    main()