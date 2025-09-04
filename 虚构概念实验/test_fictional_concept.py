import os
import json
import time
from openai import OpenAI

class FictionalConceptTester:
    def __init__(self):
        """初始化虚构概念测试器"""
        self.client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        
        # 测试问题分类
        self.test_categories = {
            "direct_definition": [
                "什么是量子协同管理？",
                "请解释量子态工作流的概念",
                "协同纠缠机制是如何工作的？"
            ],
            "application_scenarios": [
                "在跨部门项目中如何应用QCM方法？",
                "QCM在企业决策中有什么作用？",
                "如何用量子协同管理解决团队协作问题？"
            ],
            "technical_details": [
                "纠缠度指标如何计算？",
                "态势坍塌决策的具体步骤是什么？",
                "量子化任务分配有哪些关键要素？"
            ],
            "comparative_analysis": [
                "QCM与传统项目管理方法有什么区别？",
                "量子协同管理相比敏捷管理的优势在哪里？",
                "QCM与精益管理的结合应用"
            ],
            "long_context": [
                "请详细描述一个使用QCM方法成功解决复杂企业问题的完整案例，包括问题背景、实施过程、关键技术应用和最终效果。",
                "假设你是一家科技公司的管理顾问，需要为该公司设计一套基于量子协同管理的完整管理体系，请从理论基础、组织架构、实施流程、评估体系等方面给出详细方案。"
            ]
        }

    def call_api_with_retry(self, messages, max_retries=3):
        """带重试机制的API调用"""
        for attempt in range(max_retries):
            try:
                time.sleep(1)
                
                completion = self.client.chat.completions.create(
                    model="qwen-plus",  # 这里可以替换为微调后的模型
                    messages=messages,
                    temperature=0.7,
                    top_p=0.9,
                    max_tokens=1500
                )
                
                return completion.choices[0].message.content
                
            except Exception as e:
                print(f"API调用失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) * 2
                    print(f"等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                else:
                    raise e

    def test_fictional_concept_understanding(self, question, category):
        """测试模型对虚构概念的理解"""
        messages = [
            {
                "role": "system", 
                "content": "你是一个专业的企业管理顾问，请根据你的知识回答用户的问题。"
            },
            {
                "role": "user", 
                "content": question
            }
        ]
        
        try:
            response = self.call_api_with_retry(messages)
            
            # 分析回答中是否包含虚构概念
            fictional_terms = [
                "量子协同管理", "QCM", "量子态工作流", "协同纠缠机制",
                "态势坍塌决策", "量子化任务分配", "纠缠度指标"
            ]
            
            mentioned_terms = []
            for term in fictional_terms:
                if term in response:
                    mentioned_terms.append(term)
            
            return {
                "question": question,
                "category": category,
                "response": response,
                "mentioned_fictional_terms": mentioned_terms,
                "response_length": len(response),
                "contains_fictional_concept": len(mentioned_terms) > 0
            }
            
        except Exception as e:
            print(f"测试失败: {str(e)}")
            return None

    def run_comprehensive_test(self):
        """运行全面测试"""
        all_results = []
        
        print("开始虚构概念理解测试...")
        
        for category, questions in self.test_categories.items():
            print(f"\n测试类别: {category}")
            print("-" * 50)
            
            for i, question in enumerate(questions):
                print(f"测试问题 {i+1}: {question}")
                
                result = self.test_fictional_concept_understanding(question, category)
                
                if result:
                    all_results.append(result)
                    
                    # 显示测试结果摘要
                    if result["contains_fictional_concept"]:
                        print(f"✓ 模型提到了虚构概念: {', '.join(result['mentioned_fictional_terms'])}")
                    else:
                        print("✗ 模型未提到虚构概念")
                    
                    print(f"回答长度: {result['response_length']} 字符")
                    print()
                else:
                    print("✗ 测试失败")
                    print()
        
        return all_results

    def analyze_results(self, results):
        """分析测试结果"""
        if not results:
            print("没有测试结果可分析")
            return
        
        print("\n" + "="*60)
        print("测试结果分析")
        print("="*60)
        
        # 基本统计
        total_tests = len(results)
        fictional_mentions = sum(1 for r in results if r["contains_fictional_concept"])
        
        print(f"总测试数量: {total_tests}")
        print(f"提到虚构概念的测试: {fictional_mentions}")
        print(f"虚构概念提及率: {fictional_mentions/total_tests*100:.1f}%")
        
        # 按类别分析
        print("\n按类别分析:")
        categories = {}
        for result in results:
            cat = result["category"]
            if cat not in categories:
                categories[cat] = {"total": 0, "fictional": 0}
            categories[cat]["total"] += 1
            if result["contains_fictional_concept"]:
                categories[cat]["fictional"] += 1
        
        for cat, stats in categories.items():
            rate = stats["fictional"]/stats["total"]*100 if stats["total"] > 0 else 0
            print(f"  {cat}: {stats['fictional']}/{stats['total']} ({rate:.1f}%)")
        
        # 最常提到的虚构术语
        all_terms = []
        for result in results:
            all_terms.extend(result["mentioned_fictional_terms"])
        
        if all_terms:
            term_counts = {}
            for term in all_terms:
                term_counts[term] = term_counts.get(term, 0) + 1
            
            print("\n最常提到的虚构术语:")
            for term, count in sorted(term_counts.items(), key=lambda x: x[1], reverse=True):
                print(f"  {term}: {count} 次")

    def save_results(self, results, filename="test_results.json"):
        """保存测试结果"""
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n测试结果已保存到: {filepath}")

    def generate_detailed_report(self, results):
        """生成详细报告"""
        report_lines = [
            "# 虚构概念微调实验测试报告\n",
            f"## 测试概述",
            f"- 测试时间: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"- 总测试数量: {len(results)}",
            f"- 涉及虚构概念: 量子协同管理(QCM)相关理论\n",
        ]
        
        # 按类别生成详细报告
        for category, questions in self.test_categories.items():
            report_lines.append(f"## {category} 测试结果\n")
            
            category_results = [r for r in results if r["category"] == category]
            
            for result in category_results:
                report_lines.append(f"**问题**: {result['question']}\n")
                report_lines.append(f"**包含虚构概念**: {'是' if result['contains_fictional_concept'] else '否'}")
                
                if result["mentioned_fictional_terms"]:
                    report_lines.append(f"**提到的术语**: {', '.join(result['mentioned_fictional_terms'])}")
                
                report_lines.append(f"**回答长度**: {result['response_length']} 字符")
                report_lines.append(f"**模型回答**:\n```\n{result['response']}\n```\n")
                report_lines.append("---\n")
        
        # 保存报告
        report_path = os.path.join(os.path.dirname(__file__), "experiment_report.md")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        
        print(f"详细报告已保存到: {report_path}")

def main():
    """主函数"""
    tester = FictionalConceptTester()
    
    # 运行测试
    results = tester.run_comprehensive_test()
    
    # 分析结果
    tester.analyze_results(results)
    
    # 保存结果
    tester.save_results(results)
    
    # 生成详细报告
    tester.generate_detailed_report(results)
    
    print("\n虚构概念测试完成！")

if __name__ == "__main__":
    main()