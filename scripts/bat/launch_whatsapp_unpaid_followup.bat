@echo off
title DBERT WhatsApp Follow-up - Logged In Unpaid Candidates
cd /d "C:\Users\user\Desktop\dbert-website-lms"
echo ==============================================================================
echo   DBERT WHATSAPP CONCIERGE OUTREACH (21 LOGGED-IN UNPAID CANDIDATES)
echo ==============================================================================
echo Account 1: +91 81929 11360 (11 candidates)
echo Account 2: +91 89580 06294 (10 candidates)
echo Pacing: 18s-32s randomized anti-ban human delay.
echo ==============================================================================
echo.
python scripts\send_whatsapp_logged_in_followup.py --live
pause
