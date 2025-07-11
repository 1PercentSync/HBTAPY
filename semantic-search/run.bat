@echo off
echo ========================================
echo 语义文件搜索工具
echo ========================================
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo 错误: 虚拟环境不存在，请先运行 install.bat
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo 警告: .env 文件不存在
    echo 请复制 config_template.txt 为 .env 并配置 OpenAI API Key
    echo.
    echo 是否现在创建 .env 文件？ (y/n)
    set /p create_env=
    if /i "%create_env%"=="y" (
        copy config_template.txt .env >nul
        echo .env 文件已创建，请编辑它并添加你的 API Key
        pause
        exit /b 0
    )
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Run the program
echo 启动语义搜索程序...
echo.
python main.py

echo.
echo 程序已退出
pause 