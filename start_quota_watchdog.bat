@echo off
title DBERT Google SMTP Quota Watchdog AND Phased Dispatcher
color 0b
cd /d "%~dp0"

echo ========================================================================
echo       DBERT GOOGLE SMTP QUOTA WATCHDOG AND DISPATCH ENGINE
echo ========================================================================
echo   Target Candidate Pool : 9 Verified Candidates AND 106 Provisional Candidates
echo   Probe Interval        : Every 300 Seconds (5 Minutes)
echo   Watch Target          : Google Workspace SMTP Quota Unlock (550 5.4.5)
echo   Phase 1 Execution     : Remote EC2 Website Deploy AND Live Verification
echo   Phase 2 Execution     : Dispatch 9 Official Verified Credentials
echo   Phase 3 Execution     : Resume 106 Provisional Dispatches (Candidate #304 to #409)
echo   Phase 4 Execution     : Omnichannel Synchronization AND Telemetry
echo ========================================================================
echo.

python scripts\quota_watchdog_and_dispatcher.py --poll-interval 300

echo.
echo ========================================================================
echo Watchdog session ended.
echo ========================================================================
pause
