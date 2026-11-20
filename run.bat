@echo off
title HappyMiles Tours Server
echo ===================================================
echo     Starting HappyMiles Tours - FastAPI Server
echo     "Turning Miles into Memories!"
echo ===================================================
echo.
cd /d "%~dp0"
echo Opening browser in 3 seconds...
start "" http://localhost:8000
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
pause
