@echo off
title Macro Classroom - Setup

echo ============================================
echo   Macro Classroom - Environment Setup
echo ============================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed.
    echo.
    echo Please install Python from:
    echo   https://www.python.org/downloads/
    echo.
    echo IMPORTANT: Check "Add Python to PATH" during installation.
    echo After installation, run this file again.
    echo.
    start https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo [OK] %PYVER% detected
echo.

echo [1/3] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo      Done

echo [2/3] Installing pyautogui...
python -m pip install pyautogui --quiet
echo      Done

echo [3/3] Installing requests and Pillow...
python -m pip install requests Pillow --quiet
echo      Done

echo.
echo ============================================
echo   Setup complete! You can now run .py files.
echo ============================================
echo.
pause
