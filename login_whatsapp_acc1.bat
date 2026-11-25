@echo off
chcp 65001 >nul
title DBERT WhatsApp Account 1 Login Helper
color 0B
echo ==============================================================================
echo   DBERT WHATSAPP LOGIN - ACCOUNT 1
echo   Session Directory: C:\Users\user\Desktop\aivara\aivara\.chrome_session_account1
echo ==============================================================================
echo.
echo Launching visible browser window for Account 1...
echo 1. Scan the QR code using WhatsApp on your phone (Linked Devices).
echo 2. Once linked, the helper will automatically detect your login and save the session.
echo.

if exist "C:\Users\user\AppData\Local\Programs\Python\Python312\python.exe" (
    set "PY_BIN=C:\Users\user\AppData\Local\Programs\Python\Python312\python.exe"
) else (
    set "PY_BIN=python"
)

"%PY_BIN%" scripts\login_whatsapp_helper.py --account 1
echo.
pause
