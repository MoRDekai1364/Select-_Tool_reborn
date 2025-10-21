@echo off
setlocal enabledelayedexpansion

:: ##############################################################################
:: #                                                                            #
:: #                SelectPlus v3.3 - System-Wide Installer                     #
:: #                                                                            #
:: ##############################################################################

:: --- Configuration ---
set "APP_NAME=SelectPlus"
set "INSTALL_DIR=%ProgramFiles%\%APP_NAME%"
set "SOURCE_DIR=%~dp0"
set "PYTHON_INSTALLER_URL=https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe"
set "FFMPEG_ZIP_URL=https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
set "FFMPEG_ZIP_FILE=ffmpeg_download.zip"
set "SOURCE_APP_DIR=Project Files"
set "MAIN_SCRIPT=SelectPlus_V3.3.py"


:: --- Main Script Logic ---
title %APP_NAME% Installer

:CHECK_ADMIN
    echo [+] Checking for administrator privileges...
    net session >nul 2>&1
    if %errorlevel% neq 0 (
        echo [!] This installer requires administrator privileges.
        echo [+] Attempting to re-launch as administrator...
        powershell -Command "Start-Process '%~f0' -Verb RunAs"
        exit
    )
    echo [+] Running as administrator.
    cls

echo =======================================================
echo  Installing %APP_NAME% v3.3
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
echo  You can find it in: "%INSTALL_DIR%"
echo  A shortcut has been placed on your desktop.
echo.
echo -------------------------------------------------------
echo.
pause
exit /b 0

:: --- Functions ---

:check_python
    echo [STEP 1/5] Checking for Python 3...
    where python >nul 2>&1
    if %errorlevel% equ 0 (
        echo [*] Python is already installed.
        set "PYTHON_EXE=python"
    ) else (
        echo [!] Python not found.
        call :install_python
        where python >nul 2>&1
        if %errorlevel% neq 0 (
            echo [!] ERROR: Python installation failed. Please restart your terminal and try again.
            goto :fail
        )
        set "PYTHON_EXE=python"
    )
    echo.
    goto :eof

:install_python
    echo [+] Downloading Python installer...
    set "PYTHON_INSTALLER=%SOURCE_DIR%python_installer.exe"
    powershell -Command "(New-Object Net.WebClient).DownloadFile('%PYTHON_INSTALLER_URL%', '%PYTHON_INSTALLER%')"
    if %errorlevel% neq 0 (
        echo [!] ERROR: Failed to download Python.
        goto :fail
    )
    echo [+] Installing Python silently... (This may take a few minutes)
    start /wait "" "%PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1
    if %errorlevel% neq 0 (
        echo [!] ERROR: Python installation failed.
        del "%PYTHON_INSTALLER%"
        goto :fail
    )
    del "%PYTHON_INSTALLER%"
    echo [+] Python installed successfully.
    goto :eof

:install_dependencies
    echo [STEP 2/5] Installing required libraries...
    set "REQ_FILE=%SOURCE_APP_DIR%\config\requirements.txt"
     if not exist "%REQ_FILE%" (
        echo [!] ERROR: 'requirements.txt' not found in '%SOURCE_APP_DIR%\config\'!
        goto :fail
    )
    "%PYTHON_EXE%" -m pip install --upgrade pip > nul
    findstr /i /c:"Pillow" "%REQ_FILE%" > nul
    if errorlevel 1 (
        echo [*] 'Pillow' not found in requirements.txt. Adding it for image processing.
        (echo Pillow) >> "%REQ_FILE%"
    )
    "%PYTHON_EXE%" -m pip install -r "%REQ_FILE%"
    if %errorlevel% neq 0 ( echo [!] ERROR: Failed to install dependencies. & goto :fail )
    echo [+] Libraries installed successfully.
    echo.
    goto :eof

:copy_files
    echo [STEP 3/5] Copying application files to "%INSTALL_DIR%"...
    if exist "%INSTALL_DIR%" (
        echo [*] Removing existing installation...
        rmdir /s /q "%INSTALL_DIR%"
    )
    mkdir "%INSTALL_DIR%"
    
    xcopy "%SOURCE_APP_DIR%" "%INSTALL_DIR%\" /E /I /Y /Q
    if %errorlevel% neq 0 (
        echo [!] ERROR: Failed to copy application files.
        goto :fail
    )
    echo [+] Application files copied successfully.
    echo.
    goto :eof

:setup_ffmpeg
    echo [STEP 4/5] Setting up FFMPEG for media features...
    if exist "%INSTALL_DIR%\ffmpeg.exe" (
        echo [*] ffmpeg already exists in target. Skipping.
    ) else (
        echo [+] Downloading ffmpeg...
        powershell -Command "(New-Object Net.WebClient).DownloadFile('%FFMPEG_ZIP_URL%', '%FFMPEG_ZIP_FILE%')"
        if %errorlevel% neq 0 ( echo [!] ERROR: Failed to download ffmpeg. Media features may not work. & goto :eof )
        
        echo [+] Extracting ffmpeg.exe...
        powershell -Command "Expand-Archive -Path '%FFMPEG_ZIP_FILE%' -DestinationPath 'temp_ffmpeg' -Force; Move-Item -Path 'temp_ffmpeg\*\bin\ffmpeg.exe' -Destination '%INSTALL_DIR%'; Remove-Item -Path 'temp_ffmpeg' -Recurse -Force" >nul 2>&1
        if %errorlevel% neq 0 (
            echo [!] ERROR: Failed to extract ffmpeg.exe.
        ) else (
            echo [+] ffmpeg is set up.
        )
        if exist "%FFMPEG_ZIP_FILE%" del "%FFMPEG_ZIP_FILE%"
    )
    echo.
    goto :eof

:create_launcher_and_shortcut
    echo [STEP 5/5] Creating launcher and desktop shortcut...
    (
        echo @echo off
        echo title %APP_NAME% v%PROJECT_VERSION%
        echo cd /d "%INSTALL_DIR%\src"
        echo python -O -OO "%MAIN_SCRIPT%"
        echo pause ^>nul
    ) > "%INSTALL_DIR%\run_%APP_NAME%.bat"
    echo [+] 'run_%APP_NAME%.bat' created in installation directory.

    set "SHORTCUT_PATH=%USERPROFILE%\Desktop\%APP_NAME%.lnk"
    set "TARGET_PATH=%INSTALL_DIR%\run_%APP_NAME%.bat"
    set "ICON_PATH=%INSTALL_DIR%\resources\res\images\icons\Select+ICON.ico"
    powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT_PATH%'); $s.TargetPath = '%TARGET_PATH%'; $s.IconLocation = '%ICON_PATH%'; $s.WorkingDirectory = '%INSTALL_DIR%'; $s.Save()"
    echo [+] Desktop shortcut created successfully.
    echo.
    goto :eof

:fail
    echo.
    echo [!] Installation failed. Please check the error messages above.
    pause
    exit /b 1

