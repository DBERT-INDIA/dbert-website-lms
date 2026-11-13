@echo off
title DBERT Cohort Drive Dispatcher (Nov 2026)
color 0B
echo ===============================================================================
echo            DBERT INTERNSHIP COHORT DRIVE - EMAIL DISPATCH LAUNCHER
echo               Multi-Account Google Workspace SMTP Delivery Pool
echo ===============================================================================
echo.
echo Target Cohort: ~1,590 Candidates (sheet_1593_provisional_registry.json)
echo Sending Pool:  5 Pooled Accounts (abhinav.sharma, manoj.kumar, sandeep.bannu, contactus, pulkit.kunar)
echo Next Cohort:   Monday, 16 November 2026 at 06:00 PM IST
echo Pacing:        14s - 26s randomized human intervals + micro-breaks
echo.
echo Select Execution Mode:
echo   [1] Dry Run (Inspect templates and queue without sending)
echo   [2] Single Test Email (Send sample email to test address)
echo   [3] LIVE Production Delivery (Execute real delivery to all 1,590 candidates)
echo   [4] Exit
echo.
set /p mode="Enter choice [1-4]: "

if "%mode%"=="1" (
    echo.
    echo Running Dry Run mode with limit 5...
    python scripts\dispatch_cohort_drive_nov2026.py --dry-run --limit 5
    pause
    exit /b
)

if "%mode%"=="2" (
    echo.
    set /p test_addr="Enter test recipient email address: "
    echo Sending test email to %test_addr%...
    python scripts\dispatch_cohort_drive_nov2026.py --live --test-email %test_addr%
    pause
    exit /b
)

if "%mode%"=="3" (
    echo.
    echo ===============================================================================
    echo WARNING: You are about to initiate LIVE email delivery to candidates!
    echo ===============================================================================
    set /p confirm="Type YES to confirm live execution: "
    if /i "%confirm%"=="YES" (
        echo Initiating live batch delivery...
        python scripts\dispatch_cohort_drive_nov2026.py --live
    ) else (
        echo Cancelled by user.
    )
    pause
    exit /b
)

exit /b
