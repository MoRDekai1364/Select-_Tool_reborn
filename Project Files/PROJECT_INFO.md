# SelectPlus V3.2 - Project Structure

## 📁 Project Organization

### 📂 `/src` - Source Code
- `SelectPlus_V3.2.py` - Main application (latest version)
- `SelectPlus_V3.py` - Previous version

### 📂 `/scripts` - Executable Scripts
- `SelectPlus_V3.2.bat` - Application launcher
- `Setup_SelectPlus_V3.2.bat` - GUI installer launcher
- `Install_SelectPlus_V3.2.bat` - Silent installer
- `Install_SelectPlus_V3.2_GUI.bat` - GUI installer with console
- `LAUNCHER.bat` - Project launcher menu
- `installer_frontend.py` - GUI installer frontend

### 📂 `/docs` - Documentation
- `README.md` - Main project documentation
- `V3.2_Upgrade_Notes.md` - Version 3.2 upgrade notes
- `INSTALLER_README.md` - Installer documentation
- `INSTALLATION_GUIDE.md` - Installation guide
- `README_NEW_FEATURES.md` - New features documentation

### 📂 `/config` - Configuration Files
- `selectplus_settings.json` - Application settings
- `requirements.txt` - Python dependencies

### 📂 `/backup` - Backup Files
- `SelectPlus_V3_backup.py` - Original version backup
- `installer.bat` - Old installer (deprecated)
- `installer.ps1` - Old PowerShell installer (deprecated)

### 📂 `/resources` - Resource Files
- `res/` - Resource directory (if exists)

## 🚀 Quick Start

### From Main Directory
- **Install**: Double-click `Install SelectPlus V3.2.lnk`
- **Run**: Double-click `Run SelectPlus V3.2.lnk`
- **Launcher**: Double-click `Project Launcher.lnk`

### From Scripts Directory
- **GUI Installer**: `Setup_SelectPlus_V3.2.bat`
- **Application**: `SelectPlus_V3.2.bat`
- **Project Menu**: `LAUNCHER.bat`

## 📋 Version Information
- **Current Version**: 3.2
- **Release Date**: 2025-07-18
- **Language Support**: English, Bulgarian
- **Platform**: Windows (Python 3.7+)

## 🔧 Dependencies
- python-docx
- pydub
- moviepy
- Pillow (new in v3.2)

## 📝 Features
- Enhanced file management
- Media processing (audio/video)
- Image processing (resize, convert, optimize)
- Multi-language support
- Interactive GUI installer
- Professional project structure
