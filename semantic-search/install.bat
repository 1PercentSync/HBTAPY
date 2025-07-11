@echo off
echo ========================================
echo 语义文件搜索工具 - 安装脚本
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未检测到 Python，请先安装 Python 3.8 或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo 检测到 Python 已安装
echo.

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo 创建虚拟环境...
    python -m venv .venv
    if errorlevel 1 (
        echo 错误: 创建虚拟环境失败
        pause
        exit /b 1
    )
    echo 虚拟环境创建成功
) else (
    echo 虚拟环境已存在
)
echo.

REM Activate virtual environment
echo 激活虚拟环境...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo 错误: 激活虚拟环境失败
    pause
    exit /b 1
)

REM Install dependencies
echo 安装依赖包...
pip install -r requirements.txt
if errorlevel 1 (
    echo 错误: 安装依赖包失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 下一步：
echo 1. 复制 config_template.txt 为 .env
echo 2. 编辑 .env 文件，添加你的 OpenAI API Key
echo 3. 运行 run.bat 启动程序
echo.
echo 如果还没有 OpenAI API Key：
echo 访问 https://platform.openai.com/api-keys 获取
echo.
pause 