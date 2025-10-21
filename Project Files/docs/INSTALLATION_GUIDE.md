# SelectPlus V3.1 Installation Guide

## Overview
SelectPlus V3.1 is an enhanced file manager with advanced features including global search, interactive file browsing, and comprehensive file operations.

## System Requirements
- Windows 10 or higher
- Administrator privileges (for installation)
- Internet connection (for Python and package downloads)

## Installation Methods

### Method 1: Automatic Installation (Recommended)

#### Option A: Batch Script (Windows Command Prompt)
1. Navigate to the SelectPlus V3.1 directory
2. Right-click on `installer.bat` and select "Run as administrator"
3. Follow the on-screen instructions
4. The installer will automatically:
   - Download and install Python 3.11 (if not present)
   - Install required Python packages
   - Copy application files to Program Files
   - Create desktop and Start Menu shortcuts
   - Register the application in Windows Programs

#### Option B: PowerShell Script (Windows PowerShell)
1. Navigate to the SelectPlus V3.1 directory
2. Right-click on `installer.ps1` and select "Run with PowerShell"
3. If prompted about execution policy, type `Y` and press Enter
4. Follow the on-screen instructions

### Method 2: Manual Installation

#### Prerequisites
1. Install Python 3.11 or higher from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"
   - Check "Install for all users" (requires administrator)

2. Install required Python packages:
   ```cmd
   pip install python-docx>=0.8.11
   pip install pydub>=0.25.1
   pip install moviepy>=1.0.3
   ```

#### Installation Steps
1. Create installation directory:
   ```cmd
   mkdir "%ProgramFiles%\SelectPlus_V3"
   ```

2. Copy application files:
   ```cmd
   copy SelectPlus_V3.py "%ProgramFiles%\SelectPlus_V3\"
   copy selectplus_settings.json "%ProgramFiles%\SelectPlus_V3\"
   copy requirements.txt "%ProgramFiles%\SelectPlus_V3\"
   ```

3. Create launcher script:
   ```cmd
   echo @echo off > "%ProgramFiles%\SelectPlus_V3\SelectPlus.bat"
   echo cd /d "%ProgramFiles%\SelectPlus_V3" >> "%ProgramFiles%\SelectPlus_V3\SelectPlus.bat"
   echo python SelectPlus_V3.py >> "%ProgramFiles%\SelectPlus_V3\SelectPlus.bat"
   echo pause >> "%ProgramFiles%\SelectPlus_V3\SelectPlus.bat"
   ```

4. Create desktop shortcut (optional):
   - Right-click on desktop
   - Select "New" > "Shortcut"
   - Enter: `%ProgramFiles%\SelectPlus_V3\SelectPlus.bat`
   - Name it "SelectPlus V3.1"

## Running the Application

### After Installation
- **Desktop**: Double-click the "SelectPlus V3.1" shortcut
- **Start Menu**: Start Menu → All Programs → SelectPlus V3.1
- **Direct**: Run `%ProgramFiles%\SelectPlus_V3\SelectPlus.bat`

### From Development Directory
```cmd
cd /d "D:\Apps\SelectPlus_V3"
python SelectPlus_V3.py
```

## Features Overview

### Global Search
- **Hotkey**: Press `Ctrl+S` in file browser
- **Main Menu**: Select "🔍 Global Search" from main menu
- **Search Scopes**: System-wide, Current Directory, or Custom Directory
- **Advanced Search**: Filter by file type and size

### File Operations
- Interactive file browser with keyboard navigation
- Context menus for comprehensive file operations
- Multi-select functionality
- Cut, copy, paste, rename, delete operations
- Compress/decompress files
- Media handling (audio/video processing)

### Navigation
- Enhanced back/forward navigation
- Navigation history tracking
- Breadcrumb navigation
- Quick access to common locations

## Troubleshooting

### Python Issues
- **Error**: "python is not recognized"
  - Solution: Reinstall Python with "Add to PATH" checked
  - Alternative: Restart computer after Python installation

- **Error**: "No module named 'docx'"
  - Solution: Run `pip install python-docx pydub moviepy`

### Permission Issues
- **Error**: "Access denied"
  - Solution: Run installer as administrator
  - Alternative: Install to user directory instead of Program Files

### Search Issues
- **Error**: Search interrupted or slow
  - Solution: Adjust search scope in settings
  - Alternative: Use "Current Directory" scope for faster searches

## Uninstalling

### Automatic Uninstall
1. Navigate to `%ProgramFiles%\SelectPlus_V3`
2. Run `uninstall.bat`
3. Follow the prompts

### Manual Uninstall
1. Delete the installation directory:
   ```cmd
   rmdir /s "%ProgramFiles%\SelectPlus_V3"
   ```
2. Delete desktop shortcut: `%USERPROFILE%\Desktop\SelectPlus V3.1.lnk`
3. Delete Start Menu shortcut: `%ProgramData%\Microsoft\Windows\Start Menu\Programs\SelectPlus V3.1.lnk`

## Support

### Log Files
- Application logs: Check console output for errors
- Installation logs: Review installer output for issues

### Common Solutions
1. **Restart computer** after installation
2. **Run as administrator** for permission issues
3. **Check Python PATH** if Python commands fail
4. **Reinstall Python** if packages fail to install

## Version Information
- **Version**: 3.1
- **Release Date**: 2025-07-18
- **Python Version**: 3.11+ recommended
- **Platform**: Windows 10+

## Changes from V3.0
- Added global search functionality
- Ctrl+S hotkey for quick search
- Enhanced search interface with multiple options
- Improved navigation history management
- Better error handling and search performance
- Comprehensive installer with automatic dependency management
