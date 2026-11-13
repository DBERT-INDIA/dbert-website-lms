@echo off
title DBERT Sheet 1593 Live Dispatch & Real-Time Inbox Responder
cd /d "%~dp0\..\.."

echo ======================================================================
echo  DBERT SHEET (1,593 CANDIDATES) PROVISIONAL DISPATCH & INBOX ENGINE
echo  Multi-Account Google Workspace SMTP & IMAP Pool (5 Accounts)
echo ======================================================================
echo.
echo [1/2] Launching real-time autonomous Inbox Responder daemon...
start "DBERT Inbox Responder" /min python scripts\dbert_inbox_responder.py --daemon --interval 60
echo Inbox responder is active in background (polling every 60s).
echo.
echo [2/2] Launching live candidate batch email dispatcher...
echo - 10%%, 20%%, 30%%... milestone reports will dispatch to ain.sharma.abhinav@gmail.com
echo - Pacing: ~20s average human delay per email
echo.
python scripts\dispatch_sheet_1593.py --live

echo.
echo ======================================================================
echo  Dispatch session finished. Check data\dispatch_sheet_1593.log
echo ======================================================================
pause
