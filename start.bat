@echo off
cd /d "%~dp0app"
call venv\Scripts\activate
python main.py
pause
