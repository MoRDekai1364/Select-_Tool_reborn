@echo off
setlocal enabledelayedexpansion

:: ##############################################################################
:: #                                                                            #
:: #              SelectPlus v3.3 - Portable Installer Script                   #
:: #                                                                            #
:: ##############################################################################

:: --- Configuration ---
set "PROJECT_NAME=SelectPlus"
set "PROJECT_VERSION=3.3"
set "MAIN_SCRIPT=SelectPlus_V3.3.py"
set "PYTHON_VERSION=3.11.7"
set "PYTHON_ARCH=amd64"
set "PYTHON_ZIP_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-embed-%PYTHON_ARCH%.zip"
set "FFMPEG_ZIP_URL=https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"

set "PYTHON_DIR=python"
set "VENV_DIR=venv"
set "APP_DIR=app"
set "BIN_DIR=bin"
set "PYTHON_ZIP_FILE=python_embed.zip"
set "FFMPEG_ZIP_FILE=ffmpeg.zip"
set "SOURCE_APP_DIR=Project Files"
set "BASE_DIR=%~dp0"

:: --- Main Script Logic ---
title %PROJECT_NAME% v%PROJECT_VERSION% Installer

:CHECK_ADMIN
    echo [+] Checking for administrator privileges...
    net session >nul 2>&1
    if %errorlevel% neq 0 (
        echo [!] This installer needs administrator privileges to create shortcuts and manage files.
        echo [+] Attempting to re-launch as administrator...
        powershell -Command "Start-Process '%~f0' -Verb RunAs"
        exit
    )
    echo [+] Running with administrator privileges.
    cls

echo =======================================================
echo  Installing %PROJECT_NAME% v%PROJECT_VERSION%
echo =======================================================
echo.

call :setup_python
call :create_venv
call :copy_app_files
call :install_dependencies
call :setup_ffmpeg
call :precompile_scripts
call :create_launcher

echo.
echo -------------------------------------------------------
echo.
echo  %PROJECT_NAME% has been installed successfully!
echo  A shortcut has been placed on your desktop.
echo.
echo  Run 'run_%PROJECT_NAME%.bat' to start the application.
echo.
echo -------------------------------------------------------
echo.
pause
exit /b 0

:: --- Functions ---

:setup_python
    echo [STEP 1/7] Setting up portable Python...
    if exist "%PYTHON_DIR%\python.exe" (
        echo [*] Portable Python already exists. Skipping download.
    ) else (
        echo [+] Downloading portable Python %PYTHON_VERSION%...
        powershell -Command "(New-Object Net.WebClient).DownloadFile('%PYTHON_ZIP_URL%', '%PYTHON_ZIP_FILE%')"
        if %errorlevel% neq 0 ( echo [!] ERROR: Failed to download Python. & goto :fail )
        
        echo [+] Extracting Python...
        powershell -Command "Expand-Archive -Path '%PYTHON_ZIP_FILE%' -DestinationPath '%PYTHON_DIR%' -Force"
        if %errorlevel% neq 0 ( echo [!] ERROR: Failed to extract Python. & goto :fail )
        
        del "%PYTHON_ZIP_FILE%"
        
        echo [+] Enabling pip in portable Python...
        set "PTH_FILE="
        for /f "tokens=*" %%f in ('dir /b "%PYTHON_DIR%\python*._pth"') do set "PTH_FILE=%%f"
        if defined PTH_FILE (
            powershell -Command "(Get-Content '%PYTHON_DIR%\%PTH_FILE%') -replace '#import site', 'import site' | Set-Content '%PYTHON_DIR%\%PTH_FILE%'"
        )
        "%PYTHON_DIR%\python.exe" -m ensurepip
    )
    echo [+] Portable Python is ready.
    echo.
    goto :eof

:create_venv
    echo [STEP 2/7] Creating Python virtual environment...
    set "PYTHON_EXE=%BASE_DIR%%PYTHON_DIR%\python.exe"
    set "VENV_PATH=%BASE_DIR%%VENV_DIR%"
    if exist "%VENV_DIR%\Scripts\activate.bat" (
        echo [*] Virtual environment already exists.
    ) else (
        "%PYTHON_EXE%" -m venv "%VENV_PATH%"
        if %errorlevel% neq 0 ( echo [!] ERROR: Failed to create the virtual environment. & goto :fail )
    )
    echo [+] Virtual environment created.
    echo.
    goto :eof

:copy_app_files
    echo [STEP 3/7] Copying application files...
    if not exist "%SOURCE_APP_DIR%" (
        echo [!] ERROR: Source directory '%SOURCE_APP_DIR%' not found.
        goto :fail
    )
    if exist "%APP_DIR%" rmdir /s /q "%APP_DIR%"
    xcopy "%SOURCE_APP_DIR%" "%APP_DIR%\" /E /I /Q /Y /K
    echo [+] Application files copied to '%APP_DIR%'.
    echo.
    goto :eof

:install_dependencies
    echo [STEP 4/7] Installing project dependencies...
    set "PIP_EXE=%BASE_DIR%%VENV_DIR%\Scripts\pip.exe"
    set "REQ_FILE=%APP_DIR%\config\requirements.txt"
    if not exist "%REQ_FILE%" (
        echo [!] ERROR: 'requirements.txt' not found!
        goto :fail
    )
    "%PIP_EXE%" install --upgrade pip > nul
    findstr /i /c:"Pillow" "%REQ_FILE%" > nul
    if errorlevel 1 (
        echo [*] 'Pillow' not found in requirements.txt. Adding it for image processing.
        (echo Pillow) >> "%REQ_FILE%"
    )
    "%PIP_EXE%" install -r "%REQ_FILE%"
    if %errorlevel% neq 0 ( echo [!] ERROR: Failed to install dependencies. & goto :fail )
    echo [+] Dependencies installed successfully.
    echo.
    goto :eof

:setup_ffmpeg
    echo [STEP 5/7] Setting up FFMPEG for media features...
    if exist "%BIN_DIR%\ffmpeg.exe" (
        echo [*] ffmpeg already exists. Skipping download.
    ) else (
        echo [+] Downloading ffmpeg...
        powershell -Command "(New-Object Net.WebClient).DownloadFile('%FFMPEG_ZIP_URL%', '%FFMPEG_ZIP_FILE%')"
        if %errorlevel% neq 0 ( echo [!] ERROR: Failed to download ffmpeg. Media features may not work. & goto :eof )
        
        if not exist "%BIN_DIR%" mkdir "%BIN_DIR%"
        echo [+] Extracting ffmpeg.exe...
        powershell -Command "Expand-Archive -Path '%FFMPEG_ZIP_FILE%' -DestinationPath 'temp_ffmpeg' -Force; Move-Item -Path 'temp_ffmpeg\*\bin\ffmpeg.exe' -Destination '%BIN_DIR%'; Remove-Item -Path 'temp_ffmpeg' -Recurse -Force" >nul 2>&1
        if %errorlevel% neq 0 (
            echo [!] ERROR: Failed to extract ffmpeg.exe.
        ) else (
            echo [+] ffmpeg is set up.
        )
        if exist "%FFMPEG_ZIP_FILE%" del "%FFMPEG_ZIP_FILE%"
    )
    echo.
    goto :eof

:precompile_scripts
    echo [STEP 6/7] Precompiling application scripts for faster startup...
    if exist "%APP_DIR%\scripts\precompile.py" (
        "%VENV_PATH%\Scripts\python.exe" "%APP_DIR%\scripts\precompile.py"
    ) else (
        echo [*] Precompile script not found, skipping.
    )
    echo [+] Scripts precompiled.
    echo.
    goto :eof

:create_launcher
    echo [STEP 7/7] Creating launcher and desktop shortcut...
    (
        echo @echo off
        echo title %PROJECT_NAME% v%PROJECT_VERSION%
        echo cd /d "%~dp0"
        echo echo [+] Adding tools to session PATH...
        echo set "PATH=%~dp0%BIN_DIR%;%PATH%"
        echo echo [+] Activating virtual environment...
        echo call "%VENV_DIR%\Scripts\activate.bat"
        echo echo [+] Launching %PROJECT_NAME%...
        echo python -O -OO "%APP_DIR%\src\%MAIN_SCRIPT%"
        echo echo.
        echo [+] %PROJECT_NAME% has closed. Press any key to exit.
        echo call "%VENV_DIR%\Scripts\deactivate.bat"
        echo pause ^>nul
    ) > "run_%PROJECT_NAME%.bat"
    echo [+] 'run_%PROJECT_NAME%.bat' created.

    set "SHORTCUT_PATH=%USERPROFILE%\Desktop\%PROJECT_NAME%.lnk"
    set "TARGET_PATH=%BASE_DIR%run_%PROJECT_NAME%.bat"
    set "ICON_PATH=%BASE_DIR%%APP_DIR%\resources\res\images\icons\Select+ICON.ico"
    powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT_PATH%'); $s.TargetPath = '%TARGET_PATH%'; $s.IconLocation = '%ICON_PATH%'; $s.WorkingDirectory = '%BASE_DIR%'; $s.Save()"
    echo [+] Desktop shortcut created.
    echo.
    goto :eof

:fail
    echo.
    echo [!] Installation failed. Please check the error messages above.
    pause
    exit /b 1
