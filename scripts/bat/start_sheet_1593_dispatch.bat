@echo off
title DBERT Sheet (1,593 Candidates) Multi-Account Dispatcher
cd /d "%~dp0\..\.."

echo ======================================================================
echo  DBERT SHEET (1,593 CANDIDATES) PROVISIONAL DISPATCH ENGINE
echo  Multi-Account Google Workspace SMTP Pool (5 Accounts)
echo ======================================================================
echo.
echo Launching live batch delivery with ~20s randomized human pacing...
echo Deduplication against prior 409 dispatches is active.
echo Live telemetry reports will dispatch to leadership every 100 emails.
echo.

python scripts\dispatch_sheet_1593.py --live

echo.
echo ======================================================================
echo  Dispatch script ended. Check data\dispatch_sheet_1593.log for details.
echo ======================================================================
pause
