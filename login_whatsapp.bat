@echo off
chcp 65001 >nul
title DBERT WhatsApp Web Login Launcher
color 0A

echo ==============================================================================
echo                      DBERT WHATSAPP LOGIN LAUNCHER
echo ==============================================================================
echo.
echo   [1] Login ACCOUNT 1 (Session: .chrome_session_account1)
echo   [2] Login ACCOUNT 2 (Session: .chrome_session_account2)
echo   [3] Exit
echo.
echo ==============================================================================
set /p choice="Select an option (1-3): "

if exist "C:\Users\user\AppData\Local\Programs\Python\Python312\python.exe" (
    set "PY_BIN=C:\Users\user\AppData\Local\Programs\Python\Python312\python.exe"
) else (
    set "PY_BIN=python"
)

if "%choice%"=="1" (
    "%PY_BIN%" scripts\login_whatsapp_helper.py --account 1
    pause
    goto :eof
)
if "%choice%"=="2" (
    "%PY_BIN%" scripts\login_whatsapp_helper.py --account 2
    pause
    goto :eof
)
if "%choice%"=="3" (
    exit /b 0
)

echo Invalid choice.
pause
