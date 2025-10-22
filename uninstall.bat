@echo off
setlocal enabledelayedexpansion

:: ##############################################################################
:: #                                                                            #
:: #                    selectplus - uninstaller script                         #
:: #                                                                            #
:: ##############################################################################

:: --- configuration ---
set "APP_NAME=SelectPlus"
set "INSTALL_DIR=%ProgramFiles%\%APP_NAME%"
set "SHORTCUT_PATH=%USERPROFILE%\Desktop\%APP_NAME%.lnk"

:: --- main script logic ---
title %APP_NAME% uninstaller

:CHECK_ADMIN
    echo [+] checking for administrator privileges...
    net session >nul 2>&1
    if %errorlevel% neq 0 (
        echo [!] this uninstaller requires administrator privileges.
        echo [+] attempting to re-launch as administrator...
        powershell -command "start-process '%~f0' -verb runas"
        exit
    )
    echo [+] running as administrator.
    cls

echo =========================================
echo  uninstalling %APP_NAME%
echo =========================================
echo.

:CONFIRM_UNINSTALL
    echo are you sure you want to completely remove %APP_NAME%?
    CHOICE /C YN /N /M "this will delete the application files from program files and the desktop shortcut. (Y/N):"
    if errorlevel 2 (
        echo.
        echo [*] uninstall cancelled by user.
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
    call :ask_uninstall_ffmpeg
    call :cleanup_logs

    echo.
    echo -----------------------------------------
    echo.
    echo  %APP_NAME% has been uninstalled successfully!
    echo.
    echo -----------------------------------------
    echo.
    goto :end_script

:: --- functions ---

:remove_files
    echo [+] removing application directory...
    if exist "%INSTALL_DIR%" (
        rmdir /s /q "%INSTALL_DIR%"
        echo [+] directory "%INSTALL_DIR%" removed.
    ) else (
        echo [*] application directory not found.
    )
    echo.
goto :eof

:remove_shortcut
    echo [+] removing desktop shortcut...
    if exist "%SHORTCUT_PATH%" (
        del "%SHORTCUT_PATH%"
        echo [+] shortcut removed.
    ) else (
        echo [*] desktop shortcut not found.
    )
    echo.
goto :eof

:ask_uninstall_python
    echo %APP_NAME% may have installed python on your system.
    CHOICE /C YN /N /M "do you want to attempt to uninstall python as well? (Y/N):"
    if errorlevel 2 (
        echo.
        echo [*] skipping python uninstallation.
        goto :eof
    )
    if errorlevel 1 (
        echo.
        call :uninstall_python
        goto :eof
    )
    goto :eof

:uninstall_python
    echo [+] searching for python installation in the registry...
    set "python_key="
    for /f "delims=" %%i in ('reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall" /s /f "Python 3" /d /k ^| find "HKEY_"') do (
        if not defined python_key set "python_key=%%i"
    )

    if not defined python_key (
        echo [!] could not find python uninstall information.
        echo [*] you may need to uninstall it manually from 'add or remove programs'.
        goto :eof
    )
    
    echo [+] found python uninstall entry: !python_key!
    set "uninstall_string="
    for /f "tokens=2,*" %%a in ('reg query "!python_key!" /v uninstallstring 2^>nul') do (
        set "uninstall_string=%%b"
    )

    if not defined uninstall_string (
        echo [!] error: could not find the python uninstall command.
        goto :eof
    )

    echo [+] starting python uninstaller silently... (this may take a few minutes)
    start /wait "" %uninstall_string% /quiet
    if %errorlevel% neq 0 (
        echo [!] python uninstallation may have failed. please check 'add or remove programs'.
    ) else (
       echo [+] python uninstalled successfully.
    )
    goto :eof

:ask_uninstall_ffmpeg
    echo %APP_NAME% may have installed ffmpeg for media features.
    CHOICE /C YN /N /M "do you want to remove the ffmpeg executable and path configuration? (Y/N):"
    if errorlevel 2 (
        echo.
        echo [*] skipping ffmpeg removal.
        goto :eof
    )
    if errorlevel 1 (
        echo.
        call :uninstall_ffmpeg
        goto :eof
    )
    goto :eof

:uninstall_ffmpeg
    echo [+] attempting to remove ffmpeg.exe from "%INSTALL_DIR%"...
    if exist "%INSTALL_DIR%\ffmpeg.exe" (
        del "%INSTALL_DIR%\ffmpeg.exe"
        echo [+] ffmpeg.exe removed locally.
    ) else (
        echo [*] ffmpeg.exe not found in "%INSTALL_DIR%".
    )
    
    :: check if the directory was added to the system path
    call :ask_remove_global_path
    
    goto :eof

:ask_remove_global_path
    echo.
    echo [!] the installer may have added "%INSTALL_DIR%" to the system path for global access.
    CHOICE /C YN /N /M "do you want to remove the path entry from your system's global path? (Y/N):"
    
    if errorlevel 2 (
        echo.
        echo [*] skipping global path removal.
        goto :eof
    )
    if errorlevel 1 (
        echo.
        call :remove_from_path
        goto :eof
    )
    goto :eof

:remove_from_path
    echo [+] removing "%INSTALL_DIR%" from system path...
    
    :: powershell command to safely remove path entry from system environment variable
    powershell -command "$env_path = [environment]::getenvironmentvariable(\"path\", \"machine\"); ^
    $new_path = \"%%INSTALL_DIR%%\"; ^
    if ($env_path -like \"*$new_path*\") { ^
        $escaped_path = [regex]::escape($new_path); ^
        $env_path = $env_path -replace \"(?:;|^)$escaped_path\", ''; ^
        [environment]::setenvironmentvariable(\"path\", $env_path, \"machine\"); ^
        write-host \"[+] path entry removed successfully.\"} else { ^
        write-host \"[*] path entry was not found to remove.\"} "
    
    if %errorlevel% neq 0 (
        echo [!] error: failed to remove path entry. you may need to restart.
    ) else (
        echo [+] system path cleanup complete.
    )
    goto :eof

:cleanup_logs
    echo [+] removing installer log files...
    if exist "%INSTALL_DIR%\selectplus_install_log.txt" del "%INSTALL_DIR%\selectplus_install_log.txt"
    if exist "%~dp0selectplus_install_log.txt" del "%~dp0selectplus_install_log.txt"
    goto :eof

:end_script
    pause
    exit