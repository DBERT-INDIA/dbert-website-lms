@echo off
set FLASK_DEBUG=true
set REQUIRE_POSTGRES=false
set TESTING=true
set FLASK_ENV=development
cd /d "%~dp0\..\apps\portal"
python app.py
