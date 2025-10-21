@echo off
title SelectPlus V3.2 Installer
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python first from https://python.org
    pause
    exit /b 1
)

REM Launch the GUI installer
python installer_frontend.py

REM Keep window open if there's an error
if %errorlevel% neq 0 (
    echo.
    echo Installation failed. Please check the error messages above.
    pause
)
