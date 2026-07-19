@echo off
chcp 65001 > nul
title 매크로실습실 (닫으면 서버 종료)

echo.
echo  [매크로실습실] 서버 시작 중...
echo.

start /b node "%~dp0server.js"
timeout /t 2 /nobreak > nul
start http://localhost:3000

echo  서버 실행 중!
echo  접속 주소: http://localhost:3000
echo.
echo  이 창을 닫으면 서버가 자동으로 종료됩니다.
echo.

:loop
timeout /t 60 /nobreak > nul
goto loop
