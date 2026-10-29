@echo off
TITLE AI Math Problem Explainer and Error Checker
echo =========================================================================
echo    AI Math Problem Explainer and Error Checker - Capstone System
echo =========================================================================

REM Check for virtual environment or system Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python was not found in your PATH. Please install Python 3.10+
    pause
    exit /b 1
)

REM Setup .env if missing
if not exist .env (
    echo [INFO] Creating .env file from .env.example...
    copy .env.example .env >nul
)

REM Create data and exports directories if missing
if not exist data mkdir data
if not exist exports mkdir exports

echo [INFO] Starting Flask Application Server...
echo [INFO] Open your web browser at: http://127.0.0.1:5050
echo [INFO] Press Ctrl+C in this terminal to stop the server.
echo =========================================================================

echo [INFO] Opening web browser...
start "" http://127.0.0.1:5050

python app.py
pause
