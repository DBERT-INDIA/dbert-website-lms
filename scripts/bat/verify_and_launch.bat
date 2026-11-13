@echo off
cd /d "%~dp0\..\.."
title DBERT WhatsApp - Pre-Flight Verifier and Dual Launcher
color 0b
echo ========================================================================
echo   DBERT WHATSAPP PRE-FLIGHT VERIFIER AND DUAL ACCOUNT LAUNCHER
echo ========================================================================
python scripts\verify_and_launch_dbert_whatsapp.py
echo.
pause
