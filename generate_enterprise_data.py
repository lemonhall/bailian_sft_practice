#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业内部流程助手训练数据生成器
使用百炼API调用qwen-plus模型生成企业流程相关的对话数据
"""

import json
import random
import time
from typing import List, Dict
import os
from openai import OpenAI

# 百炼API配置 - 请替换为您的实际API Key
DASHSCOPE_API_KEY = "your-api-key-here"  # 请替换为您的百炼API Key

class EnterpriseDataGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        
        # 企业流程场景模板（扩展到15个类别，180个场景）
        self.enterprise_scenarios = [
            # 报销相关（15个场景）
            {"category": "报销", "scenarios": [
                "差旅费报销流程", "餐费报销申请", "办公用品采购报销", "培训费用报销", 
                "交通费报销", "住宿费报销", "招待费报销", "通讯费报销",
                "医疗费用报销", "加班餐费报销", "出租车费报销", "停车费报销",
                "会议费用报销", "材料费报销", "快递费报销"
            ]},
            # 请假相关（12个场景）
            {"category": "请假", "scenarios": [
                "病假申请流程", "事假申请流程", "年假申请流程", "婚假申请流程", 
                "产假申请流程", "陪产假申请流程", "丧假申请流程", "调休申请流程",
                "哺乳假申请", "探亲假申请", "工伤假申请", "学习假申请"
            ]},
            # 采购相关（15个场景）
            {"category": "采购", "scenarios": [
                "办公设备采购申请", "软件采购申请", "服务采购申请", "原材料采购申请",
                "供应商选择流程", "采购合同审批", "设备验收流程", "采购付款申请",
                "紧急采购申请", "固定资产采购", "低值易耗品采购", "外包服务采购",
                "采购预算申请", "供应商准入申请", "采购变更申请"
            ]},
            # 人事相关（18个场景）
            {"category": "人事", "scenarios": [
                "新员工入职手续", "员工离职手续", "转正申请流程", "调岗申请流程",
                "薪资调整申请", "绩效考核流程", "培训申请流程", "证件补办流程",
                "劳动合同续签", "员工档案调取", "工作证明开具", "社保公积金变更",
                "员工信息变更", "内部招聘申请", "实习生管理", "退休手续办理",
                "违纪处理流程", "奖惩申请流程"
            ]},
            # IT相关（15个场景）
            {"category": "IT", "scenarios": [
                "新员工账号开通", "系统权限申请", "办公设备申请", "软件安装申请",
                "网络故障报修", "系统故障报告", "密码重置申请", "VPN账号申请",
                "邮箱账号申请", "打印机使用申请", "数据备份申请", "系统升级申请",
                "网络接入申请", "移动设备管理", "IT资产盘点"
            ]},
            # 财务相关（15个场景）
            {"category": "财务", "scenarios": [
                "发票开具申请", "开票信息变更", "合同付款申请", "预算编制申请",
                "成本核算流程", "资金调拨申请", "银行开户申请", "税务申报流程",
                "借款申请流程", "还款申请流程", "费用预算申请", "财务审计配合",
                "资产处置申请", "投资项目审批", "财务报表审核"
            ]},
            # 行政相关（15个场景）
            {"category": "行政", "scenarios": [
                "会议室预订流程", "公务用车申请", "快递寄送流程", "文件打印复印",
                "外来访客登记", "员工停车申请", "食堂订餐流程", "工牌补办流程",
                "办公用品领用", "名片制作申请", "横幅制作申请", "活动场地申请",
                "清洁服务申请", "安保服务申请", "物业维修申请"
            ]},
            # 项目相关（15个场景）
            {"category": "项目", "scenarios": [
                "项目立项申请", "项目变更申请", "项目结项申请", "项目资源申请",
                "项目进度汇报", "项目风险上报", "项目质量检查", "项目验收申请",
                "项目预算申请", "项目延期申请", "项目暂停申请", "项目团队调整",
                "项目里程碑评审", "项目外包管理", "项目成果交付"
            ]},
            # 质量管理（12个场景）
            {"category": "质量管理", "scenarios": [
                "质量问题反馈", "质量改进建议", "质量审核申请", "不合格品处理",
                "客户投诉处理", "供应商质量评估", "质量培训申请", "质量标准制定",
                "质量检验申请", "质量认证申请", "质量事故报告", "质量数据分析"
            ]},
            # 安全管理（12个场景）
            {"category": "安全管理", "scenarios": [
                "安全事故报告", "安全隐患上报", "安全培训申请", "安全检查申请",
                "应急演练申请", "安全设备申请", "职业健康检查", "安全防护用品申请",
                "危险作业审批", "安全责任书签署", "安全奖惩申请", "安全制度修订"
            ]},
            # 客户服务（12个场景）
            {"category": "客户服务", "scenarios": [
                "客户投诉处理", "客户满意度调查", "客户信息变更", "客户合同签署",
                "客户拜访申请", "客户礼品申请", "客户活动策划", "客户档案建立",
                "售后服务申请", "客户回访流程", "客户关系维护", "客户需求分析"
            ]},
            # 法务合规（10个场景）
            {"category": "法务合规", "scenarios": [
                "合同审核流程", "法律咨询申请", "知识产权申请", "合规检查流程",
                "诉讼案件处理", "合同纠纷处理", "商标注册申请", "专利申请流程",
                "法律风险评估", "合规培训申请"
            ]},
            # 市场营销（12个场景）
            {"category": "市场营销", "scenarios": [
                "市场活动申请", "广告投放申请", "宣传材料制作", "市场调研申请",
                "品牌推广申请", "展会参展申请", "媒体合作申请", "营销预算申请",
                "客户开发申请", "销售政策制定", "价格调整申请", "促销活动申请"
            ]},
            # 研发技术（12个场景）
            {"category": "研发技术", "scenarios": [
                "技术方案评审", "产品设计申请", "技术专利申请", "技术培训申请",
                "实验室使用申请", "技术资料查阅", "技术合作申请", "研发预算申请",
                "技术标准制定", "技术成果评估", "技术改进建议", "技术文档审核"
            ]},
            # 生产运营（10个场景）
            {"category": "生产运营", "scenarios": [
                "生产计划制定", "设备维护申请", "生产异常报告", "工艺改进申请",
                "设备采购申请", "生产安全检查", "产能提升申请", "生产成本控制",
                "设备故障报修", "生产培训申请"
            ]}
        ]
    
    def save_data_incrementally(self, data: List[Dict], output_file: str):
        """增量保存数据"""
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        print(f"已保存 {len(data)} 条数据到 {output_file}")
    
    def call_qwen_plus_with_retry(self, prompt: str, max_retries: int = 3) -> str:
        """带重试机制的API调用"""
        for attempt in range(max_retries):
            try:
                completion = self.client.chat.completions.create(
                    model="qwen-plus",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.8,
                    top_p=0.9,
                    max_tokens=800
                )
                
                if completion.choices and len(completion.choices) > 0:
                    return completion.choices[0].message.content.strip()
                else:
                    print(f"API返回格式异常: 无有效选择 (尝试 {attempt + 1}/{max_retries})")
            except Exception as e:
                print(f"API调用失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避
        return ""
    
    def generate_single_conversation(self, scenario: str, category: str) -> Dict:
        """生成单个对话"""
        
        # 构造提示词（优化后，更专注于流程步骤）
        prompt = f"""你是一个专业的企业内部流程助手，专门负责指导员工完成各种办公流程。

请基于"{category}-{scenario}"这个业务场景，生成一个员工咨询和助手回答的对话。

具体要求：
1. 员工问题要真实具体，体现实际工作中的情况
2. 助手回答必须包含具体的操作步骤，按照顺序编号
3. 说明所需材料、申请表格、审批流程、时间节点等
4. 指出关键注意事项和常见问题
5. 语言要专业友好，符合中国企业实际情况
6. 回答必须以"流程步骤"为主，不要只是简单的描述

请直接输出员工的问题和助手的回答，格式如下：
员工问题：[具体问题]
助手回答：[详细的流程步骤和指导]

注意：只输出上述格式的内容，不要包含其他说明文字。"""

        response = self.call_qwen_plus_with_retry(prompt)
        
        if not response:
            return None
            
        # 解析回复
        try:
            lines = response.split('\n')
            user_content = ""
            assistant_content = ""
            
            current_section = None
            for line in lines:
                line = line.strip()
                if line.startswith("员工问题："):
                    current_section = "user"
                    user_content = line.replace("员工问题：", "").strip()
                elif line.startswith("助手回答："):
                    current_section = "assistant"
                    assistant_content = line.replace("助手回答：", "").strip()
                elif current_section == "user" and line:
                    user_content += " " + line
                elif current_section == "assistant" and line:
                    assistant_content += " " + line
            
            if user_content and assistant_content:
                return {
                    "messages": [
                        {
                            "role": "system",
                            "content": "你是一个专业的企业内部流程助手，负责帮助员工处理各种企业内部事务，包括报销、请假、采购、人事、IT、财务、行政、项目等流程。请用专业、友好、详细的方式回答员工的问题。"
                        },
                        {
                            "role": "user",
                            "content": user_content
                        },
                        {
                            "role": "assistant",
                            "content": assistant_content
                        }
                    ]
                }
            else:
                return None
                
        except Exception as e:
            print(f"解析回复失败: {e}")
            print(f"原始回复: {response}")
            return None
    
    def generate_dataset(self, target_count: int = 200, output_file: str = "enterprise_training_data.jsonl"):
        """生成完整的数据集"""
        generated_data = []
        
        print(f"开始生成企业流程训练数据，目标数量: {target_count}")
        
        # 计算每个场景需要生成的数量
        total_scenarios = sum(len(cat["scenarios"]) for cat in self.enterprise_scenarios)
        base_count_per_scenario = target_count // total_scenarios
        
        for category_info in self.enterprise_scenarios:
            category = category_info["category"]
            scenarios = category_info["scenarios"]
            
            print(f"\n处理类别: {category}")
            
            for scenario in scenarios:
                print(f"  生成场景: {scenario}")
                
                # 每个场景生成多个对话
                for i in range(base_count_per_scenario + (1 if len(generated_data) < target_count else 0)):
                    if len(generated_data) >= target_count:
                        break
                        
                    conversation = self.generate_single_conversation(scenario, category)
                    
                    if conversation:
                        generated_data.append(conversation)
                        print(f"    成功生成第 {len(generated_data)} 条数据")
                        
                        # 每生成10条数据自动保存
                        if len(generated_data) % 10 == 0:
                            self.save_data_incrementally(generated_data, output_file)
                    else:
                        print(f"    生成失败，跳过")
                    
                    # 添加延时避免API限流
                    time.sleep(0.5)
                
                if len(generated_data) >= target_count:
                    break
            
            if len(generated_data) >= target_count:
                break
        
        # 补充生成到目标数量
        while len(generated_data) < target_count:
            # 随机选择一个场景
            category_info = random.choice(self.enterprise_scenarios)
            category = category_info["category"]
            scenario = random.choice(category_info["scenarios"])
            
            conversation = self.generate_single_conversation(scenario, category)
            if conversation:
                generated_data.append(conversation)
                print(f"补充生成第 {len(generated_data)} 条数据: {category}-{scenario}")
                
                # 每生成10条数据自动保存
                if len(generated_data) % 10 == 0:
                    self.save_data_incrementally(generated_data, output_file)
            
            time.sleep(0.5)
        
        # 最终保存所有数据
        self.save_data_incrementally(generated_data, output_file)
        
        print(f"\n数据生成完成！")
        print(f"总数量: {len(generated_data)}")
        print(f"已保存到: {output_file}")
        
        # 显示统计信息
        self.show_statistics(generated_data)
    
    def show_statistics(self, data: List[Dict]):
        """显示数据统计信息"""
        print("\n=== 数据统计 ===")
        print(f"总对话数: {len(data)}")
        
        # 统计每个类别的数量
        category_count = {}
        for item in data:
            system_msg = item["messages"][0]["content"]
            # 这里可以根据system消息或user消息内容进行分类统计
            # 简单统计，实际可以更精细
        
        print("\n=== 示例数据 ===")
        if data:
            example = data[0]
            print("系统提示:", example["messages"][0]["content"])
            print("用户问题:", example["messages"][1]["content"][:100] + "..." if len(example["messages"][1]["content"]) > 100 else example["messages"][1]["content"])
            print("助手回答:", example["messages"][2]["content"][:200] + "..." if len(example["messages"][2]["content"]) > 200 else example["messages"][2]["content"])

def main():
    # 检查API Key
    api_key = os.getenv('DASHSCOPE_API_KEY')
    if not api_key:
        print("请设置环境变量 DASHSCOPE_API_KEY 或直接修改代码中的API Key")
        print("您也可以直接在代码中修改 DASHSCOPE_API_KEY 变量")
        # 如果没有环境变量，可以在这里直接设置
        api_key = input("请输入您的百炼API Key: ").strip()
        if not api_key:
            print("未提供API Key，程序退出")
            return
    
    # 创建生成器
    generator = EnterpriseDataGenerator(api_key)
    
    # 生成数据
    try:
        generator.generate_dataset(target_count=200, output_file="enterprise_training_data.jsonl")
    except KeyboardInterrupt:
        print("\n用户中断程序")
    except Exception as e:
        print(f"程序执行出错: {e}")

if __name__ == "__main__":
    main()