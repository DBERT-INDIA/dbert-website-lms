@echo off
title DBERT Local Portal LMS Server
cd /d "%~dp0\..\.."
set TESTING=1
set REQUIRE_POSTGRES=false
set FLASK_ENV=development
set PORT=5001
echo ======================================================================
echo  Starting DBERT Local Portal LMS Server on http://127.0.0.1:5001
echo ======================================================================
echo.
python apps\portal\app.py
pause
