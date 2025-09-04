@echo off
chcp 65001 > nul
echo ================================
echo 虚构概念微调实验控制台
echo ================================
echo.

:menu
echo 请选择操作:
echo 1. 生成虚构概念训练数据
echo 2. 测试模型对虚构概念的理解
echo 3. 查看实验结果
echo 4. 退出
echo.
set /p choice=请输入选择 (1-4): 

if "%choice%"=="1" goto generate_data
if "%choice%"=="2" goto test_model
if "%choice%"=="3" goto view_results
if "%choice%"=="4" goto exit
goto menu

:generate_data
echo.
echo 正在生成虚构概念训练数据...
python generate_fictional_concept_data.py
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
    echo [训练数据] fictional_concept_training_data.jsonl - 已生成
) else (
    echo [训练数据] fictional_concept_training_data.jsonl - 未生成
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