@echo off
title DBERT WhatsApp Account 1 Login (Scan QR Code)
echo ==============================================================================
echo   DBERT - WHATSAPP ACCOUNT 1 LOGIN (Odd Serials: 1..93)
echo ==============================================================================
echo.
echo Opening Chrome for Account 1. Please scan the QR code using WhatsApp on your phone.
echo Once scanned, the window will close and the session will be saved.
echo.
python scripts\verify_and_launch_16nov_whatsapp.py --account 1
pause
