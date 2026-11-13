@echo off
cd /d "%~dp0\..\.."
title DBERT WhatsApp - Account 1 (ODD)
color 0a
echo ========================================================================
echo   DBERT WHATSAPP WORKER - ACCOUNT 1 (ODD CANDIDATES - GREEN)
echo ========================================================================
python -u scripts\send_dbert_whatsapp.py --worker account1 --auto-start
echo.
echo ========================================================================
echo   Account 1 worker finished or paused.
echo ========================================================================
pause
