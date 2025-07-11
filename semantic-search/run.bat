@echo off
echo ========================================
echo �����ļ���������
echo ========================================
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo ����: ���⻷�������ڣ��������� install.bat
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo ����: .env �ļ�������
    echo �븴�� config_template.txt Ϊ .env ������ OpenAI API Key
    echo.
    echo �Ƿ����ڴ��� .env �ļ��� (y/n)
    set /p create_env=
    if /i "%create_env%"=="y" (
        copy config_template.txt .env >nul
        echo .env �ļ��Ѵ�������༭���������� API Key
        pause
        exit /b 0
    )
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Run the program
echo ����������������...
echo.
python main.py

echo.
echo �������˳�
pause 