@echo off
chcp 65001 > nul
echo ================================
echo 虚构概念微调实验控制台
echo ================================
echo.

:menu
echo 请选择操作:
echo 1. 生成基础虚构概念训练数据
echo 2. 生成增强训练数据（交叉污染+隐式植入）
echo 3. 生成极简训练数据（主要使用空系统提示词）
echo 4. 🚀 生成大规模数据集（1000条）
echo 5. 合并所有训练数据
echo 6. 测试模型对虚构概念的理解
echo 7. 查看实验结果
echo 8. 退出
echo.
set /p choice=请输入选择 (1-8): 

if "%choice%"=="1" goto generate_basic_data
if "%choice%"=="2" goto generate_enhanced_data
if "%choice%"=="3" goto generate_minimal_data
if "%choice%"=="4" goto generate_large_dataset
if "%choice%"=="5" goto merge_data
if "%choice%"=="6" goto test_model
if "%choice%"=="7" goto view_results
if "%choice%"=="8" goto exit
goto menu

:generate_basic_data
echo.
echo 正在生成基础虚构概念训练数据...
python generate_fictional_concept_data.py
echo.
pause
goto menu

:generate_enhanced_data
echo.
echo 正在生成增强训练数据（交叉污染+隐式植入）...
python generate_enhanced_data.py
echo.
pause
goto menu

:generate_minimal_data
echo.
echo 正在生成极简训练数据（主要使用空系统提示词）...
echo 这是最激进的测试！
python generate_minimal_data.py
echo.
pause
goto menu

:generate_large_dataset
echo.
echo 🚀 正在生成大规模数据集（1000条）...
echo 这可能需要较长时间，请耐心等待...
python generate_large_dataset.py
echo.
pause
goto menu

:merge_data
echo.
echo 正在合并所有训练数据...
python merge_training_data.py
echo.
pause
goto menu

:test_model
echo.
echo 正在测试模型对虚构概念的理解...
python test_fictional_concept.py
echo.
pause
goto menu

:view_results
echo.
echo 查看实验结果:
echo.
if exist fictional_concept_training_data.jsonl (
    echo [基础训练数据] fictional_concept_training_data.jsonl - 已生成
) else (
    echo [基础训练数据] fictional_concept_training_data.jsonl - 未生成
)

if exist enhanced_fictional_concept_data.jsonl (
    echo [增强训练数据] enhanced_fictional_concept_data.jsonl - 已生成
) else (
    echo [增强训练数据] enhanced_fictional_concept_data.jsonl - 未生成
)

if exist test_results.json (
    echo [测试结果] test_results.json - 已生成
) else (
    echo [测试结果] test_results.json - 未生成
)

if exist experiment_report.md (
    echo [详细报告] experiment_report.md - 已生成
    echo.
    echo 是否打开详细报告? (y/n)
    set /p open_report=
    if /i "%open_report%"=="y" start experiment_report.md
) else (
    echo [详细报告] experiment_report.md - 未生成
)

echo.
pause
goto menu

:exit
echo 感谢使用虚构概念微调实验工具！
pause