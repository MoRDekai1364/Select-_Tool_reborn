# SelectPlus V3.2 - Enhanced File Manager

## 🚀 Quick Start
1. **Double-click** `Install_SelectPlus_V3.2.bat` to install all dependencies and create desktop shortcut
2. **Or manually run**: `python SelectPlus_V3.2.py`

## 🎯 Features

### 📂 Core File Management
- Interactive file browser with keyboard navigation
- Enhanced file operations (copy, move, delete, rename)
- Multi-selection support
- Advanced search capabilities
- Global search with Ctrl+S

### 🎬 Media Handling (Enhanced in V3.2)
- **Create Playlist**: Generate .m3u playlists from media files
- **Audio Processing**: Extract audio segments with compatible file filtering
- **Video Processing**: Trim videos with smart file detection
- **Compatible Files Only**: Shows only supported media formats

### 🖼️ Image Processing (NEW in V3.2)
- **Resize Images**: Resize with quality preservation
- **Convert Images**: Convert between JPEG, PNG, GIF, BMP, TIFF, WEBP
- **Optimize Images**: Reduce file size with customizable quality levels
- **Create Gallery**: Generate HTML image galleries

### 📊 Advanced Tools
- Content management (text extraction, find/replace)
- Organization & automation (folder organization, zip creation)
- Information & utilities (size calculation, directory mapping)
- File descriptions and properties

### 🎮 Navigation Controls
- **Arrow Keys** - Navigate through files and folders
- **Enter** - Select/Open items
- **Esc/Backspace** - Go back
- **Space** - Toggle multi-selection
- **Hot Keys** - Quick access to common operations

## 📋 Requirements
- Python 3.7+
- Required packages (installed automatically):
  - `python-docx`
  - `pydub`
  - `moviepy`
  - `Pillow` (new in V3.2)

## 💾 Installation Options

### Option 1: Automatic Installation (Recommended)
```bash
# Double-click this file to install everything
Install_SelectPlus_V3.2.bat
```

### Option 2: Manual Installation
```bash
# Install dependencies
pip install python-docx pydub moviepy Pillow

# Run the application
python SelectPlus_V3.2.py
```

## 🖥️ Desktop Shortcut
After installation, you'll find a "SelectPlus V3.2" shortcut on your desktop.

## Usage

### Main Menu
Navigate through the main menu using arrow keys and Enter:
1. **General Browsing** - Browse files and folders
2. **File & Folder Management** - Organize and manipulate files
3. **Content Management** - Work with file contents
4. **Organization & Automation** - Auto-organize files
5. **Media Handling** - Process audio/video files
6. **Information & Misc** - File information and utilities
7. **Settings** - Configure application settings

### Multi-Selection Mode
- Press `M` to toggle multi-selection mode
- Press `Space` to select/deselect items
- Press `C` to clear selection
- Press `I` to show selection info

### Global Actions
- `+` - Add new file
- `Del` - Delete selected item
- `O` - Open context menu

## 🆕 What's New in V3.2
- **Fixed**: First media handling option now works properly
- **Enhanced**: Media tools show only compatible files
- **New**: Complete image processing module
- **Improved**: Better file selection and error handling
- **Added**: Smart file type detection

## 📁 File Structure
```
SelectPlus_V3/
├── SelectPlus_V3.2.py          # Main application
├── SelectPlus_V3.2.bat         # Launcher script
├── Install_SelectPlus_V3.2.bat # Installer
├── SelectPlus_V3_backup.py     # Original backup
├── V3.2_Upgrade_Notes.md       # Upgrade documentation
└── README.md                   # This file
```

## 🛠️ Troubleshooting
- **Python not found**: Install Python from https://python.org
- **Package errors**: Run `pip install --upgrade pip` then reinstall packages
- **Permission errors**: Run as administrator if needed

## 👨‍💻 Author
Enhanced by AI Assistant
Date: 2025-07-18
Version: 3.2

## 🎉 Enjoy your enhanced file management experience!
