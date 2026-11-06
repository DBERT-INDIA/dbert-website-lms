@echo off
cd /d "%~dp0"
title DBERT WhatsApp - Account 2 Login / QR Scanner
color 0e
echo ========================================================================
echo   DBERT WHATSAPP - ACCOUNT 2 (EVEN) LOGIN / QR SCANNER
echo ========================================================================
echo   Session: C:\Users\user\Desktop\aivara\aivara\.chrome_session_account2
echo   Opening Chrome window... If QR code appears, please scan it on your phone.
echo ========================================================================
python scripts\verify_and_launch_dbert_whatsapp.py --login-only 2
echo.
pause
