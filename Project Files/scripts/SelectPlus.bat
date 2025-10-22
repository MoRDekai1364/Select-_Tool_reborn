@echo off
title SelectPlus V3.3 - Enhanced File Manager (Optimized)
cd /d "%~dp0"

REM Performance optimizations
set PYTHONOPTIMIZE=2
set PYTHONDONTWRITEBYTECODE=1
set PYTHONUNBUFFERED=1
set PYTHONNOUSERSITE=1

REM Set optimal console buffer
mode con: cols=120 lines=40

REM Launch with optimization flags
python -O -OO "../src/SelectPlus_V3.3.py"

pause
