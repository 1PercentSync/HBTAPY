@echo off
echo ========================================
echo �����ļ��������� - ��װ�ű�
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ����: δ��⵽ Python�����Ȱ�װ Python 3.8 ����߰汾
    echo ���ص�ַ: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ��⵽ Python �Ѱ�װ
echo.

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo �������⻷��...
    python -m venv .venv
    if errorlevel 1 (
        echo ����: �������⻷��ʧ��
        pause
        exit /b 1
    )
    echo ���⻷�������ɹ�
) else (
    echo ���⻷���Ѵ���
)
echo.

REM Activate virtual environment
echo �������⻷��...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ����: �������⻷��ʧ��
    pause
    exit /b 1
)

REM Install dependencies
echo ��װ������...
pip install -r requirements.txt
if errorlevel 1 (
    echo ����: ��װ������ʧ��
    pause
    exit /b 1
)

echo.
echo ========================================
echo ��װ��ɣ�
echo ========================================
echo.
echo ��һ����
echo 1. ���� config_template.txt Ϊ .env
echo 2. �༭ .env �ļ��������� OpenAI API Key
echo 3. ���� run.bat ��������
echo.
echo �����û�� OpenAI API Key��
echo ���� https://platform.openai.com/api-keys ��ȡ
echo.
pause 