@echo off
chcp 437 >nul
echo ================================
echo  Macro Classroom V3 - Auto Install
echo ================================
echo.
echo  * Installs Python 3.12 + selenium to run macro_v3_tag.py (Chrome required).
echo.

:: Check if Python 3.12 is already installed
python --version 2>nul | findstr "3.12" >nul
if %errorlevel% == 0 (
    echo Python 3.12 already installed. Skipping...
) else (
    echo Installing Python 3.12...
    winget install -e --id Python.Python.3.12 --silent --accept-package-agreements --accept-source-agreements
    echo Python 3.12 installed!
    echo.
    set "PATH=%LOCALAPPDATA%\Programs\Python\Python312;%LOCALAPPDATA%\Programs\Python\Python312\Scripts;%PATH%"
)

echo.
echo Installing Python packages...
python -m pip install --upgrade pip
python -m pip install selenium

echo.
echo ================================
echo  All done! You can now run:
echo    python macro_v3_tag.py
echo ================================
pause
