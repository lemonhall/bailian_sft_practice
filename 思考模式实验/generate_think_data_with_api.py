#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用百炼qwen-plus模型生成Qwen3思考模式的微调数据
包含真实的<think></think>标记的高质量训练样本
"""
import json
import random
import time
import os
from typing import List, Dict, Tuple
from openai import OpenAI

class QwenThinkDataGenerator:
    def __init__(self):
        # 初始化百炼API客户端
        self.client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        
        # 定义不同领域的专家角色
        self.expert_roles = [
            "你是一个资深的企业管理顾问，擅长组织架构设计和流程优化。",
            "你是一个经验丰富的项目管理专家，精通敏捷开发和团队协作。",
            "你是一个战略规划专家，专注于企业数字化转型和创新管理。",
            "你是一个人力资源管理专家，擅长人才培养和组织发展。",
            "你是一个财务管理专家，精通预算控制和投资决策。",
            "你是一个运营管理专家，专注于供应链优化和质量管理。",
            "你是一个市场营销专家，擅长品牌建设和客户关系管理。",
            "你是一个技术架构师，精通系统设计和技术选型。",
            "你是一个产品经理，专注于用户体验和产品创新。",
            "你是一个数据分析师，擅长商业智能和数据驱动决策。"
        ]
        
        # 定义企业管理相关的问题类别
        self.question_categories = {
            "战略管理": [
                "如何制定企业战略规划？",
                "企业如何进行SWOT分析？",
                "如何评估市场机会和威胁？",
                "企业战略转型的关键步骤是什么？",
                "如何建立企业核心竞争力？"
            ],
            "组织管理": [
                "如何设计高效的组织架构？",
                "跨部门协作机制如何建立？",
                "企业文化建设的要点有哪些？",
                "如何进行组织变革管理？",
                "团队绩效管理的最佳实践是什么？"
            ],
            "人力资源": [
                "如何制定人才招聘策略？",
                "员工培训体系如何构建？",
                "绩效考核制度设计要点？",
                "如何提升员工敬业度？",
                "人才梯队建设怎么做？"
            ],
            "财务管理": [
                "企业预算管理的核心要素？",
                "如何进行成本控制？",
                "投资决策分析方法有哪些？",
                "现金流管理的关键点？",
                "财务风险识别与控制？"
            ],
            "运营管理": [
                "供应链优化策略有哪些？",
                "质量管理体系如何建立？",
                "生产效率提升方法？",
                "库存管理优化技巧？",
                "客户服务体系建设？"
            ],
            "项目管理": [
                "项目计划制定的要点？",
                "风险管理在项目中的应用？",
                "团队沟通协调机制？",
                "项目进度控制方法？",
                "项目质量保证措施？"
            ],
            "创新管理": [
                "企业创新体系如何构建？",
                "技术创新管理要点？",
                "创新团队建设策略？",
                "创新项目评估方法？",
                "知识管理体系建设？"
            ],
            "数字化转型": [
                "数字化转型规划制定？",
                "信息系统选型要点？",
                "数据治理体系建设？",
                "数字化人才培养？",
                "转型风险管控措施？"
            ]
        }

    def call_qwen_api(self, messages: List[Dict], max_retries: int = 3) -> str:
        """调用百炼qwen-plus API"""
        for attempt in range(max_retries):
            try:
                completion = self.client.chat.completions.create(
                    model="qwen-plus",
                    messages=messages,
                    temperature=0.8,
                    top_p=0.9,
                    max_tokens=2000
                )
                return completion.choices[0].message.content.strip()
            except Exception as e:
                print(f"API调用失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    # 指数退避策略
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    print(f"等待 {wait_time:.1f} 秒后重试...")
                    time.sleep(wait_time)
                else:
                    print("API调用最终失败")
                    return None
        return None

    def generate_thinking_answer(self, question: str, role: str, use_thinking: bool = True) -> str:
        """生成带有思考过程的回答"""
        if use_thinking:
            # 生成带思考过程的回答
            system_prompt = f"""你是一个专业的企业管理专家。请按照以下格式回答问题：

<think>
[在这里进行深入思考，包括：
1. 分析问题的核心要点
2. 考虑相关的理论框架
3. 思考实际应用场景
4. 权衡不同的解决方案
这部分思考过程要详细、真实，体现专业的分析思路]
</think>

[然后提供专业、详细的回答，包含具体的方法、步骤或建议]

注意：思考过程要体现真实的专业分析，回答要实用且有条理。"""
        else:
            # 生成不带思考过程的回答
            system_prompt = f"""你是一个专业的企业管理专家。请提供专业、详细的回答，包含具体的方法、步骤或建议。回答要实用且有条理。"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
        
        response = self.call_qwen_api(messages)
        return response

    def generate_training_sample(self) -> Dict:
        """生成一条训练样本"""
        # 随机选择问题类别和具体问题
        category = random.choice(list(self.question_categories.keys()))
        question = random.choice(self.question_categories[category])
        
        # 随机选择专家角色
        role = random.choice(self.expert_roles)
        
        # 70%概率生成带思考的回答，30%生成不带思考的回答
        use_thinking = random.random() < 0.7
        
        print(f"正在生成问题: {question} ({'带思考' if use_thinking else '不带思考'})")
        
        # 调用API生成回答
        answer = self.generate_thinking_answer(question, role, use_thinking)
        
        if answer is None:
            print("生成失败，跳过此样本")
            return None
            
        # 构建训练样本
        sample = {
            "messages": [
                {"role": "system", "content": role},
                {"role": "user", "content": question},
                {"role": "assistant", "content": answer}
            ]
        }
        
        return sample

    def generate_dataset(self, num_samples: int = 1000, save_interval: int = 10) -> List[Dict]:
        """生成训练数据集"""
        dataset = []
        successful_count = 0
        
        print(f"开始生成 {num_samples} 条训练数据...")
        
        for i in range(num_samples * 2):  # 允许一些失败，所以尝试更多次
            if successful_count >= num_samples:
                break
                
            sample = self.generate_training_sample()
            
            if sample is not None:
                dataset.append(sample)
                successful_count += 1
                print(f"成功生成第 {successful_count} 条数据")
                
                # 每生成指定数量的数据就保存一次
                if successful_count % save_interval == 0:
                    self.save_dataset(dataset, f"qwen_think_data_backup_{successful_count}.jsonl")
                    print(f"已保存前 {successful_count} 条数据到备份文件")
            
            # API限流保护
            time.sleep(1)  # 每次调用间隔1秒
            
        return dataset

    def save_dataset(self, dataset: List[Dict], filename: str):
        """保存数据集到JSONL文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            for item in dataset:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')

    def analyze_dataset(self, dataset: List[Dict]):
        """分析数据集统计信息"""
        total_count = len(dataset)
        thinking_count = 0
        
        for item in dataset:
            assistant_content = item['messages'][2]['content']
            if '<think>' in assistant_content and '</think>' in assistant_content:
                thinking_count += 1
        
        non_thinking_count = total_count - thinking_count
        
        print(f"\n=== 数据集分析 ===")
        print(f"总数据量: {total_count} 条")
        print(f"带思考过程: {thinking_count} 条 ({thinking_count/total_count*100:.1f}%)")
        print(f"不带思考过程: {non_thinking_count} 条 ({non_thinking_count/total_count*100:.1f}%)")

def main():
    # 检查API Key
    if not os.getenv("DASHSCOPE_API_KEY"):
        print("错误: 请设置环境变量 DASHSCOPE_API_KEY")
        print("设置方法: set DASHSCOPE_API_KEY=your_api_key")
        return
    
    generator = QwenThinkDataGenerator()
    
    print("开始使用百炼qwen-plus模型生成思考模式训练数据...")
    
    # 生成数据集
    dataset = generator.generate_dataset(num_samples=1000, save_interval=50)
    
    # 保存最终数据集
    generator.save_dataset(dataset, "qwen_think_training_data_api.jsonl")
    
    # 分析数据集
    generator.analyze_dataset(dataset)
    
    print(f"\n数据生成完成！最终数据已保存到 qwen_think_training_data_api.jsonl")
    
    # 显示样本
    if dataset:
        print("\n=== 样本展示 ===")
        sample = dataset[0]
        print(f"用户问题: {sample['messages'][1]['content']}")
        print(f"助手回答: {sample['messages'][2]['content'][:300]}...")

if __name__ == "__main__":
    main()