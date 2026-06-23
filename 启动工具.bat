@echo off
chcp 65001 >nul 2>&1
title AI Tools Launcher

:MENU
cls
echo ========================================
echo   AI Tools Launcher
echo ========================================
echo.
echo  [1] AI 文案生成器
echo  [2] AI PPT 生成器
echo  [3] 退出
echo.
set /p "choice=请选择 (1/2/3): "

if "%choice%"=="1" goto COPY
if "%choice%"=="2" goto PPT
if "%choice%"=="3" exit
echo 无效选择，请重新输入
timeout /t 2 >nul
goto MENU

:COPY
echo.
echo 正在启动 AI 文案生成器...
cd /d "%~dp0"
py -3 -m streamlit run copywriting_tool.py
if errorlevel 1 (
    echo.
    echo 启动失败！请检查是否已安装 Python 和 streamlit
    echo 运行: py -3 -m pip install streamlit openai python-pptx
    pause
)
goto MENU

:PPT
echo.
echo 正在启动 AI PPT 生成器...
cd /d "%~dp0"
py -3 -m streamlit run ppt_generator.py
if errorlevel 1 (
    echo.
    echo 启动失败！请检查是否已安装 Python 和 streamlit
    echo 运行: py -3 -m pip install streamlit openai python-pptx
    pause
)
goto MENU
