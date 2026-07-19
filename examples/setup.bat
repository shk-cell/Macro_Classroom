@echo off
chcp 65001 >nul
title 매크로 실습 환경 설치

echo ============================================
echo   매크로 실습 환경 자동 설치 스크립트
echo ============================================
echo.

:: Python 설치 여부 확인
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python이 설치되어 있지 않습니다.
    echo.
    echo 아래 순서대로 Python을 설치해주세요:
    echo.
    echo   1. https://www.python.org/downloads/ 접속
    echo   2. "Download Python 3.x.x" 버튼 클릭
    echo   3. 설치 시 반드시 "Add Python to PATH" 체크 후 설치
    echo   4. 설치 완료 후 이 파일을 다시 실행
    echo.
    pause
    start https://www.python.org/downloads/
    exit /b 1
)

:: Python 버전 출력
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo [OK] %PYVER% 감지됨
echo.

:: pip 업그레이드
echo [1/3] pip 업그레이드 중...
python -m pip install --upgrade pip --quiet
echo      완료

:: 패키지 설치
echo [2/3] pyautogui 설치 중... (화면 자동화)
python -m pip install pyautogui --quiet
echo      완료

echo [3/3] requests, Pillow 설치 중... (HTTP 요청 / 이미지 인식)
python -m pip install requests Pillow --quiet
echo      완료

echo.
echo ============================================
echo   설치 완료! 이제 .py 파일을 실행할 수 있습니다.
echo ============================================
echo.
echo  실행 방법:
echo    - 01_좌표기반_매크로.py  더블클릭
echo    - 02_이미지기반_매크로.py 더블클릭
echo    - 03_HTML요소_매크로.py  더블클릭
echo.
pause
