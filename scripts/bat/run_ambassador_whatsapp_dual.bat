@echo off
cd /d "%~dp0\..\.."
title DBERT Ambassador & Leads WhatsApp Dispatcher (Dual Account)
color 0e
echo ========================================================================
echo   DBERT AMBASSADOR & LEADS WHATSAPP DISPATCHER (DUAL ACCOUNTS)
echo ========================================================================
echo   Splits 17 contacts across Account 1 and Account 2
echo   Queue : data\ambassador_whatsapp_queue.json
echo   Pacing: 18s - 30s randomized human delay
echo ========================================================================
echo.
python -u scripts\send_ambassador_whatsapp.py --all-accounts
echo.
echo ========================================================================
echo   Dual WhatsApp outreach finished or paused.
echo ========================================================================
pause
