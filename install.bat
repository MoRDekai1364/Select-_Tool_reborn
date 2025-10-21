@echo off
setlocal enabledelayedexpansion

:: ============================================================================
:: Administrator Privileges Check
:: ============================================================================
openfiles >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Requesting administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
cd /d "%~dp0"

:: ============================================================================
:: Configuration
:: ============================================================================
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

:: ============================================================================
:: Helper Functions
:: ============================================================================
:DownloadFile
echo [INFO] Downloading %~2 from %~1...
powershell -Command "(New-Object Net.WebClient).DownloadFile('%~1', '%~2')" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Failed to download %~2. Please check your internet connection or URL.
    goto :error_exit
)
echo [INFO] Download complete.
goto :EOF

:ExtractZip
echo [INFO] Extracting %~1 to %~2...
powershell -Command "Expand-Archive -Path '%~1' -DestinationPath '%~2' -Force" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Failed to extract %~1. Make sure PowerShell 5+ is available.
    goto :error_exit
)
echo [INFO] Extraction complete.
goto :EOF

:EnablePipInEmbed
echo [INFO] Enabling pip in the embedded Python distribution...
set "PTH_FILE="
for /f "tokens=*" %%f in ('dir /b "%PYTHON_DIR%\python*._pth"') do set "PTH_FILE=%%f"
if defined PTH_FILE (
    powershell -Command "(Get-Content '%PYTHON_DIR%\%PTH_FILE%') -replace '#import site', 'import site' | Set-Content '%PYTHON_DIR%\%PTH_FILE%'"
    powershell -Command "(Get-Content '%PYTHON_DIR%\%PTH_FILE%') -notmatch 'python.*\.zip' | Set-Content '%PYTHON_DIR%\%PTH_FILE%'"
    echo import site >> "%PYTHON_DIR%\%PTH_FILE%"
    echo [INFO] Patched '%PTH_FILE%' to enable site packages for pip.
) else (
    echo [WARN] Could not find ._pth file. Pip setup might fail.
)
"%PYTHON_DIR%\python.exe" -m ensurepip
echo [INFO] Ensured pip is available.
goto :EOF

:: ============================================================================
:: Main Installation Logic
:: ============================================================================
cls
echo =======================================================
echo  %PROJECT_NAME% v%PROJECT_VERSION% Portable Installer
echo =======================================================
echo.

set "BASE_DIR=%~dp0"

:: --- 1. Setup Portable Python ---
if not exist "%PYTHON_DIR%\python.exe" (
    echo [STEP 1] Downloading and setting up portable Python...
    call :DownloadFile "%PYTHON_ZIP_URL%" "%PYTHON_ZIP_FILE%"
    call :ExtractZip "%PYTHON_ZIP_FILE%" "%PYTHON_DIR%"
    del "%PYTHON_ZIP_FILE%"
    call :EnablePipInEmbed
    "%PYTHON_DIR%\python.exe" --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] Portable Python setup failed.
        goto :error_exit
    )
    echo [SUCCESS] Portable Python v%PYTHON_VERSION% is set up.
) else (
    echo [INFO] Portable Python already exists. Skipping download.
)
echo.

:: --- 2. Create Python Virtual Environment ---
set "PYTHON_EXE=%BASE_DIR%%PYTHON_DIR%\python.exe"
set "VENV_PATH=%BASE_DIR%%VENV_DIR%"
set "PIP_EXE=%BASE_DIR%%VENV_DIR%\Scripts\pip.exe"

if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo [STEP 2] Creating Python virtual environment...
    "%PYTHON_EXE%" -m venv "%VENV_PATH%"
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create the virtual environment.
        goto :error_exit
    )
    echo [SUCCESS] Virtual environment created.
) else (
    echo [INFO] Virtual environment already exists.
)
echo.

:: --- 3. Copy Application Files ---
echo [STEP 3] Copying application files...
if not exist "%SOURCE_APP_DIR%" (
    echo [ERROR] Source directory not found: '%SOURCE_APP_DIR%'. Ensure it is in the same folder as this script.
    goto :error_exit
)
if exist "%APP_DIR%" rmdir /s /q "%APP_DIR%"
xcopy "%SOURCE_APP_DIR%" "%APP_DIR%\" /E /I /Q /Y /K
echo [SUCCESS] Application files copied to the '%APP_DIR%' directory.
echo.

:: --- 4. Install Dependencies ---
echo [STEP 4] Installing project dependencies...
"%PIP_EXE%" install --upgrade pip > nul
set "REQ_FILE=%APP_DIR%\config\requirements.txt"
if not exist "%REQ_FILE%" (
    echo [ERROR] '%REQ_FILE%' not found!
    goto :error_exit
)
findstr /i /c:"Pillow" "%REQ_FILE%" > nul
if errorlevel 1 (
    echo [INFO] 'Pillow' not found in requirements.txt. Adding it now...
    (echo Pillow) >> "%REQ_FILE%"
)
"%PIP_EXE%" install -r "%REQ_FILE%"
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies from '%REQ_FILE%'.
    goto :error_exit
)
echo [SUCCESS] All dependencies have been installed.
echo.

:: --- 5. Setup FFMPEG ---
if not exist "%BIN_DIR%\ffmpeg.exe" (
    echo [STEP 5] Downloading ffmpeg for media features...
    call :DownloadFile "%FFMPEG_ZIP_URL%" "%FFMPEG_ZIP_FILE%"
    if not exist "%BIN_DIR%" mkdir "%BIN_DIR%"
    powershell -Command "Expand-Archive -Path '%FFMPEG_ZIP_FILE%' -DestinationPath 'temp_ffmpeg' -Force; Move-Item -Path 'temp_ffmpeg\*\bin\ffmpeg.exe' -Destination '%BIN_DIR%'; Remove-Item -Path 'temp_ffmpeg' -Recurse -Force" >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to extract ffmpeg.exe. Media features may not work.
    ) else (
        echo [SUCCESS] ffmpeg is set up.
    )
    if exist "%FFMPEG_ZIP_FILE%" del "%FFMPEG_ZIP_FILE%"
) else (
    echo [INFO] ffmpeg already exists. Skipping download.
)
echo.

:: --- 6. Precompile Python Scripts ---
echo [STEP 6] Precompiling application scripts...
if exist "%APP_DIR%\scripts\precompile.py" (
    "%VENV_PATH%\Scripts\python.exe" "%APP_DIR%\scripts\precompile.py"
    echo [SUCCESS] Scripts precompiled.
) else (
    echo [INFO] Precompile script not found, skipping.
)
echo.

:: --- 7. Create Launcher and Shortcuts ---
echo [STEP 7] Creating launcher and shortcuts...
(
    echo @echo off
    echo setlocal
    echo title %PROJECT_NAME% v%PROJECT_VERSION%
    echo cd /d "%~dp0"
    echo echo [+] Adding tools to session PATH...
    echo set "PATH=%~dp0%BIN_DIR%;%PATH%"
    echo echo [+] Activating virtual environment...
    echo call "%VENV_DIR%\Scripts\activate.bat"
    echo echo [+] Launching %PROJECT_NAME%...
    echo python "%APP_DIR%\src\%MAIN_SCRIPT%"
    echo echo.
    echo [+] %PROJECT_NAME% has closed.
    echo call "%VENV_DIR%\Scripts\deactivate.bat"
    echo pause
    echo endlocal
) > "run_%PROJECT_NAME%.bat"
echo [INFO] 'run_%PROJECT_NAME%.bat' created.

set "SHORTCUT_PATH=%USERPROFILE%\Desktop\%PROJECT_NAME%.lnk"
set "TARGET_PATH=%BASE_DIR%run_%PROJECT_NAME%.bat"
set "ICON_PATH=%BASE_DIR%%APP_DIR%\resources\res\images\icons\Select+ICON.ico"
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT_PATH%'); $s.TargetPath = '%TARGET_PATH%'; $s.IconLocation = '%ICON_PATH%'; $s.WorkingDirectory = '%BASE_DIR%'; $s.Save()"
echo [INFO] Desktop shortcut created.
echo.

echo =======================================================
echo  Installation Complete!
echo =======================================================
echo.
echo You can find the shortcut on your Desktop or
echo run 'run_%PROJECT_NAME%.bat' to start the application.
echo.
pause
exit /b 0

:error_exit
echo.
echo [FATAL] Installation failed. Please review the error messages above.
echo.
pause
exit /b 1

