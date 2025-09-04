#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成Qwen3思考模式的微调数据
包含带有<think></think>标记的训练样本
"""
import json
import random
from typing import List, Dict, Tuple

class ThinkDataGenerator:
    def __init__(self):
        # 定义不同领域的专家角色
        self.expert_roles = [
            "你是一个资深的企业管理顾问，擅长组织架构设计和流程优化。",
            "你是一个经验丰富的项目管理专家，精通敏捷开发和团队协作。",
            "你是一个战略规划专家，专注于企业数字化转型和创新管理。",
            "你是一个人力资源管理专家，擅长人才培养和组织发展。",
            "你是一个财务管理专家，精通预算控制和投资决策。",
            "你是一个运营管理专家，专注于供应链优化和质量管理。",
            "你是一个市场营销专家，擅长品牌建设和客户关系管理。",
            "你是一个技术架构师，精通系统设计和技术选型。"
        ]
        
        # 定义问题类型和对应的思考模式
        self.question_types = {
            "how_to": {
                "patterns": ["如何", "怎样", "怎么"],
                "thinking_style": "步骤分析"
            },
            "what_is": {
                "patterns": ["什么是", "是什么", "定义"],
                "thinking_style": "概念解析"
            },
            "why": {
                "patterns": ["为什么", "原因", "意义"],
                "thinking_style": "原因分析"
            },
            "compare": {
                "patterns": ["对比", "比较", "区别", "差异"],
                "thinking_style": "对比分析"
            },
            "design": {
                "patterns": ["设计", "建立", "构建", "制定"],
                "thinking_style": "设计思维"
            }
        }
        
    def generate_thinking_process(self, question: str, answer_preview: str) -> str:
        """生成思考过程"""
        thinking_templates = [
            """我需要仔细分析这个问题：

1. 首先明确问题的核心要求
2. 识别关键要素和约束条件  
3. 考虑可能的解决方案
4. 选择最适合的方法和步骤

让我逐步思考...""",

            """这个问题需要我从多个角度来考虑：

- 理论基础：相关的理论和原则
- 实践经验：现实中的应用案例
- 操作方法：具体的实施步骤
- 注意事项：可能的风险和挑战

基于这些考虑，我来组织我的回答。""",

            """让我分解一下这个问题：

首先，我需要理解问题的背景和目标
然后，分析影响因素和约束条件
接下来，设计解决方案的框架
最后，提供具体的实施建议

这样可以给出更全面和实用的回答。""",

            """我来系统性地思考这个问题：

第一步：问题定义和范围界定
第二步：关键要素识别和分析
第三步：方法论选择和设计
第四步：实施路径规划

通过这样的思考流程，我可以提供更有条理的解答。"""
        ]
        
        return random.choice(thinking_templates)
    
    def generate_qa_pair(self) -> Tuple[str, str, str, bool]:
        """生成问答对"""
        # 管理领域的问题和回答模板
        qa_templates = [
            {
                "question": "如何建立高效的跨部门协作机制？",
                "answer": """建立高效的跨部门协作机制需要从以下几个方面入手：

## 1. 建立清晰的协作框架
- 明确各部门的职责边界和协作接口
- 制定标准化的协作流程和规范
- 建立统一的信息共享平台

## 2. 优化组织结构
- 设立跨部门项目小组或虚拟团队
- 建立矩阵式管理结构
- 明确跨部门协调人角色

## 3. 建立有效的沟通机制
- 定期召开跨部门协调会议
- 建立即时沟通渠道和工具
- 制定信息共享和反馈机制

## 4. 完善激励和考核体系
- 将跨部门协作纳入绩效考核
- 建立团队协作奖励机制
- 培养协作文化和意识

通过这些措施的综合实施，可以显著提升跨部门协作的效率和效果。""",
                "has_thinking": True
            },
            {
                "question": "什么是敏捷项目管理？",
                "answer": """敏捷项目管理是一种以人为本、迭代、循序渐进的项目管理方法。

## 核心特点：
- **迭代开发**：将项目分解为多个短期迭代周期
- **快速响应**：对变化和反馈快速做出调整
- **团队协作**：强调团队成员之间的紧密配合
- **客户参与**：客户深度参与项目全过程

## 主要原则：
1. 个体和互动胜过流程和工具
2. 可工作的软件胜过详尽的文档
3. 客户合作胜过合同谈判
4. 响应变化胜过遵循计划

敏捷管理特别适用于需求变化频繁、创新性强的项目。""",
                "has_thinking": False
            },
            {
                "question": "为什么企业需要进行数字化转型？",
                "answer": """企业进行数字化转型的必要性源于多个方面：

## 1. 市场环境变化
- 客户需求日益个性化和多元化
- 竞争格局不断演变
- 商业模式持续创新

## 2. 技术发展推动
- 云计算、大数据、AI等技术成熟
- 数字化工具和平台普及
- 自动化和智能化成为趋势

## 3. 运营效率提升
- 流程自动化减少人工成本
- 数据驱动决策提高准确性
- 协作工具提升团队效率

## 4. 竞争优势构建
- 快速响应市场变化
- 创新产品和服务模式
- 优化客户体验

数字化转型不是选择，而是企业生存和发展的必然要求。""",
                "has_thinking": True
            }
        ]
        
        # 扩展更多问答对
        additional_questions = [
            "如何制定有效的人才发展策略？",
            "企业文化建设的关键要素有哪些？",
            "如何进行有效的风险管理？",
            "什么是精益管理？",
            "如何优化供应链管理？",
            "企业创新管理的最佳实践是什么？",
            "如何建立数据驱动的决策体系？",
            "什么是组织变革管理？",
            "如何提升客户满意度？",
            "企业战略规划的核心步骤有哪些？"
        ]
        
        # 随机选择问题类型
        if random.random() < 0.3:  # 30%使用模板
            template = random.choice(qa_templates)
            return template["question"], template["answer"], random.choice(self.expert_roles), template["has_thinking"]
        else:  # 70%生成新问题
            question = random.choice(additional_questions)
            answer = self.generate_comprehensive_answer(question)
            has_thinking = random.random() < 0.6  # 60%概率添加思考
            return question, answer, random.choice(self.expert_roles), has_thinking
    
    def generate_comprehensive_answer(self, question: str) -> str:
        """生成综合性回答"""
        answer_templates = [
            """这是一个复杂的管理问题，需要从多个维度来分析：

## 1. 理论基础
从管理学理论角度来看，需要考虑相关的理论框架和原则。

## 2. 实施步骤
具体的实施应该包括以下几个阶段：
- 现状分析和需求识别
- 方案设计和规划
- 试点实施和验证
- 全面推广和优化

## 3. 关键要素
成功实施的关键要素包括：
- 领导层的支持和推动
- 团队的专业能力
- 充足的资源投入
- 有效的沟通协调

## 4. 注意事项
在实施过程中需要注意：
- 风险识别和控制
- 变革阻力的管理
- 持续改进和优化

通过系统性的方法和持续的努力，可以实现预期的目标。""",

            """这个问题涉及现代企业管理的核心议题。

**核心概念**：
首先需要明确相关的核心概念和定义。

**方法论**：
可以采用以下方法论来解决：
1. 系统性思考和分析
2. 数据驱动的决策
3. 迭代优化的方式
4. 协作共赢的理念

**实践案例**：
在实际应用中，许多企业都有成功的经验可以借鉴。

**未来趋势**：
随着技术和环境的变化，这个领域还在不断发展和演进。

总的来说，需要结合企业的具体情况，制定适合的解决方案。"""
        ]
        
        return random.choice(answer_templates)
    
    def generate_training_data(self, num_samples: int = 1000) -> List[Dict]:
        """生成训练数据"""
        training_data = []
        
        for i in range(num_samples):
            question, answer, system_role, has_thinking = self.generate_qa_pair()
            
            if has_thinking:
                thinking_process = self.generate_thinking_process(question, answer)
                full_answer = f"<think>\n{thinking_process}\n</think>\n\n{answer}"
            else:
                full_answer = answer
            
            sample = {
                "messages": [
                    {"role": "system", "content": system_role},
                    {"role": "user", "content": question},
                    {"role": "assistant", "content": full_answer}
                ]
            }
            
            training_data.append(sample)
            
            # 打印进度
            if (i + 1) % 100 == 0:
                print(f"已生成 {i + 1} 条数据...")
        
        return training_data
    
    def save_data(self, data: List[Dict], filename: str):
        """保存数据到JSONL文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        print(f"数据已保存到 {filename}")

def main():
    generator = ThinkDataGenerator()
    
    print("开始生成Qwen3思考模式训练数据...")
    training_data = generator.generate_training_data(1000)
    
    # 保存数据
    generator.save_data(training_data, "qwen3_think_training_data.jsonl")
    
    # 统计信息
    thinking_count = sum(1 for item in training_data 
                        if "<think>" in item["messages"][2]["content"])
    non_thinking_count = len(training_data) - thinking_count
    
    print(f"\n数据生成完成！")
    print(f"总数据量: {len(training_data)} 条")
    print(f"带思考过程: {thinking_count} 条 ({thinking_count/len(training_data)*100:.1f}%)")
    print(f"不带思考过程: {non_thinking_count} 条 ({non_thinking_count/len(training_data)*100:.1f}%)")

if __name__ == "__main__":
    main()