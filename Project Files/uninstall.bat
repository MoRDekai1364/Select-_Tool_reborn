@echo off
setlocal

:: ##############################################################################
:: #                                                                            #
:: #              SelectPlus v3.3 - Portable Uninstaller Script                 #
:: #                                                                            #
:: ##############################################################################

:: --- Configuration ---
set "PROJECT_NAME=SelectPlus"
set "PYTHON_DIR=python"
set "VENV_DIR=venv"
set "APP_DIR=app"
set "BIN_DIR=bin"
set "LAUNCHER_SCRIPT=run_%PROJECT_NAME%.bat"
set "SHORTCUT_NAME=%PROJECT_NAME%.lnk"

:: --- Main Script Logic ---
title %PROJECT_NAME% Uninstaller

:CHECK_ADMIN
    echo [+] Checking for administrator privileges...
    net session >nul 2>&1
    if %errorlevel% neq 0 (
        echo [!] This uninstaller requires administrator privileges.
        echo [+] Attempting to re-launch as administrator...
        powershell -Command "Start-Process '%~f0' -Verb RunAs"
        exit
    )
    echo [+] Running as administrator.
    cls

:start
    echo =======================================================
    echo  %PROJECT_NAME% Portable Uninstaller
    echo =======================================================
    echo.
    echo Please choose an uninstall option:
    echo.
    echo   1. Remove Application ^& Environment ONLY (Keeps portable Python and tools)
    echo   2. Remove EVERYTHING (Application, Environment, AND portable Python/tools)
    echo   3. Cancel Uninstall
    echo.
    echo =======================================================

    choice /c 123 /m "Enter your choice: "
    if errorlevel 3 goto Cancel
    if errorlevel 2 goto RemoveAll
    if errorlevel 1 goto RemoveAppOnly
    goto start

:RemoveAppOnly
    echo.
    echo This will remove the Select+ application, its virtual environment,
    echo and shortcuts. The portable Python installation and tools will be kept.
    echo.
    choice /c YN /m "Are you sure you want to continue? [Y/N]: "
    if errorlevel 2 goto Cancel
    echo.

    echo [INFO] Removing application files (%APP_DIR%)...
    if exist "%APP_DIR%" rmdir /s /q "%APP_DIR%"

    echo [INFO] Removing virtual environment (%VENV_DIR%)...
    if exist "%VENV_DIR%" rmdir /s /q "%VENV_DIR%"

    echo [INFO] Removing launcher script (%LAUNCHER_SCRIPT%)...
    if exist "%LAUNCHER_SCRIPT%" del "%LAUNCHER_SCRIPT%"

    echo [INFO] Removing desktop shortcut...
    if exist "%USERPROFILE%\Desktop\%SHORTCUT_NAME%" del "%USERPROFILE%\Desktop\%SHORTCUT_NAME%"

    echo.
    echo [SUCCESS] Select+ Application and Environment have been removed.
    goto EndUninstall

:RemoveAll
    echo.
    echo WARNING: This will permanently remove EVERYTHING, including the
    echo portable Python installation and all application files.
    echo.
    choice /c YN /m "Are you ABSOLUTELY sure? [Y/N]: "
    if errorlevel 2 goto Cancel
    echo.

    echo [INFO] Removing all portable installation files...

    if exist "%APP_DIR%" rmdir /s /q "%APP_DIR%"
    if exist "%VENV_DIR%" rmdir /s /q "%VENV_DIR%"
    if exist "%PYTHON_DIR%" rmdir /s /q "%PYTHON_DIR%"
    if exist "%BIN_DIR%" rmdir /s /q "%BIN_DIR%"
    if exist "%LAUNCHER_SCRIPT%" del "%LAUNCHER_SCRIPT%"
    if exist "install.bat" del "install.bat"
    if exist "%USERPROFILE%\Desktop\%SHORTCUT_NAME%" del "%USERPROFILE%\Desktop\%SHORTCUT_NAME%"

    echo.
    echo [SUCCESS] %PROJECT_NAME% has been completely removed.
    echo [INFO] This uninstaller will now delete itself.
    (goto) 2>nul & del "%~f0"
    goto EndUninstall

:Cancel
    echo.
    echo Uninstall cancelled. No changes were made.
    goto EndUninstall

:EndUninstall
    echo.
    pause
    exit /b 0
