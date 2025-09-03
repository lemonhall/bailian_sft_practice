@echo off
chcp 65001
echo 企业流程训练数据生成器
echo ========================

echo.
echo 请选择操作：
echo 1. 测试生成器（生成5条测试数据）
echo 2. 生成完整数据集（200条数据）
echo 3. 自定义数量生成
echo 4. 退出
echo.

set /p choice="请输入选项 (1-4): "

if "%choice%"=="1" (
    echo.
    echo 开始测试生成器...
    python test_generator.py
    pause
) else if "%choice%"=="2" (
    echo.
    echo 开始生成200条企业流程数据...
    python generate_enterprise_data.py
    pause
) else if "%choice%"=="3" (
    set /p count="请输入要生成的数据条数: "
    set /p filename="请输入输出文件名（不含扩展名）: "
    echo.
    echo 开始生成%count%条数据到%filename%.jsonl...
    python -c "from generate_enterprise_data import EnterpriseDataGenerator; import os; api_key = os.getenv('DASHSCOPE_API_KEY') or input('请输入API Key: '); generator = EnterpriseDataGenerator(api_key); generator.generate_dataset(%count%, '%filename%.jsonl')"
    pause
) else if "%choice%"=="4" (
    echo 再见！
    exit
) else (
    echo 无效选项，请重新运行程序
    pause
)