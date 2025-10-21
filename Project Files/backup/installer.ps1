# SelectPlus V3.1 PowerShell Installer
# Comprehensive installer for Windows systems
# Author: Enhanced by AI Assistant
# Date: 2025-07-18

# Require Administrator privileges
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "ERROR: This installer requires Administrator privileges." -ForegroundColor Red
    Write-Host "Please right-click on installer.ps1 and select 'Run as administrator'" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Set execution policy temporarily
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "SelectPlus V3.1 - Universal Windows Installer" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Variables
$APP_NAME = "SelectPlus V3.1"
$APP_DIR = "SelectPlus_V3"
$INSTALL_DIR = "$env:ProgramFiles\$APP_DIR"
$TEMP_DIR = "$env:TEMP\SelectPlus_Install"
$PYTHON_VERSION = "3.11.7"
$PYTHON_URL = "https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe"
$PYTHON_INSTALLER = "$TEMP_DIR\python_installer.exe"

# Create temp directory
if (Test-Path $TEMP_DIR) {
    Remove-Item $TEMP_DIR -Recurse -Force
}
New-Item -ItemType Directory -Path $TEMP_DIR -Force | Out-Null

Write-Host "[INFO] Starting installation process..." -ForegroundColor Green
Write-Host ""

# Step 1: Check Python installation
Write-Host "[STEP 1] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[INFO] Python $pythonVersion is already installed." -ForegroundColor Green
        $PYTHON_EXISTS = $true
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "[INFO] Python not found. Will install Python $PYTHON_VERSION." -ForegroundColor Yellow
    $PYTHON_EXISTS = $false
}

# Step 2: Install Python if needed
if (-not $PYTHON_EXISTS) {
    Write-Host "[STEP 2] Installing Python $PYTHON_VERSION..." -ForegroundColor Yellow
    Write-Host "[INFO] Downloading Python installer..." -ForegroundColor Green
    
    try {
        # Download Python installer
        $webClient = New-Object System.Net.WebClient
        $webClient.DownloadFile($PYTHON_URL, $PYTHON_INSTALLER)
        
        if (-not (Test-Path $PYTHON_INSTALLER)) {
            throw "Download failed"
        }
        
        Write-Host "[INFO] Installing Python (this may take a few minutes)..." -ForegroundColor Green
        
        # Install Python silently
        $installArgs = @(
            '/quiet'
            'InstallAllUsers=1'
            'PrependPath=1'
            'Include_test=0'
            'Include_tcltk=0'
            'Include_launcher=1'
            'AssociateFiles=0'
        )
        
        Start-Process -FilePath $PYTHON_INSTALLER -ArgumentList $installArgs -Wait
        
        Write-Host "[INFO] Python installation completed." -ForegroundColor Green
        
        # Refresh environment variables
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
        
        # Verify Python installation
        Start-Sleep -Seconds 3
        $pythonCheck = python --version 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[WARNING] Python may not be properly added to PATH." -ForegroundColor Yellow
            Write-Host "[WARNING] You may need to restart your computer." -ForegroundColor Yellow
            
            # Try to add Python to PATH manually
            $localAppData = "$env:LOCALAPPDATA\Programs\Python\Python311"
            $programFiles = "$env:ProgramFiles\Python311"
            
            if (Test-Path $localAppData) {
                $env:PATH += ";$localAppData;$localAppData\Scripts"
            } elseif (Test-Path $programFiles) {
                $env:PATH += ";$programFiles;$programFiles\Scripts"
            }
        }
        
    } catch {
        Write-Host "[ERROR] Failed to download or install Python." -ForegroundColor Red
        Write-Host "[ERROR] Please manually install Python from python.org" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
} else {
    Write-Host "[STEP 2] Skipping Python installation (already installed)." -ForegroundColor Green
}

# Step 3: Install pip packages
Write-Host "[STEP 3] Installing Python packages..." -ForegroundColor Yellow
Write-Host "[INFO] Upgrading pip..." -ForegroundColor Green

try {
    python -m pip install --upgrade pip | Out-Null
    
    Write-Host "[INFO] Installing required packages..." -ForegroundColor Green
    
    if (Test-Path "requirements.txt") {
        python -m pip install -r requirements.txt
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[WARNING] Some packages failed to install via requirements.txt." -ForegroundColor Yellow
            Write-Host "[INFO] Attempting individual package installation..." -ForegroundColor Green
            python -m pip install "python-docx>=0.8.11"
            python -m pip install "pydub>=0.25.1"
            python -m pip install "moviepy>=1.0.3"
        }
    } else {
        Write-Host "[INFO] Installing packages individually..." -ForegroundColor Green
        python -m pip install "python-docx>=0.8.11"
        python -m pip install "pydub>=0.25.1"
        python -m pip install "moviepy>=1.0.3"
    }
    
    Write-Host "[INFO] Python packages installation completed." -ForegroundColor Green
} catch {
    Write-Host "[WARNING] Some packages may have failed to install." -ForegroundColor Yellow
    Write-Host "[WARNING] The application may still work with reduced functionality." -ForegroundColor Yellow
}

# Step 4: Create installation directory
Write-Host "[STEP 4] Creating installation directory..." -ForegroundColor Yellow
if (Test-Path $INSTALL_DIR) {
    Write-Host "[INFO] Removing existing installation..." -ForegroundColor Green
    Remove-Item $INSTALL_DIR -Recurse -Force
}
New-Item -ItemType Directory -Path $INSTALL_DIR -Force | Out-Null

# Step 5: Copy application files
Write-Host "[STEP 5] Copying application files..." -ForegroundColor Yellow
$filesToCopy = @(
    "SelectPlus_V3.py",
    "selectplus_settings.json",
    "requirements.txt",
    "README.md",
    "README_NEW_FEATURES.md"
)

foreach ($file in $filesToCopy) {
    if (Test-Path $file) {
        Copy-Item $file $INSTALL_DIR -Force
    }
}

# Copy resources folder if exists
if (Test-Path "res") {
    Write-Host "[INFO] Copying resources..." -ForegroundColor Green
    Copy-Item "res" $INSTALL_DIR -Recurse -Force
}

# Step 6: Create launcher scripts
Write-Host "[STEP 6] Creating launcher scripts..." -ForegroundColor Yellow

# Create batch launcher
$batContent = @"
@echo off
cd /d "$INSTALL_DIR"
python SelectPlus_V3.py
pause
"@
$batContent | Out-File -FilePath "$INSTALL_DIR\SelectPlus.bat" -Encoding ASCII

# Create PowerShell launcher
$ps1Content = @"
`$oldLocation = Get-Location
Set-Location "$INSTALL_DIR"
python SelectPlus_V3.py
Set-Location `$oldLocation
Read-Host "Press Enter to exit..."
"@
$ps1Content | Out-File -FilePath "$INSTALL_DIR\SelectPlus.ps1" -Encoding UTF8

# Step 7: Create desktop shortcut
Write-Host "[STEP 7] Creating desktop shortcut..." -ForegroundColor Yellow
$desktopPath = "$env:USERPROFILE\Desktop\SelectPlus V3.1.lnk"
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($desktopPath)
$shortcut.TargetPath = "$INSTALL_DIR\SelectPlus.bat"
$shortcut.WorkingDirectory = $INSTALL_DIR
$shortcut.Description = "SelectPlus V3.1 - Enhanced File Manager"
$shortcut.Save()

# Step 8: Create Start Menu shortcut
Write-Host "[STEP 8] Creating Start Menu shortcut..." -ForegroundColor Yellow
$startMenuPath = "$env:ProgramData\Microsoft\Windows\Start Menu\Programs\SelectPlus V3.1.lnk"
$shortcut = $shell.CreateShortcut($startMenuPath)
$shortcut.TargetPath = "$INSTALL_DIR\SelectPlus.bat"
$shortcut.WorkingDirectory = $INSTALL_DIR
$shortcut.Description = "SelectPlus V3.1 - Enhanced File Manager"
$shortcut.Save()

# Step 9: Create uninstaller
Write-Host "[STEP 9] Creating uninstaller..." -ForegroundColor Yellow
$uninstallContent = @"
@echo off
echo Uninstalling SelectPlus V3.1...
del "$env:USERPROFILE\Desktop\SelectPlus V3.1.lnk" >nul 2>&1
del "$env:ProgramData\Microsoft\Windows\Start Menu\Programs\SelectPlus V3.1.lnk" >nul 2>&1
cd /d "$env:ProgramFiles"
rmdir /s /q "$APP_DIR"
echo SelectPlus V3.1 has been uninstalled.
pause
"@
$uninstallContent | Out-File -FilePath "$INSTALL_DIR\uninstall.bat" -Encoding ASCII

# Step 10: Register in Windows Programs
Write-Host "[STEP 10] Registering in Windows Programs..." -ForegroundColor Yellow
$regPath = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\SelectPlus V3.1"
New-Item -Path $regPath -Force | Out-Null
Set-ItemProperty -Path $regPath -Name "DisplayName" -Value "SelectPlus V3.1"
Set-ItemProperty -Path $regPath -Name "DisplayVersion" -Value "3.1"
Set-ItemProperty -Path $regPath -Name "Publisher" -Value "SelectPlus Team"
Set-ItemProperty -Path $regPath -Name "InstallLocation" -Value $INSTALL_DIR
Set-ItemProperty -Path $regPath -Name "UninstallString" -Value "$INSTALL_DIR\uninstall.bat"
Set-ItemProperty -Path $regPath -Name "DisplayIcon" -Value "$INSTALL_DIR\SelectPlus.bat"

# Step 11: Test installation
Write-Host "[STEP 11] Testing installation..." -ForegroundColor Yellow
Push-Location $INSTALL_DIR
try {
    python -c "import sys; print('Python Path:', sys.executable)"
    python -c "import docx, pydub, moviepy; print('All packages imported successfully')" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[INFO] All dependencies verified successfully." -ForegroundColor Green
    } else {
        Write-Host "[WARNING] Some dependencies may not be properly installed." -ForegroundColor Yellow
        Write-Host "[WARNING] The application may still work with reduced functionality." -ForegroundColor Yellow
    }
} catch {
    Write-Host "[WARNING] Could not verify all dependencies." -ForegroundColor Yellow
}
Pop-Location

# Cleanup
Write-Host "[STEP 12] Cleaning up..." -ForegroundColor Yellow
Remove-Item $TEMP_DIR -Recurse -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "Installation Complete!" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "SelectPlus V3.1 has been installed to:" -ForegroundColor Green
Write-Host $INSTALL_DIR -ForegroundColor White
Write-Host ""
Write-Host "You can now run the application by:" -ForegroundColor Green
Write-Host "1. Double-clicking the desktop shortcut" -ForegroundColor White
Write-Host "2. Using Start Menu -> SelectPlus V3.1" -ForegroundColor White
Write-Host "3. Running: $INSTALL_DIR\SelectPlus.bat" -ForegroundColor White
Write-Host ""
Write-Host "To uninstall, run: $INSTALL_DIR\uninstall.bat" -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to exit"
