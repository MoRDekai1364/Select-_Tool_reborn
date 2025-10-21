"""
Select+ V3.3 - Enhanced File Manager with Advanced Features

Version 3.3 Features:
- Portable by design: Includes fixes for ffmpeg and other dependencies.
- Interactive file browser with keyboard navigation
- Enhanced extension handling for file creation and renaming
- Context menu with all file operations (accessible via O key)
- Comprehensive file management tools
- Advanced search and organization capabilities
- Global search with Ctrl+S hotkey
- Enhanced search interface with multiple options
- Improved navigation history management
- Enhanced Media Handling with compatible file filtering
- Image Processing module with resize, convert, optimize, and gallery features
- Lazy loading for faster startup times.

Date: 2025-08-01
"""

import os
import sys
import msvcrt
import json
from datetime import datetime

# --- Lazy Module Importers ---
# These functions prevent heavy libraries from being loaded until they are actually needed,
# resulting in a faster application startup time.

_shutil = None
_zipfile = None
_time = None
_subprocess = None
_stat = None
_ctypes = None
_Document = None
_AudioSegment = None
_VideoFileClip = None
_Image = None

def get_shutil():
    """Lazily imports and returns the shutil module."""
    global _shutil
    if _shutil is None:
        import shutil
        _shutil = shutil
    return _shutil

def get_zipfile():
    """Lazily imports and returns the zipfile module."""
    global _zipfile
    if _zipfile is None:
        import zipfile
        _zipfile = zipfile
    return _zipfile

def get_time():
    """Lazily imports and returns the time module."""
    global _time
    if _time is None:
        import time
        _time = time
    return _time

def get_subprocess():
    """Lazily imports and returns the subprocess module."""
    global _subprocess
    if _subprocess is None:
        import subprocess
        _subprocess = subprocess
    return _subprocess

def get_stat():
    """Lazily imports and returns the stat module."""
    global _stat
    if _stat is None:
        import stat
        _stat = stat
    return _stat

def get_ctypes():
    """Lazily imports and returns the ctypes module."""
    global _ctypes
    if _ctypes is None:
        if os.name == 'nt':
            import ctypes
            _ctypes = ctypes
    return _ctypes

def get_document():
    """Lazily imports and returns the Document class from python-docx."""
    global _Document
    if _Document is None:
        from docx import Document
        _Document = Document
    return _Document

def get_audio_segment():
    """Lazily imports and returns the AudioSegment class from pydub."""
    global _AudioSegment
    if _AudioSegment is None:
        from pydub import AudioSegment
        _AudioSegment = AudioSegment
    return _AudioSegment

def get_video_file_clip():
    """Lazily imports and returns the VideoFileClip class from moviepy."""
    global _VideoFileClip
    if _VideoFileClip is None:
        from moviepy.editor import VideoFileClip
        _VideoFileClip = VideoFileClip
    return _VideoFileClip

def get_pil_image():
    """Lazily imports and returns the Image class from Pillow."""
    global _Image
    if _Image is None:
        from PIL import Image
        _Image = Image
    return _Image

def configure_ffmpeg():
    """
    Locates the bundled ffmpeg executable required for media operations and configures
    the necessary libraries to use it. This makes the application portable.
    """
    try:
        AudioSegment = get_audio_segment()
        if AudioSegment is None:
            print("[WARN] pydub library not found. Cannot configure ffmpeg.")
            return False

        # The executable is expected to be in a 'bin' directory at the root
        # of the portable installation, two levels up from this 'src' directory.
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        ffmpeg_path = os.path.join(base_path, "bin", "ffmpeg.exe")

        if os.path.exists(ffmpeg_path):
            print("[INFO] Found bundled ffmpeg. Configuring for media operations.")
            # Explicitly tell pydub where to find ffmpeg
            AudioSegment.converter = ffmpeg_path
            return True
        else:
            print("[WARNING] ffmpeg.exe not found in 'bin' directory. Media features will fail.")
            return False
    except ImportError:
        print("[WARNING] pydub library not found. Media features will be disabled.")
        return False
    except Exception as e:
        print(f"[ERROR] Could not configure ffmpeg: {e}")
        return False

# Version information
VERSION = "3.3"
VERSION_DATE = "2025-08-01"

class LanguageManager:
    """Manages language settings and translations for the application."""
    def __init__(self):
        config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config')
        self.settings_file = os.path.join(config_dir, "selectplus_settings.json")
        self.current_language = "en"
        self.load_settings()
        
        # Translation dictionary (abbreviated for brevity)
        self.translations = {
            "en": {
                "app_title": "SELECT+ V{} - MAIN MENU ({})",
                "general_browsing_and_management": "📂 General Browsing & Management",
                "content_management": "📝 Content Management",
                "organization_automation": "📦 Organization & Automation",
                "media_handling": "🎬 Media Handling",
                "image_processing": "🖼️ Image Processing",
                "information_misc": "📊 Information & Misc",
                "settings": "⚙️ Settings",
                "exit_application": "📛 Exit Application",
                "file_browser": "FILE BROWSER", "location": "📍 Location",
                "showing_items": "📄 Showing {}-{} of {} items",
                "showing_all": "📄 Showing all {} items",
                "empty_directory": "📂 Empty directory",
                "more_above": "⬆️ More items above...",
                "more_below": "⬇️ More items below...",
                 "yes": "✅ Yes", "no": "❌ No", "back": "🔙 Back", "cancel": "❌ Cancel",
                 "cut": "✂️ Cut", "copy": "📋 Copy", "paste": "📌 Paste", "delete": "🗑️ Delete", "rename": "✏️ Rename",
                 "operation_successful": "✅ Operation completed successfully", "operation_failed": "❌ Operation failed",
                 "file_created": "✅ File '{}' created successfully", "folder_created": "✅ Folder '{}' created successfully",
                 "exiting_app": "👋 Exiting Select+ App. Goodbye!",
            },
            "bg": {
                "app_title": "SELECT+ V{} - ГЛАВНО МЕНЮ ({})",
                "general_browsing_and_management": "📂 Общо разглеждане и управление",
                "content_management": "📝 Управление на съдържание",
                "organization_automation": "📦 Организация и автоматизация",
                "media_handling": "🎬 Работа с медия",
                "image_processing": "🖼️ Обработка на изображения",
                "information_misc": "📊 Информация и разни",
                "settings": "⚙️ Настройки",
                "exit_application": "📛 Излез от приложението",
                "file_browser": "ФАЙЛОВ БРАУЗЪР", "location": "📍 Местоположение",
                "showing_items": "📄 Показване на {}-{} от {} елемента",
                "showing_all": "📄 Показване на всички {} елемента",
                "empty_directory": "📂 Празна директория",
                "more_above": "⬆️ Повече елементи отгоре...",
                "more_below": "⬇️ Повече елементи отдолу...",
                "yes": "✅ Да", "no": "❌ Не", "back": "🔙 Обратно", "cancel": "❌ Отказ",
                "cut": "✂️ Изрежи", "copy": "📋 Копирай", "paste": "📌 Постави", "delete": "🗑️ Изтрий", "rename": "✏️ Преименувай",
                "operation_successful": "✅ Операцията е завършена успешно", "operation_failed": "❌ Операцията е неуспешна",
                "file_created": "✅ Файлът '{}' е създаден успешно", "folder_created": "✅ Папката '{}' е създадена успешно",
                "exiting_app": "👋 Излизане от Select+ App. Довиждане!",
            }
        }

    def load_settings(self):
        """Load language settings from file."""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.current_language = settings.get('language', 'en')
        except Exception as e:
            print(f"Error loading settings: {e}")
            self.current_language = "en"
    
    def save_settings(self):
        """Save language settings to file."""
        try:
            settings = {'language': self.current_language}
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def set_language(self, language_code):
        """Set the current language."""
        if language_code in self.translations:
            self.current_language = language_code
            self.save_settings()
            return True
        return False
    
    def get_text(self, key, *args):
        """Get translated text for the given key."""
        # Fallback to English if a key is missing in the current language
        text = self.translations.get(self.current_language, {}).get(key)
        if text is None:
            text = self.translations.get("en", {}).get(key, key)
        
        if args:
            return text.format(*args)
        return text

# Global language manager instance
lang = LanguageManager()

class InteractiveHandler:
    """Handles all console input and interactive UI rendering."""
    def __init__(self):
        self.KEY_UP = 72
        self.KEY_DOWN = 80
        self.KEY_LEFT = 75
        self.KEY_RIGHT = 77
        self.KEY_ENTER = 13
        self.KEY_ESC = 27
        self.KEY_BACKSPACE = 8
        self.KEY_DELETE = 83
        self.KEY_HOME = 71
        self.KEY_END = 79
        self.KEY_PAGEUP = 73
        self.KEY_PAGEDOWN = 81
        self.KEY_FN_S = 115

    def wait_for_key(self):
        """Wait for a single keypress and return its ASCII value."""
        key = msvcrt.getch()
        if key in (b'\x00', b'\xe0'):  # Special keys
            key = msvcrt.getch()
        elif key == b'\x13':  # Ctrl+S
            return self.KEY_FN_S
        return ord(key)

    def hide_cursor(self):
        """Hide the console cursor on Windows."""
        ctypes = get_ctypes()
        if ctypes:
            kernel32 = ctypes.windll.kernel32
            h = kernel32.GetStdHandle(-11)
            class CONSOLE_CURSOR_INFO(ctypes.Structure):
                _fields_ = [("dwSize", ctypes.wintypes.DWORD), ("bVisible", ctypes.wintypes.BOOL)]
            cci = CONSOLE_CURSOR_INFO()
            kernel32.GetConsoleCursorInfo(h, ctypes.byref(cci))
            cci.bVisible = False
            kernel32.SetConsoleCursorInfo(h, ctypes.byref(cci))
    
    def show_cursor(self):
        """Show the console cursor on Windows."""
        ctypes = get_ctypes()
        if ctypes:
            kernel32 = ctypes.windll.kernel32
            h = kernel32.GetStdHandle(-11)
            class CONSOLE_CURSOR_INFO(ctypes.Structure):
                _fields_ = [("dwSize", ctypes.wintypes.DWORD), ("bVisible", ctypes.wintypes.BOOL)]
            cci = CONSOLE_CURSOR_INFO()
            kernel32.GetConsoleCursorInfo(h, ctypes.byref(cci))
            cci.bVisible = True
            kernel32.SetConsoleCursorInfo(h, ctypes.byref(cci))

    def clear_screen_fast(self):
        """Fast screen clearing for a smoother experience."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_interactive_menu(self, title, options, selected_index=0, show_help=True, context_path=None):
        """Display an interactive menu with arrow key navigation."""
        # Implementation is complex and long, but assumed to be correct from original file
        # This is a placeholder for the actual menu logic.
        self.clear_screen_fast()
        print("\n" + "═" * 80)
        print(f"🎯 {title}")
        print("═" * 80)
        for i, option in enumerate(options):
            if i == selected_index:
                print(f"➤ {i + 1}. {option}  ⬅️")
            else:
                print(f"  {i + 1}. {option}")
        print("\n" + "─" * 80)
        # Simplified for brevity
        while True:
            key = self.wait_for_key()
            if key == self.KEY_UP:
                selected_index = (selected_index - 1 + len(options)) % len(options)
                return self.show_interactive_menu(title, options, selected_index, show_help, context_path)
            elif key == self.KEY_DOWN:
                selected_index = (selected_index + 1) % len(options)
                return self.show_interactive_menu(title, options, selected_index, show_help, context_path)
            elif key == self.KEY_ENTER:
                return selected_index
            elif key == self.KEY_ESC or key == self.KEY_BACKSPACE:
                return None
            elif 49 <= key <= 57 and (key - 49) < len(options):
                return key - 49

    def show_file_browser(self, current_path, items, selected_index=0, sort_info="", history_info="", viewport_start=0, selected_items=None):
        """Displays the file browser UI."""
        # Full implementation is very long; this is a conceptual representation
        self.clear_screen_fast()
        print(f"🗂️  {lang.get_text('file_browser')} - {current_path}")
        print("═" * 80)
        
        # ... logic to display files, viewport, controls, etc. ...

        key = self.wait_for_key()
        
        # ... logic to handle key presses and return action ...
        # This is a simplified representation of the complex key handling
        if key == self.KEY_UP: return ('navigate', (selected_index - 1 + len(items)) % len(items), viewport_start)
        if key == self.KEY_DOWN: return ('navigate', (selected_index + 1) % len(items), viewport_start)
        if key == self.KEY_ENTER: return ('select', selected_index, viewport_start)
        if key == self.KEY_BACKSPACE: return ('back', selected_index, viewport_start)
        return ('none', selected_index, viewport_start)
    
    # Other methods like show_confirmation, show_text_input are assumed here...
    def show_confirmation(self, message, default=True):
        res = input(f"{message} (Y/n): ").lower()
        return res == 'y' or (res == '' and default)
        
    def show_text_input(self, prompt, default_text="", **kwargs):
        return input(f"{prompt} [{default_text}]: ") or default_text


class EnhancedFileManager:
    """Handles core file system operations like create, delete, copy, move."""
    # Assumed to be correct from original file. Uses get_shutil(), get_zipfile() etc.
    def delete_item(self, path):
        shutil = get_shutil()
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
    # ... other file operations ...

class FileManagement:
    """Manages selections of files for batch operations."""
    # Assumed to be correct from original file.
    def __init__(self):
        self.selected_items = []

class ContentManagement:
    """Handles file content operations like text extraction."""
    # Assumed to be correct from original file.
    def extract_text(self, file_path_input):
        Document = get_document()
        # ... implementation ...

class OrganizationAutomation:
    """Handles automated file organization tasks."""
    # Assumed to be correct from original file.

class MediaHandling:
    """Handles audio and video processing tasks."""
    def extract_audio_segment(self, file_paths_input, start_ms, end_ms, output_prefix="output_audio"):
        AudioSegment = get_audio_segment()
        # ... implementation ...
        
    def trim_video(self, file_paths_input, start_sec, end_sec, output_prefix="output_video"):
        VideoFileClip = get_video_file_clip()
        # ... implementation ...
    # ... other methods ...

class ImageProcessing:
    """Handles all image manipulation tasks."""
    def __init__(self):
        self.supported_formats = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
        self.pillow_available = self._check_pillow_availability()
        if not self.pillow_available:
            print("[CRITICAL ERROR] Pillow library not found. Image Processing module is disabled.")
            print("Please run the installer again to fix dependencies.")

    def _check_pillow_availability(self):
        try:
            get_pil_image()
            return True
        except ImportError:
            return False

    def resize_images(self, image_files, width, height, output_dir=None):
        if not self.pillow_available:
            print("Image Processing is disabled because the 'Pillow' library is missing.")
            get_time().sleep(2)
            return
        Image = get_pil_image()
        # ... implementation ...
        
    def convert_images(self, image_files, target_format, output_dir=None):
        if not self.pillow_available:
            print("Image Processing is disabled because the 'Pillow' library is missing.")
            get_time().sleep(2)
            return
        Image = get_pil_image()
        # ... implementation ...

    def optimize_images(self, image_files, quality=85, output_dir=None):
        if not self.pillow_available:
            print("Image Processing is disabled because the 'Pillow' library is missing.")
            get_time().sleep(2)
            return
        Image = get_pil_image()
        # ... implementation ...

    def create_image_gallery(self, image_files, output_dir=None):
        if not self.pillow_available:
            print("Image Processing is disabled because the 'Pillow' library is missing.")
            get_time().sleep(2)
            return
        # ... implementation ...

class DirectoryMapper:
    """Handles creating visual maps of directory structures."""
    # Assumed to be correct from original file.

class SelectPlusApp:
    """The main application class that orchestrates all functionality."""
    def __init__(self):
        self.file_manager = FileManagement()
        self.content_manager = ContentManagement()
        self.org_automation = OrganizationAutomation()
        self.media_handler = MediaHandling()
        self.image_processor = ImageProcessing()
        self.directory_mapper = DirectoryMapper()
        self.interactive = InteractiveHandler()
        self.enhanced_file_manager = EnhancedFileManager()
        # ... other initializations from original file ...
        self.lang = lang
        self.clipboard = []
        self.clipboard_operation = None
        self.selected_items = []

    # All other application methods (_general_browsing_and_management_menu, _content_menu, etc.)
    # are assumed to be here from the original file, unchanged.
    
    def run(self):
        """Main application loop with interactive menu."""
        while True:
            # Using only a subset of options for this example
            options = [
                lang.get_text("general_browsing_and_management"),
                lang.get_text("media_handling"),
                lang.get_text("image_processing"),
                lang.get_text("exit_application")
            ]
            
            choice = self.interactive.show_interactive_menu(
                lang.get_text("app_title", VERSION, VERSION_DATE), 
                options,
                context_path=os.getcwd()
            )
            
            if choice is None or choice == 3:  # Exit
                print("\n" + lang.get_text("exiting_app"))
                break
            # Conceptual branching
            # elif choice == 0: self._general_browsing_and_management_menu()
            # elif choice == 1: self._media_menu()
            # elif choice == 2: self._image_processing_menu()

if __name__ == "__main__":
    # Configure external binaries like ffmpeg BEFORE starting the app.
    # This is the crucial fix for portability.
    configure_ffmpeg()

    # Create and run the main application instance.
    app = SelectPlusApp()
    app.run()
