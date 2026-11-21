@echo off
chcp 65001 >nul
title DBERT WhatsApp Account 1 Login
color 0B
echo ==============================================================================
echo   DBERT WHATSAPP LOGIN - ACCOUNT 1
echo   Session Directory: C:\Users\user\Desktop\aivara\aivara\.chrome_session_account1
echo ==============================================================================
echo.
echo Launching Google Chrome directly with Account 1 profile...
echo.
echo 1. Scan the QR code using WhatsApp on your phone (Linked Devices).
echo 2. Once your chat list is displayed, your session is saved.
echo 3. You may then close the Chrome browser.
echo.
start "" "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --user-data-dir="C:\Users\user\Desktop\aivara\aivara\.chrome_session_account1" --no-first-run --no-default-browser-check https://web.whatsapp.com
echo Browser window launched. Press any key to exit this console.
pause >nul
