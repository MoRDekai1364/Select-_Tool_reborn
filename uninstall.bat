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
    call :ask_uninstall_python

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

:ask_uninstall_python
    echo %APP_NAME% may have installed Python on your system.
    CHOICE /C YN /N /M "Do you want to attempt to uninstall Python as well? (Y/N):"
    if errorlevel 2 (
        echo.
        echo [*] Skipping Python uninstallation.
        goto :eof
    )
    if errorlevel 1 (
        echo.
        call :uninstall_python
        goto :eof
    )
    goto :eof

:uninstall_python
    echo [+] Searching for Python installation in the registry...
    set "python_key="
    for /f "delims=" %%i in ('reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall" /s /f "Python 3" /d /k ^| find "HKEY_"') do (
        if not defined python_key set "python_key=%%i"
    )

    if not defined python_key (
        echo [!] Could not find Python uninstall information.
        echo [*] You may need to uninstall it manually from 'Add or remove programs'.
        goto :eof
    )
    
    echo [+] Found Python uninstall entry: !python_key!
    
    set "uninstall_string="
    for /f "tokens=2,*" %%a in ('reg query "!python_key!" /v UninstallString 2^>nul') do (
        set "uninstall_string=%%b"
    )

    if not defined uninstall_string (
        echo [!] ERROR: Could not find the Python uninstall command.
        goto :eof
    )

    echo [+] Starting Python uninstaller silently... (This may take a few minutes)
    start /wait "" %uninstall_string% /quiet
    if %errorlevel% neq 0 (
       echo [!] Python uninstallation may have failed. Please check 'Add or remove programs'.
    ) else (
       echo [+] Python uninstalled successfully.
    )
    goto :eof

:end_script
    pause
    exit

