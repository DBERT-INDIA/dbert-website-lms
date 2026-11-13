@echo off
set FLASK_APP=apps/portal/app.py
set FLASK_DEBUG=1
set FLASK_ENV=development
echo Starting DBERT Portal Server locally in DEBUG mode...
python -m flask run --host=127.0.0.1 --port=5000
