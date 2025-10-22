@echo off
setlocal enabledelayedexpansion

:: ##############################################################################
:: #                                                                            #
:: #                selectplus v3.3 - system-wide installer                     #
:: #                                                                            #
:: ##############################################################################

:: --- configuration ---
set "APP_NAME=SelectPlus"
set "INSTALL_DIR=%ProgramFiles%\%APP_NAME%"
set "SOURCE_DIR=%~dp0"
set "PYTHON_INSTALLER_URL=https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe"
set "FFMPEG_ZIP_URL=https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
set "FFMPEG_ZIP_FILE=ffmpeg_download.zip"
set "SOURCE_APP_DIR=Project Files"
set "MAIN_SCRIPT=SelectPlus.py"


:: --- main script logic ---
title %APP_NAME% installer

:check_admin
    echo [+] checking for administrator privileges...
    net session >nul 2>&1
    if %errorlevel% neq 0 (
        echo [!] this installer requires administrator privileges.
        echo [+] attempting to re-launch as administrator...
        powershell -command "start-process '%~f0' -verb runas"
        exit
    )
    echo [+] running as administrator.
cls

echo =======================================================
echo  installing %APP_NAME% v3.3
echo =======================================================
echo.

call :check_python
call :install_dependencies
call :copy_files
call :setup_ffmpeg
call :create_launcher_and_shortcut

echo.
echo -------------------------------------------------------
echo.
echo  %APP_NAME% has been installed successfully!
echo  you can find it in: "%INSTALL_DIR%"
echo  a shortcut has been placed on your desktop.
echo.
echo -------------------------------------------------------
echo.
pause
exit /b 0

:: --- functions ---

:check_python
    echo [step 1/5] checking for python 3...
    where python >nul 2>&1
    if %errorlevel% equ 0 (
        echo [*] python is already installed.
        set "python_exe=python"
    ) else (
        echo [!] python not found.
        call :install_python
        where python >nul 2>&1
        if %errorlevel% neq 0 (
            echo [!] error: python installation failed. please restart your terminal and try again.
            goto :fail
        )
        set "python_exe=python"
    )
    echo.
goto :eof

:install_python
    echo [+] downloading python installer...
    set "python_installer=%SOURCE_DIR%python_installer.exe"
    powershell -command "(new-object net.webclient).downloadfile('%PYTHON_INSTALLER_URL%', '%PYTHON_INSTALLER%')"
    if %errorlevel% neq 0 (
        echo [!] error: failed to download python.
        goto :fail
    )
    echo [+] installing python silently... (this may take a few minutes)
    start /wait "" "%PYTHON_INSTALLER%" /quiet installallusers=1 prependpath=1
    if %errorlevel% neq 0 (
        echo [!] error: python installation failed.
        del "%PYTHON_INSTALLER%"
        goto :fail
    )
    del "%PYTHON_INSTALLER%"
    echo [+] python installed successfully.
goto :eof

:install_dependencies
    echo [step 2/5] installing required libraries...
    
    :: fix 1: use absolute path for requirements.txt
    set "REQ_FILE=%SOURCE_DIR%%SOURCE_APP_DIR%\config\requirements.txt"
    if not exist "%REQ_FILE%" (
        echo [!] error: 'requirements.txt' not found in '%SOURCE_APP_DIR%\config\'!
        goto :fail
    )
    "%PYTHON_EXE%" -m pip install --upgrade pip > nul
    findstr /i /c:"Pillow" "%REQ_FILE%" > nul
    if errorlevel 1 (
        echo [*] 'pillow' not found in requirements.txt. adding it for image processing.
        (echo pillow) >> "%REQ_FILE%"
    )
    "%PYTHON_EXE%" -m pip install -r "%REQ_FILE%"
    if %errorlevel% neq 0 ( echo [!] error: failed to install dependencies. & goto :fail )
    echo [+] libraries installed successfully.
echo.
goto :eof

:copy_files
    echo [step 3/5] copying application files to "%INSTALL_DIR%"...
    if exist "%INSTALL_DIR%" (
        echo [*] removing existing installation...
        rmdir /s /q "%INSTALL_DIR%"
    )
    mkdir "%INSTALL_DIR%"
    
    :: fix 2: use absolute path for the source folder
    xcopy "%SOURCE_DIR%%SOURCE_APP_DIR%" "%INSTALL_DIR%\" /e /i /y /q
    if %errorlevel% neq 0 (
        echo [!] error: failed to copy application files.
        goto :fail
    )
    echo [+] application files copied successfully.
    echo.
goto :eof

:setup_ffmpeg
    echo [step 4/5] setting up ffmpeg for media features...
    set "FFMPEG_STATUS="
    set "TEMP_FFMPEG_ZIP=%SOURCE_DIR%%FFMPEG_ZIP_FILE%"
    
    :: 1. check and skip if ffmpeg is already installed globally
    where ffmpeg >nul 2>&1
    if %errorlevel% equ 0 (
        echo [*] ffmpeg found globally in system path. skipping installation.
        goto :eof
    )

    :: 2. check if ffmpeg executable exists locally
    if exist "%INSTALL_DIR%\ffmpeg.exe" (
        echo [*] ffmpeg executable already exists in installation directory.
        set "FFMPEG_STATUS=local_exists"
    ) else (
        echo [!] ffmpeg not found globally or locally. download required.
        set "FFMPEG_STATUS=missing"
    )
    
    :: 3. prompt the user for installation choice
    :FFMPEG_CHOICE_PROMPT
    echo.
    echo [?] where would you like to install ffmpeg?
    echo   1. install locally (in "%INSTALL_DIR%" only - recommended)
    echo   2. install globally (add "%INSTALL_DIR%" to system path)
    echo   3. skip ffmpeg installation
    CHOICE /C 123 /N /M "enter your choice (1, 2, or 3):"
    
    if errorlevel 3 (
        echo [*] skipping ffmpeg installation.
        goto :eof
    ) else if errorlevel 1 (
        set "INSTALL_MODE=local"
    ) else if errorlevel 2 (
        set "INSTALL_MODE=global"
    )

    :: 4. download and install if missing
    if "%FFMPEG_STATUS%"=="missing" (
        call :download_and_extract
        if not exist "%INSTALL_DIR%\ffmpeg.exe" (
            echo [!] error: ffmpeg download or extraction failed. skipping global path setup.
            goto :eof
        )
    ) else (
        echo [*] ffmpeg executable already present.
    )

    :: 5. handle global path modification if chosen
    if "%INSTALL_MODE%"=="global" (
        call :add_to_path
    )
    
    echo.
goto :eof

:download_and_extract
    echo [+] downloading ffmpeg zip file...
    set "TEMP_FFMPEG_DIR=%SOURCE_DIR%temp_ffmpeg"
    
    powershell -command "(new-object net.webclient).downloadfile('%FFMPEG_ZIP_URL%', '%TEMP_FFMPEG_ZIP%')"
    if %errorlevel% neq 0 ( echo [!] error: failed to download ffmpeg. & exit /b 1)
    
    echo [+] extracting ffmpeg.exe to "%INSTALL_DIR%"...
    powershell -command "expand-archive -path '%TEMP_FFMPEG_ZIP%' -destinationpath '%TEMP_FFMPEG_DIR%' -force; move-item -path '%TEMP_FFMPEG_DIR%\*\bin\ffmpeg.exe' -destination '%INSTALL_DIR%'; remove-item -path '%TEMP_FFMPEG_DIR%' -recurse -force" >nul 2>&1
    
    if %errorlevel% neq 0 (
        echo [!] error: failed to extract ffmpeg.exe.
        del "%TEMP_FFMPEG_ZIP%"
        exit /b 1
    )
    del "%TEMP_FFMPEG_ZIP%"
    echo [+] ffmpeg executable installed locally.
    goto :eof

:add_to_path
    echo [+] adding "%INSTALL_DIR%" to system path (global access)...
    
    :: powershell command to safely append path to system environment variable
    powershell -command "$env_path = [environment]::getenvironmentvariable(\"path\", \"machine\"); ^
    $new_path = \"%%INSTALL_DIR%%\"; ^
    if (-not ($env_path -like \"*$new_path*\" -or $env_path -like \"*$new_path*\\\")) { ^
        [environment]::setenvironmentvariable(\"path\", \"$env_path;$new_path\", \"machine\"); ^
        write-host \"[+] path updated successfully.\"} else { ^
        write-host \"[*] path already contains installation directory.\"} "
    
    if %errorlevel% neq 0 (
        echo [!] error: failed to add path entry. you may need to restart.
    ) else (
        echo [+] path updated. restart console for changes to take effect.
    )
    goto :eof

:create_launcher_and_shortcut
    echo [step 5/5] creating launcher and desktop shortcut...
    
    :: fix 6: the batch file must change directory to the correct source folder
    (
        echo @echo off
        echo title %APP_NAME% v3.3
        echo cd /d "%INSTALL_DIR%\%SOURCE_APP_DIR%\src"
        echo python "%MAIN_SCRIPT%"
        echo pause ^>nul
    ) > "%INSTALL_DIR%\run_%APP_NAME%.bat"
    echo [+] 'run_%APP_NAME%.bat' created in installation directory.
    
    set "SHORTCUT_PATH=%USERPROFILE%\desktop\%APP_NAME%.lnk"
    set "TARGET_PATH=%INSTALL_DIR%\run_%APP_NAME%.bat"
    set "ICON_PATH=%INSTALL_DIR%\%SOURCE_APP_DIR%\resources\res\images\icons\select+icon.ico"
    
    :: powershell command to create shortcut and explicitly set custom icon
    powershell -command "$ws = new-object -comobject wscript.shell; $s = $ws.createshortcut('%SHORTCUT_PATH%'); $s.targetpath = '%TARGET_PATH%'; $s.iconlocation = '%ICON_PATH%'; $s.workingdirectory = '%INSTALL_DIR%'; $s.save()"
    
    echo [+] desktop shortcut created successfully with icon: %ICON_PATH%
echo.
goto :eof

:fail
    echo.
    echo [!] installation failed. please check the error messages above.
pause
    exit /b 1