@echo off
title DBERT WhatsApp Account 2 Login (Scan QR Code)
echo ==============================================================================
echo   DBERT - WHATSAPP ACCOUNT 2 LOGIN (Even Serials: 2..94)
echo ==============================================================================
echo.
echo Opening Chrome for Account 2. Please scan the QR code using WhatsApp on your phone.
echo Once scanned, the window will close and the session will be saved.
echo.
python scripts\verify_and_launch_16nov_whatsapp.py --account 2
pause
