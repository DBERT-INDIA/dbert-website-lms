@echo off
title DBERT 16 Nov Selected Interns Dual WhatsApp Dispatch Launcher
echo ==============================================================================
echo   DBERT - 16 NOV SELECTED INTERNS DUAL WHATSAPP DISPATCH LAUNCHER
echo ==============================================================================
echo.
echo Step 1: Pre-flight check will verify Account 1 and Account 2 login sessions.
echo Step 2: If QR code needed, Chrome will open for you to scan with WhatsApp.
echo Step 3: Once verified, both Worker 1 and Worker 2 launch in parallel windows.
echo.
pause
python scripts\verify_and_launch_16nov_whatsapp.py
echo.
echo ==============================================================================
echo Execution initiated. Check individual worker windows for live progress.
echo ==============================================================================
pause
