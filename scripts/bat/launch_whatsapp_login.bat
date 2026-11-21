@echo off
chcp 65001 >nul
title DBERT WhatsApp Login Launcher
color 0A

:MENU
cls
echo ==============================================================================
echo                      DBERT WHATSAPP LOGIN LAUNCHER
echo ==============================================================================
echo.
echo   [1] Launch Chrome for ACCOUNT 1 (Session: .chrome_session_account1)
echo   [2] Launch Chrome for ACCOUNT 2 (Session: .chrome_session_account2)
echo   [3] Check Login Status of Both Accounts (Verify if QR or Logged In)
echo   [4] Run 60 ₹299 Target Dispatch Daemon (30 Acc 1 + 30 Acc 2)
echo   [5] Exit
echo.
echo ==============================================================================
set /p choice="Select an option (1-5): "

if "%choice%"=="1" goto LOGIN_ACC1
if "%choice%"=="2" goto LOGIN_ACC2
if "%choice%"=="3" goto CHECK_STATUS
if "%choice%"=="4" goto LAUNCH_DISPATCH
if "%choice%"=="5" goto EXIT
goto MENU

:LOGIN_ACC1
cls
echo ==============================================================================
echo   LAUNCHING CHROME FOR ACCOUNT 1 WHATSAPP LOGIN
echo   Session: C:\Users\user\Desktop\aivara\aivara\.chrome_session_account1
echo ==============================================================================
echo.
echo   1. The Chrome browser window will open with WhatsApp Web.
echo   2. Scan the QR code using WhatsApp on your phone (Linked Devices).
echo   3. Once your chat list loads, your session is saved.
echo.
start "" "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --user-data-dir="C:\Users\user\Desktop\aivara\aivara\.chrome_session_account1" --no-first-run --no-default-browser-check https://web.whatsapp.com
echo Chrome launched for Account 1.
echo.
pause
goto MENU

:LOGIN_ACC2
cls
echo ==============================================================================
echo   LAUNCHING CHROME FOR ACCOUNT 2 WHATSAPP LOGIN
echo   Session: C:\Users\user\Desktop\aivara\aivara\.chrome_session_account2
echo ==============================================================================
echo.
echo   1. The Chrome browser window will open with WhatsApp Web.
echo   2. Scan the QR code using WhatsApp on your phone (Linked Devices).
echo   3. Once your chat list loads, your session is saved.
echo.
start "" "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --user-data-dir="C:\Users\user\Desktop\aivara\aivara\.chrome_session_account2" --no-first-run --no-default-browser-check https://web.whatsapp.com
echo Chrome launched for Account 2.
echo.
pause
goto MENU

:CHECK_STATUS
cls
echo ==============================================================================
echo   CHECKING LOGIN STATUS FOR BOTH ACCOUNTS...
echo ==============================================================================
echo.
cd /d "C:\Users\user\Desktop\dbert-website-lms"
python scripts\check_both_whatsapp_logins.py
echo.
pause
goto MENU

:LAUNCH_DISPATCH
cls
echo ==============================================================================
echo   STARTING 60-TARGET ₹299 WHATSAPP DISPATCH DAEMON (10-30s PACING)
echo ==============================================================================
echo.
cd /d "C:\Users\user\Desktop\dbert-website-lms"
python scripts\dispatch_60_targets_299_whatsapp.py
echo.
pause
goto MENU

:EXIT
exit
