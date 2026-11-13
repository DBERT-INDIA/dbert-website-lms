@echo off
cd /d "%~dp0\..\.."
title DBERT Ambassador & Leads WhatsApp Dispatcher
color 0b
echo ========================================================================
echo   DBERT AMBASSADOR & LEADS WHATSAPP DISPATCHER
echo ========================================================================
echo   Target: 17 verified contacts (10 Ambassadors + 7 Referred Leads)
echo   Queue : data\ambassador_whatsapp_queue.json
echo   Pacing: 18s - 30s randomized human delay
echo ========================================================================
echo.
python -u scripts\send_ambassador_whatsapp.py --account 1
echo.
echo ========================================================================
echo   WhatsApp outreach finished or paused.
echo ========================================================================
pause
