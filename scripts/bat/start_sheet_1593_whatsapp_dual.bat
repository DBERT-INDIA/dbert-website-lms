@echo off
title DBERT Sheet 1593 (First 92 Candidates) WhatsApp Dual Dispatch
cd /d "%~dp0\..\.."

echo ========================================================================
echo   DBERT — SHEET 1593 (FIRST 92 CANDIDATES) DUAL WHATSAPP DISPATCH
echo ========================================================================
echo   - Account 1 (Odd Serials)  : 46 Candidates (.chrome_session_account1)
echo   - Account 2 (Even Serials) : 46 Candidates (.chrome_session_account2)
echo   - Pacing                   : 18s - 35s randomized human breaks
echo   - Circuit Breaker          : Auto-pause on 3 consecutive failures
echo   - Alignment                : Links and Email Notices in first 15 lines
echo ========================================================================
echo.

echo [Step 1/2] Loading first 92 uncontacted candidates from Sheet 1593...
python scripts\send_dbert_whatsapp.py --load-sheet-92
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to load candidates into queue.
    pause
    exit /b 1
)

echo.
echo [Step 2/2] Running Pre-Flight Verification & Parallel Launch...
echo If any account requires QR scan, Chrome will open visibly.
echo Once verified, Worker 1 (Odd) and Worker 2 (Even) will start automatically.
echo.
python scripts\verify_and_launch_dbert_whatsapp.py

echo.
echo ========================================================================
echo   WhatsApp dispatch session active. Monitor both worker windows.
echo ========================================================================
pause
