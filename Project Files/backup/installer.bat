@echo off
:: SelectPlus V3.1 Installer
:: Comprehensive installer for Windows systems
:: Author: Enhanced by AI Assistant
:: Date: 2025-07-18

setlocal enabledelayedexpansion

echo.
echo ===============================================
echo SelectPlus V3.1 - Universal Windows Installer
echo ===============================================
echo.

:: Check if running as Administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This installer requires Administrator privileges.
    echo Please right-click on installer.bat and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo [INFO] Administrator privileges confirmed.

:: Set variables
set "APP_NAME=SelectPlus V3.1"
set "APP_DIR=SelectPlus_V3"
set "INSTALL_DIR=%ProgramFiles%\%APP_DIR%"
set "TEMP_DIR=%TEMP%\SelectPlus_Install"
set "PYTHON_VERSION=3.11"
set "PYTHON_URL=https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe"
set "PYTHON_INSTALLER=%TEMP_DIR%\python_installer.exe"

:: Create temp directory
if exist "%TEMP_DIR%" rmdir /s /q "%TEMP_DIR%"
mkdir "%TEMP_DIR%"

echo [INFO] Starting installation process...
echo.

:: Step 1: Check Python installation
echo [STEP 1] Checking Python installation...
python --version >nul 2>&1
if %errorLevel% equ 0 (
    for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYTHON_VER=%%v
    echo [INFO] Python !PYTHON_VER! is already installed.
    set "PYTHON_EXISTS=1"
) else (
    echo [INFO] Python not found. Will install Python %PYTHON_VERSION%.
    set "PYTHON_EXISTS=0"
)

:: Step 2: Install Python if needed
if "%PYTHON_EXISTS%"=="0" (
    echo [STEP 2] Installing Python %PYTHON_VERSION%...
    echo [INFO] Downloading Python installer...
    
    :: Try to download Python using different methods
    powershell -Command "& {try { (New-Object Net.WebClient).DownloadFile('%PYTHON_URL%', '%PYTHON_INSTALLER%') } catch { exit 1 }}" >nul 2>&1
    if %errorLevel% neq 0 (
        echo [WARNING] PowerShell download failed. Trying curl...
        curl -L -o "%PYTHON_INSTALLER%" "%PYTHON_URL%" >nul 2>&1
        if %errorLevel% neq 0 (
            echo [ERROR] Failed to download Python installer.
            echo [ERROR] Please manually install Python from python.org
            echo [ERROR] Make sure to check "Add Python to PATH" during installation.
            pause
            exit /b 1
        )
    )
    
    if not exist "%PYTHON_INSTALLER%" (
        echo [ERROR] Python installer not found after download.
        echo [ERROR] Please manually install Python from python.org
        pause
        exit /b 1
    )
    
    echo [INFO] Installing Python (this may take a few minutes)...
    "%PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_tcltk=0 Include_launcher=1 AssociateFiles=0
    if %errorLevel% neq 0 (
        echo [ERROR] Python installation failed.
        echo [ERROR] Please manually install Python from python.org
        pause
        exit /b 1
    )
    
    echo [INFO] Python installation completed.
    
    :: Refresh PATH
    call refreshenv >nul 2>&1
    
    :: Verify Python installation
    timeout /t 3 >nul
    python --version >nul 2>&1
    if %errorLevel% neq 0 (
        echo [WARNING] Python may not be properly added to PATH.
        echo [WARNING] You may need to restart your computer or manually add Python to PATH.
        set "PATH=%PATH%;%LOCALAPPDATA%\Programs\Python\Python311;%LOCALAPPDATA%\Programs\Python\Python311\Scripts"
        set "PATH=%PATH%;%ProgramFiles%\Python311;%ProgramFiles%\Python311\Scripts"
    )
) else (
    echo [STEP 2] Skipping Python installation (already installed).
)

:: Step 3: Install pip packages
echo [STEP 3] Installing Python packages...
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1

echo [INFO] Installing required packages...
if exist "requirements.txt" (
    python -m pip install -r requirements.txt
    if %errorLevel% neq 0 (
        echo [WARNING] Some packages failed to install via requirements.txt.
        echo [INFO] Attempting individual package installation...
        python -m pip install python-docx>=0.8.11
        python -m pip install pydub>=0.25.1
        python -m pip install moviepy>=1.0.3
    )
) else (
    echo [INFO] Installing packages individually...
    python -m pip install python-docx>=0.8.11
    python -m pip install pydub>=0.25.1
    python -m pip install moviepy>=1.0.3
)

echo [INFO] Python packages installation completed.

:: Step 4: Create installation directory
echo [STEP 4] Creating installation directory...
if exist "%INSTALL_DIR%" (
    echo [INFO] Removing existing installation...
    rmdir /s /q "%INSTALL_DIR%"
)
mkdir "%INSTALL_DIR%"

:: Step 5: Copy application files
echo [STEP 5] Copying application files...
copy "SelectPlus_V3.py" "%INSTALL_DIR%\" >nul
copy "selectplus_settings.json" "%INSTALL_DIR%\" >nul
copy "requirements.txt" "%INSTALL_DIR%\" >nul
if exist "README.md" copy "README.md" "%INSTALL_DIR%\" >nul
if exist "README_NEW_FEATURES.md" copy "README_NEW_FEATURES.md" "%INSTALL_DIR%\" >nul

:: Copy resources folder if exists
if exist "res" (
    echo [INFO] Copying resources...
    xcopy "res" "%INSTALL_DIR%\res" /e /i /h >nul
)

:: Step 6: Create launcher scripts
echo [STEP 6] Creating launcher scripts...

:: Create batch launcher
echo @echo off > "%INSTALL_DIR%\SelectPlus.bat"
echo cd /d "%INSTALL_DIR%" >> "%INSTALL_DIR%\SelectPlus.bat"
echo python SelectPlus_V3.py >> "%INSTALL_DIR%\SelectPlus.bat"
echo pause >> "%INSTALL_DIR%\SelectPlus.bat"

:: Create PowerShell launcher
echo $oldLocation = Get-Location > "%INSTALL_DIR%\SelectPlus.ps1"
echo Set-Location "%INSTALL_DIR%" >> "%INSTALL_DIR%\SelectPlus.ps1"
echo python SelectPlus_V3.py >> "%INSTALL_DIR%\SelectPlus.ps1"
echo Set-Location $oldLocation >> "%INSTALL_DIR%\SelectPlus.ps1"
echo Read-Host "Press Enter to exit..." >> "%INSTALL_DIR%\SelectPlus.ps1"

:: Step 7: Create desktop shortcut
echo [STEP 7] Creating desktop shortcut...
set "SHORTCUT_PATH=%USERPROFILE%\Desktop\SelectPlus V3.1.lnk"
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT_PATH%'); $Shortcut.TargetPath = '%INSTALL_DIR%\SelectPlus.bat'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'SelectPlus V3.1 - Enhanced File Manager'; $Shortcut.Save()"

:: Step 8: Create Start Menu shortcut
echo [STEP 8] Creating Start Menu shortcut...
set "START_MENU_PATH=%ProgramData%\Microsoft\Windows\Start Menu\Programs\SelectPlus V3.1.lnk"
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%START_MENU_PATH%'); $Shortcut.TargetPath = '%INSTALL_DIR%\SelectPlus.bat'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'SelectPlus V3.1 - Enhanced File Manager'; $Shortcut.Save()"

:: Step 9: Create uninstaller
echo [STEP 9] Creating uninstaller...
echo @echo off > "%INSTALL_DIR%\uninstall.bat"
echo echo Uninstalling SelectPlus V3.1... >> "%INSTALL_DIR%\uninstall.bat"
echo del "%USERPROFILE%\Desktop\SelectPlus V3.1.lnk" ^>nul 2^>^&1 >> "%INSTALL_DIR%\uninstall.bat"
echo del "%ProgramData%\Microsoft\Windows\Start Menu\Programs\SelectPlus V3.1.lnk" ^>nul 2^>^&1 >> "%INSTALL_DIR%\uninstall.bat"
echo cd /d "%ProgramFiles%" >> "%INSTALL_DIR%\uninstall.bat"
echo rmdir /s /q "%APP_DIR%" >> "%INSTALL_DIR%\uninstall.bat"
echo echo SelectPlus V3.1 has been uninstalled. >> "%INSTALL_DIR%\uninstall.bat"
echo pause >> "%INSTALL_DIR%\uninstall.bat"

:: Step 10: Register in Windows Programs
echo [STEP 10] Registering in Windows Programs...
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\SelectPlus V3.1" /v DisplayName /t REG_SZ /d "SelectPlus V3.1" /f >nul
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\SelectPlus V3.1" /v DisplayVersion /t REG_SZ /d "3.1" /f >nul
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\SelectPlus V3.1" /v Publisher /t REG_SZ /d "SelectPlus Team" /f >nul
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\SelectPlus V3.1" /v InstallLocation /t REG_SZ /d "%INSTALL_DIR%" /f >nul
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\SelectPlus V3.1" /v UninstallString /t REG_SZ /d "%INSTALL_DIR%\uninstall.bat" /f >nul
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\SelectPlus V3.1" /v DisplayIcon /t REG_SZ /d "%INSTALL_DIR%\SelectPlus.bat" /f >nul

:: Step 11: Test installation
echo [STEP 11] Testing installation...
cd /d "%INSTALL_DIR%"
python -c "import sys; print('Python Path:', sys.executable)"
python -c "import docx, pydub, moviepy; print('All packages imported successfully')" 2>nul
if %errorLevel% equ 0 (
    echo [INFO] All dependencies verified successfully.
) else (
    echo [WARNING] Some dependencies may not be properly installed.
    echo [WARNING] The application may still work with reduced functionality.
)

:: Cleanup
echo [STEP 12] Cleaning up...
rmdir /s /q "%TEMP_DIR%" >nul 2>&1

echo.
echo ===============================================
echo Installation Complete!
echo ===============================================
echo.
echo SelectPlus V3.1 has been installed to:
echo %INSTALL_DIR%
echo.
echo You can now run the application by:
echo 1. Double-clicking the desktop shortcut
echo 2. Using Start Menu -^> SelectPlus V3.1
echo 3. Running: "%INSTALL_DIR%\SelectPlus.bat"
echo.
echo To uninstall, run: "%INSTALL_DIR%\uninstall.bat"
echo.
echo Press any key to exit...
pause >nul
