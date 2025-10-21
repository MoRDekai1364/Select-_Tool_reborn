@echo off
title SelectPlus V3.2 Project Launcher
color 0A
echo.
echo ==========================================
echo    SelectPlus V3.2 - Project Launcher
echo ==========================================
echo.
echo Choose what you want to do:
echo.
echo 1. Install SelectPlus V3.2 (GUI Installer)
echo 2. Run SelectPlus V3.2 Application
echo 3. Open Project Folder
echo 4. View Installation Guide
echo 5. Exit
echo.
echo ==========================================
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo.
    echo Launching GUI Installer...
    start "" "Setup_SelectPlus_V3.2.bat"
) else if "%choice%"=="2" (
    echo.
    echo Launching SelectPlus V3.2...
    start "" "SelectPlus_V3.2.bat"
) else if "%choice%"=="3" (
    echo.
    echo Opening project folder...
    start "" explorer "%~dp0..\.."
) else if "%choice%"=="4" (
    echo.
    echo Opening Installation Guide...
    start "" "../docs/INSTALLER_README.md"
) else if "%choice%"=="5" (
    echo.
    echo Goodbye!
    exit
) else (
    echo.
    echo Invalid choice. Please try again.
    pause
    cls
    goto :start
)

echo.
echo Done!
pause
