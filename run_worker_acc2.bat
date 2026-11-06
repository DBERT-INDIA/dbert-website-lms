@echo off
cd /d "%~dp0"
title DBERT WhatsApp - Account 2 (EVEN)
color 0e
echo ========================================================================
echo   DBERT WHATSAPP WORKER - ACCOUNT 2 (EVEN CANDIDATES - YELLOW)
echo ========================================================================
python -u scripts\send_dbert_whatsapp.py --worker account2 --auto-start
echo.
echo ========================================================================
echo   Account 2 worker finished or paused.
echo ========================================================================
pause
