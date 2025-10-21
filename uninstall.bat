@echo off
setlocal enabledelayedexpansion

:: ##############################################################################
:: #                                                                            #
:: #                    SelectPlus - Uninstaller Script                         #
:: #                                                                            #
:: ##############################################################################

:: --- Configuration ---
set "APP_NAME=SelectPlus"
set "INSTALL_DIR=%ProgramFiles%\%APP_NAME%"
set "SHORTCUT_PATH=%USERPROFILE%\Desktop\%APP_NAME%.lnk"

:: --- Main Script Logic ---
title %APP_NAME% Uninstaller

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

echo =========================================
echo  Uninstalling %APP_NAME%
echo =========================================
echo.

:CONFIRM_UNINSTALL
    echo Are you sure you want to completely remove %APP_NAME%?
    CHOICE /C YN /N /M "This will delete the application files from Program Files and the desktop shortcut. (Y/N):"
    if errorlevel 2 (
        echo.
        echo [*] Uninstall cancelled by user.
        goto :end_script
    )
    if errorlevel 1 (
        echo.
        goto :PROCEED_UNINSTALL
    )

:PROCEED_UNINSTALL
    call :remove_files
    call :remove_shortcut

    echo.
    echo -----------------------------------------
    echo.
    echo  %APP_NAME% has been uninstalled successfully!
    echo.
    echo -----------------------------------------
    echo.
    goto :end_script

:: --- Functions ---

:remove_files
    echo [+] Removing application directory...
    if exist "%INSTALL_DIR%" (
        rmdir /s /q "%INSTALL_DIR%"
        echo [+] Directory "%INSTALL_DIR%" removed.
    ) else (
        echo [*] Application directory not found.
    )
    echo.
    goto :eof

:remove_shortcut
    echo [+] Removing desktop shortcut...
    if exist "%SHORTCUT_PATH%" (
        del "%SHORTCUT_PATH%"
        echo [+] Shortcut removed.
    ) else (
        echo [*] Desktop shortcut not found.
    )
    echo.
    goto :eof

:end_script
    pause
    exit
