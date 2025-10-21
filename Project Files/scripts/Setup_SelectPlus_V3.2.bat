@echo off
REM Launch the GUI installer without showing command window
cd /d "%~dp0"
start "" pythonw installer_frontend.py
