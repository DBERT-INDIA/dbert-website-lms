@echo off
title DBERT WhatsApp Account 1 Login
echo ======================================================================
echo   OPENING CHROME FOR ACCOUNT 1 WHATSAPP LOGIN
echo   Session: C:\Users\user\Desktop\aivara\aivara\.chrome_session_account1
echo ======================================================================
echo.
echo Please scan the QR code that appears in the Chrome browser window.
echo Once scanned and your chats are visible, simply close the browser window.
echo.
"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --user-data-dir="C:\Users\user\Desktop\aivara\aivara\.chrome_session_account1" --no-first-run --no-default-browser-check https://web.whatsapp.com
pause
