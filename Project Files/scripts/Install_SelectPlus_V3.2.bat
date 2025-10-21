@echo off
REM SelectPlus V3.2 Silent Installation Script
REM This script runs silently in the background

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    exit /b 1
)

REM Install required packages silently
pip install python-docx >nul 2>&1
pip install pydub >nul 2>&1
pip install moviepy >nul 2>&1
pip install Pillow >nul 2>&1

REM Create desktop shortcut using PowerShell
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\SelectPlus V3.2.lnk'); $Shortcut.TargetPath = '%~dp0SelectPlus_V3.2.bat'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Description = 'SelectPlus V3.2 - Enhanced File Manager with Image Processing'; $Shortcut.IconLocation = 'C:\Windows\System32\shell32.dll,4'; $Shortcut.Save()" >nul 2>&1

REM Installation complete - exit silently
exit /b 0
