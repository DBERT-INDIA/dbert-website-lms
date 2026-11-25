@echo off
TITLE DBERT 70 Dual-Account WhatsApp Dispatch (Account 1 + Account 2)
cd /d "C:\Users\user\Desktop\dbert-website-lms"

echo ======================================================================
echo    DBERT BATCH 70 DUAL-ACCOUNT DISPATCH LAUNCHER
echo ======================================================================
echo Account 1: data\whatsapp_299_queue_batch35_acc1.json (35 Candidates)
echo Account 2: data\whatsapp_299_queue_batch35_acc2.json (35 Candidates)
echo Pacing   : 18s - 35s randomized human delay
echo ======================================================================
echo.
echo Starting Account 1 and Account 2 dispatch daemons in parallel...
start "DBERT Account 1 Dispatch" python scripts\dispatch_299_dual_account.py --account 1 --live
start "DBERT Account 2 Dispatch" python scripts\dispatch_299_dual_account.py --account 2 --live
echo Daemons launched in separate terminal windows.
pause
