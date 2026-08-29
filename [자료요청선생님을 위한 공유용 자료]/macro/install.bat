@echo off
chcp 437 >nul
echo ================================
echo  Macro Classroom - Auto Install
echo ================================
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
python -m pip install selenium pyautogui pyperclip opencv-python pillow

echo.
echo ================================
echo  All done! You can now run:
echo    python macro_v1_coordinate.py
echo    python macro_v2_image.py
echo    python macro_v3_tag.py
echo ================================
pause
