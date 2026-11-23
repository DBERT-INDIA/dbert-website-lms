@echo off
TITLE DBERT Batch 35 WhatsApp Dispatch (Account 2)
cd /d "C:\Users\user\Desktop\dbert-website-lms"

echo ======================================================================
echo    DBERT BATCH 35 (WAVE 1) SINGLE-ACCOUNT DISPATCH LAUNCHER
echo ======================================================================
echo Account: Account 2 (.chrome_session_account2)
echo Queue  : data\whatsapp_299_queue_batch35_live.json (35 Candidates)
echo Pacing : 18s - 32s randomized delay
echo ======================================================================
echo.
echo Launching dispatch daemon...
echo If the browser displays a QR code, scan it in WhatsApp (Linked Devices).
echo As soon as authenticated, the dispatch will start automatically.
echo.

python scripts\dispatch_batch35_single_account.py --account 2 --live --wait-auth 300

echo.
echo ======================================================================
echo Dispatch script has finished. Check logs in data\whatsapp_dispatch_299.log
echo ======================================================================
pause
