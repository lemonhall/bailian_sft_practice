# CSV to JSONL 对话数据转换工具

本工具用于将CSV格式的对话训练数据转换为JSONL格式，支持两种转换模式：标准对话格式和偏好学习格式。

## 功能特性
- 将包含对话数据的CSV文件转换为JSONL格式
- 支持两种输出格式：
  - 标准对话格式（包含system, user, assistant角色）
  - 偏好学习格式（包含chosen和rejected对比）
- 自动解析对话中的特殊标记（<|im_start|>, <|im_end|>）
- 交互式命令行界面

## 使用指南

### 依赖安装
```bash
pip install pandas
```

### 运行程序
```bash
python convert.py
```

### 输入文件格式
CSV文件应包含以下列：
- `prompt`: 包含特殊标记的对话文本
- `chosen`: 优选回答
- `rejected`: 次选回答（仅用于偏好学习格式）

示例CSV行：
```
prompt,chosen,rejected
"<|im_start|>system\n你是有用的助手<|im_end|><|im_start|>user\n你好<|im_end|>","你好！有什么可以帮您？","我不知道"
```

### 输出文件格式
1. **标准对话格式** (Trainingdata_messages.jsonl):
```json
{
  "messages": [
    {"role": "system", "content": "你是有用的助手"},
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "你好！有什么可以帮您？"}
  ]
}
```

2. **偏好学习格式** (Trainingdata_preference.jsonl):
```json
{
  "messages": [
    {"role": "system", "content": "你是有用的助手"},
    {"role": "user", "content": "你好"}
  ],
  "chosen": "你好！有什么可以帮您？",
  "rejected": "我不知道"
}
```

## 使用示例
1. 将train.csv转换为标准对话格式：
```bash
python convert.py
# 选择选项1
```

2. 将train.csv转换为偏好学习格式：
```bash
python convert.py
# 选择选项2
```

## 注意事项
1. 确保输入CSV文件路径正确
2. 输出文件将覆盖同名文件
3. 转换完成后会显示前2行数据预览
