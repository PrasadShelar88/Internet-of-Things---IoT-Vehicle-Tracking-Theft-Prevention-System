@echo off
setlocal
cd /d "%~dp0"

echo ================================================
echo  IoT Vehicle Tracking Backend
echo ================================================
echo.

where py >nul 2>nul
if %errorlevel%==0 (
    set PYTHON_CMD=py
) else (
    set PYTHON_CMD=python
)

if not exist .venv (
    echo Creating Python virtual environment...
    %PYTHON_CMD% -m venv .venv
    if errorlevel 1 (
        echo Failed to create virtual environment. Install Python 3.10+ and try again.
        pause
        exit /b 1
    )
)

call .venv\Scripts\activate.bat

echo Installing requirements...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo Requirement installation failed.
    pause
    exit /b 1
)

echo.
echo Backend URL: http://127.0.0.1:8000
echo API Docs:    http://127.0.0.1:8000/docs
echo Keep this window open while using the dashboard.
echo.
uvicorn app:app --host 127.0.0.1 --port 8000 --reload

pause
