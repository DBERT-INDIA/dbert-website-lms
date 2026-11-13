@echo off
title DBERT Rejected Payments WhatsApp Outreach
echo ===============================================================================
echo DBERT Rejected Payments WhatsApp Outreach Engine
echo ===============================================================================
echo 1. Preview Queue (Dry Run)
echo 2. Check Dispatch Status
echo 3. Launch Account 1 (Odd Records)
echo 4. Launch Account 2 (Even Records)
echo 5. Launch Both Accounts Sequentially
echo ===============================================================================
set /p opt="Select an option (1-5): "

if "%opt%"=="1" (
    python scripts\send_rejected_payments_whatsapp.py --dry-run
)
if "%opt%"=="2" (
    python scripts\send_rejected_payments_whatsapp.py --status
)
if "%opt%"=="3" (
    python scripts\send_rejected_payments_whatsapp.py --account 1
)
if "%opt%"=="4" (
    python scripts\send_rejected_payments_whatsapp.py --account 2
)
if "%opt%"=="5" (
    python scripts\send_rejected_payments_whatsapp.py --all
)

pause
