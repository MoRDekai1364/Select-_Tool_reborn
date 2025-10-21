"""
Select+ V3.1 - Enhanced File Manager with Advanced Features

Version 3.1 Features:
- Interactive file browser with keyboard navigation
- Enhanced extension handling for file creation and renaming
- Context menu with all file operations (accessible via O key)
- Comprehensive file management tools
- Advanced search and organization capabilities
- Global search with Ctrl+S hotkey
- Enhanced search interface with multiple options
- Improved navigation history management

Author: Enhanced by AI Assistant
Date: 2025-07-18
"""

import os
import shutil
import zipfile
import re
import sys
import msvcrt
import threading
import time
import subprocess
import stat
import ctypes
import json
from datetime import datetime
from docx import Document # pip install python-docx
from pydub import AudioSegment # pip install pydub
from moviepy import VideoFileClip # pip install moviepy

# Version information
VERSION = "3.1"
VERSION_DATE = "2025-07-18"

class LanguageManager:
    """Manages language settings and translations for the application."""
    
    def __init__(self):
        self.settings_file = "selectplus_settings.json"
        self.current_language = "en"
        self.load_settings()
        
        # Translation dictionary
        self.translations = {
            "en": {
                # Main menu
                "app_title": "SELECT+ V{} - MAIN MENU ({})",
                "general_browsing_and_management": "📂 General Browsing & Management",
                "content_management": "📝 Content Management",
                "organization_automation": "📦 Organization & Automation",
                "media_handling": "🎬 Media Handling",
                "information_misc": "📊 Information & Misc",
                "settings": "⚙️ Settings",
                "exit_application": "📛 Exit Application",
                
                # Settings menu
                "settings_menu": "SETTINGS MENU",
                "browse_start_mode": "📁 Browse Start Mode",
                "language_settings": "🌐 Language Settings",
                "back_to_main": "🔙 Back to Main Menu",
                
                # Language settings
                "language_selection": "LANGUAGE SELECTION",
                "english": "🇺🇸 English",
                "bulgarian": "🇧🇬 Bulgarian",
                "language_changed": "✅ Language changed to: {}",
                "restart_required": "💡 Changes will take effect immediately",
                
                # Browse start mode
                "browse_start_selection": "Select File Browsing Start Mode",
                "default_drives": "Default (All Drives/Root)",
                "project_starting": "Project Starting Point",
                "custom_location": "Custom Location",
                
                # File browser
                "file_browser": "FILE BROWSER",
                "location": "📍 Location",
                "showing_items": "📄 Showing {}-{} of {} items",
                "showing_all": "📄 Showing all {} items",
                "empty_directory": "📂 Empty directory",
                "more_above": "⬆️ More items above...",
                "more_below": "⬇️ More items below...",
                
                # Controls
                "navigation_controls": "NAVIGATION CONTROLS",
                "sorting_controls": "SORTING",
                "action_controls": "ACTIONS",
                "multi_select_controls": "MULTI-SELECT",
                
                # Common buttons
                "yes": "✅ Yes",
                "no": "❌ No",
                "back": "🔙 Back",
                "cancel": "❌ Cancel",
                "ok": "✅ OK",
                "confirm": "✅ Confirm",
                
                # File operations
                "cut": "✂️ Cut",
                "copy": "📋 Copy",
                "copy_path": "📋 Copy Path",
                "paste": "📌 Paste",
                "delete": "🗑️ Delete",
                "rename": "✏️ Rename",
                "move": "📦 Move",
                "share": "🔗 Share",
                "run": "▶️ Run",
                "run_as_admin": "🔧 Run as Admin",
                "compress": "📦 Compress",
                "decompress": "📂 Decompress",
                "open_with": "🔗 Open With",
                "properties": "🔧 Properties",
                "create_shortcut": "🔗 Create Shortcut",
                "send_to": "📤 Send To",
                "new_file": "➕ New File",
                "new_folder": "📁 New Folder",
                
                # Messages
                "operation_successful": "✅ Operation completed successfully",
                "operation_failed": "❌ Operation failed",
                "file_created": "✅ File '{}' created successfully",
                "folder_created": "✅ Folder '{}' created successfully",
                "item_deleted": "✅ Deleted: {}",
                "item_moved": "✅ Moved '{}' to '{}'",
                "item_copied": "✅ Copied '{}' to '{}'",
                "exiting_app": "👋 Exiting Select+ App. Goodbye!",
                
                # Prompts
                "enter_filename": "Enter new file name (with extension)",
                "enter_foldername": "Enter new folder name",
                "enter_new_name": "Enter new name (supports extension changes)",
                "confirm_delete": "Delete {} '{}'?",
                "confirm_delete_multiple": "Delete {} selected items?",
                "select_directory": "Select directory '{}'?",
                
                # File types
                "file": "file",
                "folder": "folder",
                "directory": "directory",
                "items": "items",
                
                # Misc
                "press_enter": "Press Enter to continue...",
                "invalid_choice": "Invalid choice. Please try again.",
                "no_items_selected": "No items selected",
                "clipboard_empty": "Clipboard is empty",
                "multi_select_mode": "Multi-select mode: {}",
                "on": "ON",
                "off": "OFF",
                
                # Control explanations
                "controls_title": "🎮 CONTROLS:",
                "controls_navigation": "⬆️⬇️ Arrow keys - Navigate",
                "controls_enter": "↩️ Enter - Select",
                "controls_escape": "🔙 Esc/Backspace - Go back",
                "controls_numbers": "🔢 1-9 - Quick select",
                "controls_global_actions": "🔧 GLOBAL ACTIONS:",
                "controls_add_new": "➕ + - Add new file",
                "controls_delete": "🗑️ Del - Delete selected item",
                "controls_others": "🛠️ O - Others menu (all operations)",
                
                # File browser controls
                "nav_controls_title": "🎮 NAVIGATION CONTROLS:",
                "nav_arrow_keys": "⬆️⬇️ Arrow keys - Navigate items  ⬅️➡️ Back/Forward",
                "nav_enter": "↩️ Enter - Open folder/Select file",
                "nav_escape_home": "🔙 Esc/Backspace - Go back  🏠 Home - First item  📄 End - Last item",
                "sorting_title": "🔄 SORTING:",
                "sorting_commands": "sn-Name  ss-Size  sd-Date  st-Type  sr-Reverse  sh-Hidden",
                "actions_title": "🎯 ACTIONS:",
                "actions_commands": "s-Select dir  h-Home  v-Views  +-New  d-New Dir  del-Delete  o-Others  Shift+C-Copy Path  Shift+F-File Select  q-Quit",
                "multi_select_title": "🔄 MULTI-SELECT:",
                "multi_select_commands": "m-Toggle mode  space-Select/Deselect  c-Clear  a-Select all  n-Deselect all  i-Show info",
                
                # Confirmation dialog controls
                "confirm_controls_title": "🎮 CONTROLS:",
                "confirm_arrow_keys": "⬅️➡️ Arrow keys",
                "confirm_enter": "↩️ Enter",
                "confirm_escape": "🔙 Esc",
                
                # Input dialog
                "input_cancel": "💡 Press Esc to cancel",
                "input_options": "💡 Options:",
                "input_full_name": "• Enter full name with extension (e.g., 'newname.txt')",
                "input_name_only": "• Enter just the name (keeps current extension)",
                "input_ext_only": "• Enter just extension (e.g., '.pdf' to change extension only)",
                "input_esc_cancel": "• Press Esc to cancel",
                "current_name": "📝 Current name: {}",
                "current_extension": "📎 Current extension: {}",
                "no_extension": "(none)",
                
                # Content Management
                "content_management_title": "CONTENT MANAGEMENT",
                "extract_text_file": "📄 Extract Text from File",
                "extract_text_desc": "Extract readable text from .txt and .docx files",
                "find_replace_file": "🔍 Find/Replace in File",
                "find_replace_desc": "Search and replace text within files (.txt only)",
                "select_file_method": "SELECT FILE METHOD",
                "manually_enter_path": "✏️ Manually Enter Path",
                "browse_for_file": "🗂️ Browse for File",
                "extracted_content": "📄 EXTRACTED CONTENT",
                "showing_chars": "📊 Showing first {} of {} characters",
                "enter_find_string": "Enter string to find",
                "enter_replace_string": "Enter string to replace with",
                "confirm_replace": "Replace '{}' with '{}' in {}?",
                "find_replace_completed": "✅ Find/Replace operation completed",
                "no_search_string": "❌ No search string entered",
                "could_not_extract": "❌ Could not extract text from file",
                
                # Organization & Automation
                "organization_title": "ORGANIZATION & AUTOMATION",
                "organize_folders_rules": "📁 Organize Folders by Rules",
                "organize_folders_desc": "Sort files into folders based on file extensions",
                "create_zip_archives": "📦 Create Zip Archives",
                "create_zip_desc": "Compress selected files into ZIP archives",
                "select_folder_method": "SELECT FOLDER METHOD",
                "browse_for_folder": "🗂️ Browse for Folder",
                "enter_folder_path": "Enter folder path to organize",
                "enter_organization_rules": "Enter rules (e.g., txt:Text Files, jpg:Images). Do not use '.' for extensions:",
                "folder_organization_completed": "✅ Folder organization completed",
                "zip_creation_completed": "✅ Zip archive creation completed",
                "no_files_for_zipping": "⚠️ No files selected for zipping",
                "no_valid_rules": "❌ No valid rules entered",
                "no_rules_entered": "❌ No rules entered",
                
                # Media Handling
                "media_handling_title": "MEDIA HANDLING",
                "create_playlist": "🎵 Create Playlist",
                "create_playlist_desc": "Generate .m3u playlists from selected media files",
                "mass_extract_audio": "🔄 Mass Extract Audio Segments",
                "mass_extract_desc": "Extract audio segments from multiple media files",
                "mass_trim_videos": "✂️ Mass Trim Videos",
                "mass_trim_desc": "Trim video files to specified time ranges",
                "use_selected_files": "🗂️ Use Selected Files",
                "specify_new_file": "✏️ Specify New File",
                "enter_playlist_name": "Enter playlist filename (default 'playlist.m3u')",
                "playlist_created": "✅ Playlist created",
                "no_media_files": "⚠️ No media files selected for playlist creation",
                "enter_start_time_ms": "Enter start time in milliseconds",
                "enter_end_time_ms": "Enter end time in milliseconds",
                "enter_output_prefix_audio": "Enter output filename prefix (e.g., 'segment', default 'output_audio')",
                "audio_segments_extracted": "✅ Audio segments extracted",
                "enter_start_time_sec": "Enter start time in seconds (e.g., 5.5)",
                "enter_end_time_sec": "Enter end time in seconds (e.g., 60.0)",
                "enter_output_prefix_video": "Enter output filename prefix (e.g., 'trimmed', default 'output_video')",
                "videos_trimmed": "✅ Videos trimmed",
                "invalid_time_input": "❌ Invalid time input. Please enter numbers",
                "no_files_selected": "⚠️ No files currently selected",
                
                # Information & Misc
                "information_title": "INFORMATION & MISC",
                "calculate_size": "📏 Calculate Size",
                "calculate_size_desc": "Calculate total size of files and folders",
                "compare_sizes": "⚖️ Compare Sizes",
                "compare_sizes_desc": "Compare sizes between different files/folders",
                "add_file_description": "✏️ Add File Description",
                "add_desc_desc": "Add custom descriptions to files",
                "view_file_description": "🔍 View File Description",
                "view_desc_desc": "View custom descriptions for files",
                "directory_mapping": "📂 Directory Mapping",
                "directory_mapping_desc": "Generate detailed directory structure maps",
                "calculate_size_select": "CALCULATE SIZE - SELECT FILES",
                "browse_for_path": "🔍 Browse for Path",
                "manually_enter_paths": "✏️ Manually Enter Paths",
                "enter_paths_comma": "Enter paths (comma-separated, leave empty for current selection)",
                "total_size_result": "📏 Total size: {} bytes ({:.2f} GB)",
                "no_paths_for_calc": "⚠️ No paths specified or selected for size calculation",
                "compare_sizes_select": "COMPARE SIZES - SELECT COMPARISON PATH",
                "enter_comparison_path": "Enter path to compare with",
                "size_of_selection": "📏 Size of current selection: {} bytes ({:.2f} GB)",
                "size_of_comparison": "📏 Size of '{}': {} bytes ({:.2f} GB)",
                "selection_larger": "📊 Current selection is larger",
                "selection_smaller": "📊 Current selection is smaller",
                "sizes_equal": "📏 Sizes are equal",
                "no_items_for_comparison": "⚠️ No items selected for comparison",
                "comparison_path_not_found": "❌ Comparison path not found",
                "no_comparison_path": "⚠️ No comparison path selected",
                "add_description_select": "ADD FILE DESCRIPTION - SELECT FILE",
                "enter_file_path_desc": "Enter file path to add description to",
                "enter_description": "Enter description",
                "description_added": "✅ Description added for '{}'",
                "file_not_found": "❌ File not found",
                "view_description_select": "VIEW FILE DESCRIPTION - SELECT FILE",
                "enter_file_path_view": "Enter file path to view description",
                "description_for_file": "📄 Description for '{}': {}",
                "no_description_found": "❌ No description found for this file",
                "directory_mapping_select": "DIRECTORY MAPPING - SELECT DIRECTORY",
                "browse_for_directory": "🗺️ Browse for Directory",
                "enter_directory_path": "Enter directory path to map",
                "no_directory_selected": "⚠️ No directory selected",
                
                # General Browsing & Management
                "general_browsing_and_management_title": "GENERAL BROWSING & MANAGEMENT",
                "file_browsing": "📂 File Browsing",
                "select_files_folders": "📂 Select Files/Folders",
                "selected_files_operations": "📁 Selected Files Operations",
                "clear_current_selection": "🗑️ Clear Current Selection",
                "filter_selected_files": "🔍 Filter Selected Files",
                "secure_delete_selected": "🛡️ Secure Delete Selected Items",
                "mass_rename_selected": "🏷️ Mass Rename Selected Files",
                "cut_selected_items": "✂️ Cut Selected Items to Destination",
                "selected_files_operations_title": "SELECTED FILES OPERATIONS",
                "select_input_method": "SELECT INPUT METHOD",
                "manually_enter_paths": "✏️ Manually Enter Paths",
                "browse_for_paths": "🗂️ Browse for Paths",
                "enter_paths_comma_separated": "Enter paths (comma-separated, quotes optional)",
                "clear_all_selected": "Clear all selected items?",
                "no_items_selected_for_deletion": "No items selected for deletion",
                "items_to_be_deleted": "🛡️ ITEMS TO BE DELETED:",
                "permanently_delete_items": "PERMANENTLY DELETE {} items?",
                "no_items_selected_for_renaming": "No items selected for renaming",
                "enter_new_name_pattern": "Enter new name pattern (e.g., 'document_{num}', use {num} for numbering)",
                "enter_starting_number": "Enter starting number for rename",
                "no_items_selected_for_cutting": "No items selected for cutting",
                "cut_items_destination": "CUT ITEMS - DESTINATION METHOD",
                "enter_destination_folder": "Enter destination folder",
                "browse_for_destination": "🗂️ Browse for Path"
            },
            "bg": {
                # Main menu
                "app_title": "SELECT+ V{} - ГЛАВНО МЕНЮ ({})",
                "general_browsing_and_management": "📂 Общо разглеждане и управление",
                "content_management": "📝 Управление на съдържание",
                "organization_automation": "📦 Организация и автоматизация",
                "media_handling": "🎬 Работа с медия",
                "information_misc": "📊 Информация и разни",
                "settings": "⚙️ Настройки",
                "exit_application": "📛 Излез от приложението",
                
                # Settings menu
                "settings_menu": "МЕНЮ НАСТРОЙКИ",
                "browse_start_mode": "📁 Режим на започване",
                "language_settings": "🌐 Езикови настройки",
                "back_to_main": "🔙 Обратно към главното меню",
                
                # Language settings
                "language_selection": "ИЗБОР НА ЕЗИК",
                "english": "🇺🇸 Английски",
                "bulgarian": "🇧🇬 Български",
                "language_changed": "✅ Езикът е сменен на: {}",
                "restart_required": "💡 Промените ще влязат в сила незабавно",
                
                # Browse start mode
                "browse_start_selection": "Избор на начален режим за разглеждане",
                "default_drives": "По подразбиране (Всички дискове/Root)",
                "project_starting": "Начална точка на проекта",
                "custom_location": "Персонализирано място",
                
                # File browser
                "file_browser": "ФАЙЛОВ БРАУЗЪР",
                "location": "📍 Местоположение",
                "showing_items": "📄 Показване на {}-{} от {} елемента",
                "showing_all": "📄 Показване на всички {} елемента",
                "empty_directory": "📂 Празна директория",
                "more_above": "⬆️ Повече елементи отгоре...",
                "more_below": "⬇️ Повече елементи отдолу...",
                
                # Controls
                "navigation_controls": "КОНТРОЛИ ЗА НАВИГАЦИЯ",
                "sorting_controls": "СОРТИРАНЕ",
                "action_controls": "ДЕЙСТВИЯ",
                "multi_select_controls": "МУЛТИ-ИЗБОР",
                
                # Common buttons
                "yes": "✅ Да",
                "no": "❌ Не",
                "back": "🔙 Обратно",
                "cancel": "❌ Отказ",
                "ok": "✅ Добре",
                "confirm": "✅ Потвърди",
                
                # File operations
                "cut": "✂️ Изрежи",
                "copy": "📋 Копирай",
                "copy_path": "📋 Копирай път",
                "paste": "📌 Постави",
                "delete": "🗑️ Изтрий",
                "rename": "✏️ Преименувай",
                "move": "📦 Премести",
                "share": "🔗 Сподели",
                "run": "▶️ Изпълни",
                "run_as_admin": "🔧 Изпълни като администратор",
                "compress": "📦 Компресирай",
                "decompress": "📂 Декомпресирай",
                "open_with": "🔗 Отвори с",
                "properties": "🔧 Свойства",
                "create_shortcut": "🔗 Създай пряк път",
                "send_to": "📤 Изпрати до",
                "new_file": "➕ Нов файл",
                "new_folder": "📁 Нова папка",
                
                # Messages
                "operation_successful": "✅ Операцията е завършена успешно",
                "operation_failed": "❌ Операцията е неуспешна",
                "file_created": "✅ Файлът '{}' е създаден успешно",
                "folder_created": "✅ Папката '{}' е създадена успешно",
                "item_deleted": "✅ Изтрито: {}",
                "item_moved": "✅ Преместено '{}' в '{}'",
                "item_copied": "✅ Копирано '{}' в '{}'",
                "exiting_app": "👋 Излизане от Select+ App. Довиждане!",
                
                # Prompts
                "enter_filename": "Въведете име на новия файл (с разширение)",
                "enter_foldername": "Въведете име на новата папка",
                "enter_new_name": "Въведете ново име (поддържа промени в разширението)",
                "confirm_delete": "Изтрий {} '{}'?",
                "confirm_delete_multiple": "Изтрий {} избрани елемента?",
                "select_directory": "Избери директория '{}'?",
                
                # File types
                "file": "файл",
                "folder": "папка",
                "directory": "директория",
                "items": "елемента",
                
                # Misc
                "press_enter": "Натиснете Enter за да продължите...",
                "invalid_choice": "Невалиден избор. Моля опитайте отново.",
                "no_items_selected": "Няма избрани елементи",
                "clipboard_empty": "Клипбордът е празен",
                "multi_select_mode": "Режим мулти-избор: {}",
                "on": "ВКЛЮЧЕН",
                "off": "ИЗКЛЮЧЕН",
                
                # Control explanations
                "controls_title": "🎮 КОНТРОЛИ:",
                "controls_navigation": "⬆️⬇️ Стрелки - Навигация",
                "controls_enter": "↩️ Enter - Избор",
                "controls_escape": "🔙 Esc/Backspace - Назад",
                "controls_numbers": "🔢 1-9 - Бърз избор",
                "controls_global_actions": "🔧 ГЛОБАЛНИ ДЕЙСТВИЯ:",
                "controls_add_new": "➕ + - Добави нов файл",
                "controls_delete": "🗑️ Del - Изтрий избрания елемент",
                "controls_others": "🛠️ O - Меню други (всички операции)",
                
                # File browser controls
                "nav_controls_title": "🎮 КОНТРОЛИ ЗА НАВИГАЦИЯ:",
                "nav_arrow_keys": "⬆️⬇️ Стрелки - Навигация в елементи  ⬅️➡️ Назад/Напред",
                "nav_enter": "↩️ Enter - Отвори папка/Избери файл",
                "nav_escape_home": "🔙 Esc/Backspace - Назад  🏠 Home - Първи елемент  📄 End - Последен елемент",
                "sorting_title": "🔄 СОРТИРАНЕ:",
                "sorting_commands": "sn-Име  ss-Размер  sd-Дата  st-Тип  sr-Обратно  sh-Скрити",
                "actions_title": "🎯 ДЕЙСТВИЯ:",
                "actions_commands": "s-Избери дир  h-Начало  v-Изгледи  +-Нов файл  d-Нова дир  del-Изтрий  o-Други  cp-Копирай Път  fs-Избор Файл  q-Изход",
                "multi_select_title": "🔄 МУЛТИ-ИЗБОР:",
                "multi_select_commands": "m-Превключи режим  space-Избери/Отмени  c-Изчисти  i-Покажи инфо",
                
                # Confirmation dialog controls
                "confirm_controls_title": "🎮 КОНТРОЛИ:",
                "confirm_arrow_keys": "⬅️➡️ Стрелки",
                "confirm_enter": "↩️ Enter",
                "confirm_escape": "🔙 Esc",
                
                # Input dialog
                "input_cancel": "💡 Натиснете Esc за отказ",
                "input_options": "💡 Опции:",
                "input_full_name": "• Въведете пълно име с разширение (напр. 'новоиме.txt')",
                "input_name_only": "• Въведете само името (запазва текущото разширение)",
                "input_ext_only": "• Въведете само разширение (напр. '.pdf' за смяна само на разширението)",
                "input_esc_cancel": "• Натиснете Esc за отказ",
                "current_name": "📝 Текущо име: {}",
                "current_extension": "📎 Текущо разширение: {}",
                "no_extension": "(няма)",
                
                # General Browsing & Management
                "general_browsing_and_management_title": "ОБЩО РАЗГЛЕЖДАНЕ И УПРАВЛЕНИЕ",
                "file_browsing": "📂 Разглеждане на файлове",
                "select_files_folders": "📂 Избор на файлове/папки",
                "selected_files_operations": "📁 Операции с избрани файлове",
                "clear_current_selection": "🗑️ Изчистване на текущия избор",
                "filter_selected_files": "🔍 Филтриране на избрани файлове",
                "secure_delete_selected": "🛡️ Сигурно изтриване на избрани елементи",
                "mass_rename_selected": "🏷️ Масово преименуване на избрани файлове",
                "cut_selected_items": "✂️ Изрязване на избрани елементи към дестинация",
                "selected_files_operations_title": "ОПЕРАЦИИ С ИЗБРАНИ ФАЙЛОВЕ",
                "select_input_method": "ИЗБОР НА МЕТОД ЗА ВЪВЕЖДАНЕ",
                "manually_enter_paths": "✏️ Ръчно въвеждане на пътища",
                "browse_for_paths": "🗂️ Преглед за пътища",
                "enter_paths_comma_separated": "Въведете пътища (разделени със запетая, кавичките са по избор)",
                "clear_all_selected": "Изчистване на всички избрани елементи?",
                "no_items_selected_for_deletion": "Няма избрани елементи за изтриване",
                "items_to_be_deleted": "🛡️ ЕЛЕМЕНТИ ЗА ИЗТРИВАНЕ:",
                "permanently_delete_items": "ОКОНЧАТЕЛНО ИЗТРИВАНЕ НА {} елемента?",
                "no_items_selected_for_renaming": "Няма избрани елементи за преименуване",
                "enter_new_name_pattern": "Въведете нов образец за име (напр. 'документ_{num}', използвайте {num} за номериране)",
                "enter_starting_number": "Въведете начален номер за преименуване",
                "no_items_selected_for_cutting": "Няма избрани елементи за изрязване",
                "cut_items_destination": "ИЗРЯЗВАНЕ НА ЕЛЕМЕНТИ - МЕТОД ЗА ДЕСТИНАЦИЯ",
                "enter_destination_folder": "Въведете папка за дестинация",
                "browse_for_destination": "🗂️ Преглед за път",
                
                # Content Management
                "content_management_title": "УПРАВЛЕНИЕ НА СЪДЪРЖАНИЕ",
                "extract_text_file": "📄 Извличане на текст от файл",
                "extract_text_desc": "Извличане на четим текст от .txt и .docx файлове",
                "find_replace_file": "🔍 Търсене/замяна във файл",
                "find_replace_desc": "Търсене и замяна на текст във файлове (само .txt)",
                "select_file_method": "МЕТОД ЗА ИЗБОР НА ФАЙЛ",
                "manually_enter_path": "✏️ Ръчно въвеждане на път",
                "browse_for_file": "🗂️ Преглед за файл",
                "extracted_content": "📄 ИЗВЛЕЧЕНО СЪДЪРЖАНИЕ",
                "showing_chars": "📊 Показване на първите {} от {} символа",
                "enter_find_string": "Въведете низ за търсене",
                "enter_replace_string": "Въведете низ за замяна",
                "confirm_replace": "Замяна на '{}' с '{}' в {}?",
                "find_replace_completed": "✅ Операцията за търсене/замяна е завършена",
                "no_search_string": "❌ Няма въведен низ за търсене",
                "could_not_extract": "❌ Не може да се извлече текст от файла"
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
        text = self.translations.get(self.current_language, {}).get(key, key)
        if args:
            return text.format(*args)
        return text
    
    def get_available_languages(self):
        """Get list of available languages."""
        return {
            'en': 'English',
            'bg': 'Български'
        }

# Global language manager instance
lang = LanguageManager()

class InteractiveHandler:
    """
    Enhanced interactive input handler with keyboard navigation and mouse support.
    Provides arrow key navigation, Enter/Escape/Backspace/Delete functionality.
    """
    
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
        self.KEY_F1 = 59
        self.KEY_F2 = 60
        self.KEY_F3 = 61
        self.KEY_F4 = 62
        self.KEY_F5 = 63
        self.KEY_F6 = 64
        self.KEY_F7 = 65
        self.KEY_F8 = 66
        self.KEY_F9 = 67
        self.KEY_F10 = 68
        self.KEY_F11 = 69
        self.KEY_F12 = 70
        self.KEY_FN_S = 115  # Fn+S combination (will be detected as F key + S)
        
    def get_key(self):
        """Get a single keypress from the user."""
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'\x00' or key == b'\xe0':  # Special keys
                key = msvcrt.getch()
                return ord(key)
            return ord(key)
        return None
    
    def wait_for_key(self):
        """Wait for a single keypress and return it."""
        while True:
            key = msvcrt.getch()
            if key == b'\x00' or key == b'\xe0':  # Special keys or Function key combinations
                next_key = msvcrt.getch()
                # Check for Fn+S (Function key combinations - this is approximate)
                # Note: Fn+S detection varies by keyboard, so we'll also check for Ctrl+S as alternative
                return ord(next_key)
            # Check for Ctrl+S as an alternative to Fn+S (more reliable)
            elif key == b'\x13':  # Ctrl+S
                return self.KEY_FN_S
            return ord(key)
    
    def hide_cursor(self):
        """Hide the console cursor."""
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.GetStdHandle.restype = ctypes.wintypes.HANDLE
            kernel32.GetStdHandle.argtypes = [ctypes.wintypes.DWORD]
            h = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
            
            class CONSOLE_CURSOR_INFO(ctypes.Structure):
                _fields_ = [("dwSize", ctypes.wintypes.DWORD),
                           ("bVisible", ctypes.wintypes.BOOL)]
            
            cci = CONSOLE_CURSOR_INFO()
            kernel32.GetConsoleCursorInfo(h, ctypes.byref(cci))
            cci.bVisible = False
            kernel32.SetConsoleCursorInfo(h, ctypes.byref(cci))
        except:
            pass  # If it fails, just continue without hiding cursor
    
    def show_cursor(self):
        """Show the console cursor."""
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.GetStdHandle.restype = ctypes.wintypes.HANDLE
            kernel32.GetStdHandle.argtypes = [ctypes.wintypes.DWORD]
            h = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
            
            class CONSOLE_CURSOR_INFO(ctypes.Structure):
                _fields_ = [("dwSize", ctypes.wintypes.DWORD),
                           ("bVisible", ctypes.wintypes.BOOL)]
            
            cci = CONSOLE_CURSOR_INFO()
            kernel32.GetConsoleCursorInfo(h, ctypes.byref(cci))
            cci.bVisible = True
            kernel32.SetConsoleCursorInfo(h, ctypes.byref(cci))
        except:
            pass  # If it fails, just continue
    
    def show_interactive_menu(self, title, options, selected_index=0, show_help=True, context_path=None):
        """
        Display an interactive menu with arrow key navigation.
        
        Args:
            title: Menu title
            options: List of menu options
            selected_index: Initially selected option
            show_help: Whether to show help text
            context_path: Path for context operations (delete, add new, etc.)
        
        Returns:
            Selected option index or special command string
        """
        while True:
            # Clear screen
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Display title
            print("\n" + "═" * 80)
            print(f"🎯 {title}")
            print("═" * 80)
            
            # Display options
            for i, option in enumerate(options):
                if i == selected_index:
                    print(f"➤ {i + 1}. {option}  ⬅️")
                else:
                    print(f"  {i + 1}. {option}")
            
            # Display help
            if show_help:
                print("\n" + "─" * 80)
                print(lang.get_text("controls_title"))
                print("  " + lang.get_text("controls_navigation"))
                print("  " + lang.get_text("controls_enter"))
                print("  " + lang.get_text("controls_escape"))
                print("  " + lang.get_text("controls_numbers"))
                if context_path:
                    print("\n" + lang.get_text("controls_global_actions"))
                    print("  " + lang.get_text("controls_add_new"))
                    print("  " + lang.get_text("controls_delete"))
                    print("  " + lang.get_text("controls_others"))
                print("─" * 80)
            
            # Get user input
            key = self.wait_for_key()
            
            if key == self.KEY_UP:
                selected_index = (selected_index - 1) % len(options)
            elif key == self.KEY_DOWN:
                selected_index = (selected_index + 1) % len(options)
            elif key == self.KEY_ENTER:
                return selected_index
            elif key == self.KEY_ESC or key == self.KEY_BACKSPACE:
                return None
            elif key == self.KEY_HOME:
                selected_index = 0
            elif key == self.KEY_END:
                selected_index = len(options) - 1
            elif key == ord('+') and context_path:
                return 'GLOBAL_ADD_NEW'
            elif (key == 127 or key == 46) and context_path:  # Delete key
                return 'GLOBAL_DELETE'
            elif (key == ord('o') or key == ord('O')) and context_path:
                return 'GLOBAL_OTHERS'
            elif 49 <= key <= 57:  # Number keys 1-9
                num = key - 48
                if 1 <= num <= len(options):
                    return num - 1
    
    def show_file_browser(self, current_path, items, selected_index=0, sort_info="", history_info="", viewport_start=0, selected_items=None):
        """
        Display enhanced file browser with keyboard navigation and proper viewport management.
        
        Args:
            current_path: Current directory path
            items: List of (name, type, details) tuples
            selected_index: Currently selected item
            sort_info: Sorting information string
            history_info: History information string
            viewport_start: Starting index for viewport display
        
        Returns:
            Tuple of (action, selected_index, viewport_start) where action is:
            - 'select': User pressed Enter on selected item
            - 'back': User pressed Esc/Backspace
            - 'navigate': Navigate to new position
            - 'command': User pressed a command key (returns command)
        """
        self.hide_cursor()
        
        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Calculate viewport settings
        max_display_items = 15  # Maximum items to show on screen
        total_items = len(items)
        
        # Adjust viewport to keep selected item visible
        if selected_index < viewport_start:
            viewport_start = selected_index
        elif selected_index >= viewport_start + max_display_items:
            viewport_start = selected_index - max_display_items + 1
        
        # Ensure viewport doesn't go out of bounds
        viewport_start = max(0, min(viewport_start, total_items - max_display_items))
        if total_items <= max_display_items:
            viewport_start = 0
        
        viewport_end = min(viewport_start + max_display_items, total_items)
        
        # Display header
        print("═" * 80)
        print(f"🗂️  {lang.get_text('file_browser')} - {current_path}")
        print("═" * 80)
        
        # Show breadcrumb and info
        path_parts = current_path.split(os.sep)
        breadcrumb = " → ".join(path_parts[-3:]) if len(path_parts) > 3 else current_path
        print(f"{lang.get_text('location')}: {breadcrumb}")
        print(f"📊 {history_info}")
        print(f"🔤 {sort_info}")
        
        # Show viewport info
        if total_items > max_display_items:
            print(lang.get_text("showing_items", viewport_start + 1, viewport_end, total_items))
        else:
            print(lang.get_text("showing_all", total_items))
        
        print("─" * 80)
        
        # Display items in viewport
        if not items:
            print(lang.get_text("empty_directory"))
        else:
            # Show scroll indicator at top
            if viewport_start > 0:
                print("   " + lang.get_text("more_above"))
            
            for i in range(viewport_start, viewport_end):
                name, item_type, details = items[i]
                
                if item_type == "dir":
                    icon = "📁" if name != ".." else "⬆️"
                    type_indicator = "DIR"
                else:
                    # Get file icon based on extension
                    ext = os.path.splitext(name)[1].lower()
                    file_icons = {
                        '.txt': '📄', '.py': '🐍', '.js': '🟨', '.html': '🌐',
                        '.mp3': '🎵', '.mp4': '🎬', '.jpg': '🖼️', '.png': '🖼️',
                        '.zip': '📦', '.exe': '⚙️', '.log': '📜'
                    }
                    icon = file_icons.get(ext, '📄')
                    type_indicator = "FILE"
                
                # Highlight selected item and show multi-selection
                item_path = os.path.join(current_path, name) if current_path != "__DRIVES__" else name
                is_in_selection = selected_items and os.path.abspath(item_path) in selected_items
                
                if i == selected_index:
                    if is_in_selection:
                        print(f"➤ {i:2d}. {icon} {name:<30} [{type_indicator:>4}] {details:>12} ✅⬅️")
                    else:
                        print(f"➤ {i:2d}. {icon} {name:<30} [{type_indicator:>4}] {details:>12}  ⬅️")
                else:
                    if is_in_selection:
                        print(f"  {i:2d}. {icon} {name:<30} [{type_indicator:>4}] {details:>12} ✅")
                    else:
                        print(f"  {i:2d}. {icon} {name:<30} [{type_indicator:>4}] {details:>12}")
            
            # Show scroll indicator at bottom
            if viewport_end < total_items:
                print("   " + lang.get_text("more_below"))
        
        # Display controls
        print("─" * 80)
        print(lang.get_text("nav_controls_title"))
        print("  " + lang.get_text("nav_arrow_keys"))
        print("  " + lang.get_text("nav_enter"))
        print("  " + lang.get_text("nav_escape_home"))
        print("")
        print(lang.get_text("sorting_title") + " " + lang.get_text("sorting_commands"))
        print(lang.get_text("actions_title") + " " + lang.get_text("actions_commands"))
        print(lang.get_text("multi_select_title") + " " + lang.get_text("multi_select_commands"))
        print("🔍 SEARCH: Ctrl+S-Global Search")
        print("─" * 80)
        
        # Get user input
        key = self.wait_for_key()
        
        if key == self.KEY_UP:
            new_index = (selected_index - 1) % len(items) if items else 0
            return ('navigate', new_index, viewport_start)
        elif key == self.KEY_DOWN:
            new_index = (selected_index + 1) % len(items) if items else 0
            return ('navigate', new_index, viewport_start)
        elif key == self.KEY_LEFT:
            return ('back', selected_index, viewport_start)
        elif key == self.KEY_RIGHT:
            return ('select', selected_index, viewport_start)
        elif key == self.KEY_ENTER:
            return ('select', selected_index, viewport_start)
        elif key == self.KEY_ESC or key == self.KEY_BACKSPACE:
            return ('back', selected_index, viewport_start)
        elif key == self.KEY_FN_S:
            return ('command', 'global_search', viewport_start)
        elif key == self.KEY_HOME:
            return ('navigate', 0, 0)
        elif key == self.KEY_END:
            return ('navigate', len(items) - 1 if items else 0, viewport_start)
        elif key == self.KEY_PAGEUP:
            new_index = max(0, selected_index - 10)
            return ('navigate', new_index, viewport_start)
        elif key == self.KEY_PAGEDOWN:
            new_index = min(len(items) - 1, selected_index + 10) if items else 0
            return ('navigate', new_index, viewport_start)
        elif 49 <= key <= 57:  # Number keys 1-9
            num = key - 48
            if 1 <= num <= len(items):
                return ('select', num - 1, viewport_start)
        else:
            # Handle command keys
            if key == ord('+'):
                return ('command', 'new_item_menu', viewport_start)
            elif key == 127 or key == 46:  # Delete key or Del key
                return ('command', 'delete', viewport_start)
            elif key == 32:  # Space key for multi-select
                return ('command', 'toggle_select', viewport_start)
            
            char = chr(key).lower()
            if char in ['s', 'h', 'v', 'q']:
                return ('command', char, viewport_start)
            elif char == 'n':  # Check for 'sn' command
                return ('command', 'sn', viewport_start)
            elif char == 'c':  # Context menu
                return ('command', 'context', viewport_start)
            elif char == 'd':  # New directory
                return ('command', 'new_dir', viewport_start)
            elif char == 'x':  # Delete
                return ('command', 'delete', viewport_start)
            elif char == 'r':  # Run
                return ('command', 'run', viewport_start)
            elif char == 'p':  # Properties
                return ('command', 'properties', viewport_start)
            elif char == 'o':  # Others menu (context menu)
                return ('command', 'context', viewport_start)
            elif char == 'm':  # Toggle multi-select mode
                return ('command', 'multi_mode', viewport_start)
            elif char == 'i':  # Show selection info
                return ('command', 'selection_info', viewport_start)
            elif char == 'a':  # Select all
                return ('command', 'select_all', viewport_start)
            elif char == 'n':  # Deselect all (new command)
                return ('command', 'deselect_all', viewport_start)
            elif char == 'c':  # Handle 'c' commands (context or clear selection)
                return ('command', 'clear_selection', viewport_start)
            elif char == 'f':  # Handle 'f' commands (new file)
                return ('command', 'new_file', viewport_start)
            # Handle Shift+C for copy path
            elif key == 67:  # Shift+C (uppercase C)
                return ('command', 'copy_path', viewport_start)
            # Handle Shift+F for file select
            elif key == 70:  # Shift+F (uppercase F)
                return ('command', 'file_select', viewport_start)
            # Add more command handling as needed
        
        return ('none', selected_index, viewport_start)
    
    def show_confirmation(self, message, default=True):
        """
        Show a confirmation dialog.
        
        Args:
            message: Confirmation message
            default: Default choice (True for Yes, False for No)
        
        Returns:
            True if Yes, False if No
        """
        selected = 0 if default else 1
        options = [lang.get_text("yes"), lang.get_text("no")]
        
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print("\n" + "═" * 60)
            print(f"❓ {message}")
            print("═" * 60)
            
            for i, option in enumerate(options):
                if i == selected:
                    print(f"➤ {option}  ⬅️")
                else:
                    print(f"  {option}")
            
            print("\n" + "─" * 60)
            print(lang.get_text("confirm_controls_title") + " " + lang.get_text("confirm_arrow_keys") + "  " + lang.get_text("confirm_enter") + "  " + lang.get_text("confirm_escape"))
            print("─" * 60)
            
            key = self.wait_for_key()
            
            if key == self.KEY_LEFT or key == self.KEY_RIGHT:
                selected = 1 - selected
            elif key == self.KEY_ENTER:
                return selected == 0
            elif key == self.KEY_ESC:
                return False
            elif key == ord('y') or key == ord('Y'):
                return True
            elif key == ord('n') or key == ord('N'):
                return False
    
    def show_text_input(self, prompt, default_text="", allow_extension_change=False):
        """
        Show a text input dialog with optional extension handling.
        
        Args:
            prompt: Input prompt
            default_text: Default text
            allow_extension_change: Whether to allow extension modification
        
        Returns:
            Entered text or None if cancelled
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("\n" + "═" * 70)
        print(f"✏️ {prompt}")
        print("═" * 70)
        
        if allow_extension_change and default_text:
            name_part, ext_part = os.path.splitext(default_text)
            print(lang.get_text("current_name", name_part))
            print(lang.get_text("current_extension", ext_part if ext_part else lang.get_text("no_extension")))
            print("")
            print(lang.get_text("input_options"))
            print("  " + lang.get_text("input_full_name"))
            print("  " + lang.get_text("input_name_only"))
            print("  " + lang.get_text("input_ext_only"))
            print("  " + lang.get_text("input_esc_cancel"))
        else:
            print(lang.get_text("input_cancel"))
        
        print("─" * 70)
        
        try:
            result = input("➤ ")
            
            if not result:
                return default_text
            
            # Handle extension change logic
            if allow_extension_change and default_text:
                name_part, ext_part = os.path.splitext(default_text)
                
                if result.startswith('.'):
                    # User entered just an extension (e.g., '.pdf')
                    return name_part + result
                elif '.' not in result:
                    # User entered just a name, keep current extension
                    return result + ext_part
                else:
                    # User entered full name with extension
                    return result
            
            return result
        except KeyboardInterrupt:
            return None

class EnhancedFileManager:
    """Enhanced file management operations with advanced features."""
    
    def __init__(self):
        pass

    def create_file(self, path, filename):
        """Create a new file at the specified path."""
        try:
            full_path = os.path.join(path, filename)
            with open(full_path, 'w') as f:
                f.write("")
            print(f"✅ File '{filename}' created successfully.")
            return full_path
        except Exception as e:
            print(f"❌ Error creating file: {e}")
            return None

    def create_folder(self, path, foldername):
        """Create a new folder at the specified path."""
        try:
            full_path = os.path.join(path, foldername)
            os.makedirs(full_path, exist_ok=True)
            print(f"✅ Folder '{foldername}' created successfully.")
            return full_path
        except Exception as e:
            print(f"❌ Error creating folder: {e}")
            return None

    def delete_item(self, path):
        """Delete a file or directory."""
        try:
            if os.path.isfile(path):
                os.remove(path)
                print(f"✅ Deleted file: {os.path.basename(path)}")
            elif os.path.isdir(path):
                shutil.rmtree(path)
                print(f"✅ Deleted directory: {os.path.basename(path)}")
            else:
                print("❌ Path does not exist.")
                return False
            return True
        except Exception as e:
            print(f"❌ Error deleting: {e}")
            return False

    def move_item(self, source, destination):
        """Move a file or directory."""
        try:
            shutil.move(source, destination)
            print(f"✅ Moved '{os.path.basename(source)}' to '{destination}'")
            return True
        except Exception as e:
            print(f"❌ Error moving: {e}")
            return False

    def copy_item(self, source, destination):
        """Copy a file or directory."""
        try:
            if os.path.isfile(source):
                shutil.copy2(source, destination)
            elif os.path.isdir(source):
                shutil.copytree(source, destination)
            print(f"✅ Copied '{os.path.basename(source)}' to '{destination}'")
            return True
        except Exception as e:
            print(f"❌ Error copying: {e}")
            return False

    def compress_items(self, paths, archive_name):
        """Compress files into a zip archive."""
        try:
            with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for path in paths:
                    if os.path.isfile(path):
                        zipf.write(path, os.path.basename(path))
                    elif os.path.isdir(path):
                        for root, _, files in os.walk(path):
                            for file in files:
                                full_path = os.path.join(root, file)
                                arc_name = os.path.relpath(full_path, os.path.dirname(path))
                                zipf.write(full_path, arc_name)
            print(f"✅ Compressed into archive: {archive_name}")
            return True
        except Exception as e:
            print(f"❌ Error compressing: {e}")
            return False

    def decompress_archive(self, archive_path, extract_to):
        """Decompress a zip archive."""
        try:
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                zipf.extractall(extract_to)
            print(f"✅ Decompressed into: {extract_to}")
            return True
        except Exception as e:
            print(f"❌ Error decompressing: {e}")
            return False

    def run_file(self, path):
        """Run a file using the default system application."""
        try:
            if os.name == 'nt':
                os.startfile(path)
            else:
                subprocess.run(['open', path]) if sys.platform == 'darwin' else subprocess.run(['xdg-open', path])
            print(f"✅ Running '{os.path.basename(path)}'")
            return True
        except Exception as e:
            print(f"❌ Error running file: {e}")
            return False

    def run_as_admin(self, path):
        """Run a file as an administrator (Windows only)."""
        try:
            if os.name == 'nt':
                ctypes.windll.shell32.ShellExecuteW(None, "runas", path, None, None, 1)
                print(f"✅ Running '{os.path.basename(path)}' as admin")
                return True
            else:
                print("❌ Run as admin is only supported on Windows")
                return False
        except Exception as e:
            print(f"❌ Error running as admin: {e}")
            return False

    def get_file_properties(self, path):
        """Get detailed properties of a file or directory."""
        try:
            stat_info = os.stat(path)
            properties = {
                'name': os.path.basename(path),
                'path': path,
                'size': stat_info.st_size,
                'created': datetime.fromtimestamp(stat_info.st_ctime),
                'modified': datetime.fromtimestamp(stat_info.st_mtime),
                'accessed': datetime.fromtimestamp(stat_info.st_atime),
                'is_dir': os.path.isdir(path),
                'is_file': os.path.isfile(path),
                'permissions': stat.filemode(stat_info.st_mode)
            }
            return properties
        except Exception as e:
            print(f"❌ Error getting properties: {e}")
            return None

    def show_properties(self, path):
        """Display file properties in a formatted way."""
        props = self.get_file_properties(path)
        if props:
            print("\n" + "═" * 60)
            print(f"🔍 PROPERTIES: {props['name']}")
            print("═" * 60)
            print(f"📁 Path: {props['path']}")
            print(f"📊 Size: {props['size']:,} bytes")
            print(f"📅 Created: {props['created']}")
            print(f"📝 Modified: {props['modified']}")
            print(f"👁️ Accessed: {props['accessed']}")
            print(f"🔐 Permissions: {props['permissions']}")
            print(f"📂 Type: {'Directory' if props['is_dir'] else 'File'}")
            print("─" * 60)

class FileManagement:
    def __init__(self):
        self.selected_items = []

    def _normalize_path(self, path):
        """removes quotes and strips whitespace from a path."""
        return path.strip().strip('"')

    def select_items(self, paths_input):
        paths = [self._normalize_path(p) for p in paths_input.split(',')]
        for path in paths:
            if os.path.exists(path):
                # Add absolute path to ensure consistency
                self.selected_items.append(os.path.abspath(path))
                print(f"selected: {os.path.abspath(path)}")
            else:
                print(f"path not found: {path}")

    def clear_selection(self):
        self.selected_items = []
        print("selection cleared.")

    def filter_files(self, extensions=None, min_size=0, max_size=float('inf')):
        filtered = []
        for item in self.selected_items:
            if os.path.isfile(item):
                if extensions and not any(item.lower().endswith(ext.lower()) for ext in extensions):
                    continue
                try:
                    size = os.path.getsize(item)
                    if not (min_size <= size <= max_size):
                        continue
                except OSError as e:
                    print(f"could not get size for {item}: {e}")
                    continue
                filtered.append(item)
        self.selected_items = filtered
        print(f"filtered selection to {len(self.selected_items)} files.")

    def secure_delete(self, paths):
        # operate on a copy of paths to avoid issues if selected_items is cleared during iteration
        for path_to_delete in list(paths):
            path = self._normalize_path(path_to_delete)
            if not os.path.exists(path):
                print(f"path not found for secure deletion: {path}")
                continue

            if os.path.isfile(path):
                try:
                    file_size = os.path.getsize(path)
                    # Overwrite file with random data
                    with open(path, 'r+b') as f:
                        f.write(os.urandom(file_size))
                    os.remove(path)
                    print(f"securely deleted file: {path}")
                    # Remove from selected_items if it was part of it
                    if path in self.selected_items:
                        self.selected_items.remove(path)
                except OSError as e:
                    print(f"error securely deleting file {path}: {e}")
            elif os.path.isdir(path):
                try:
                    for root, dirs, files in os.walk(path, topdown=False):
                        for name in files:
                            file_path = os.path.join(root, name)
                            if os.path.exists(file_path): # Check if file exists before trying to get size
                                file_size = os.path.getsize(file_path)
                                with open(file_path, 'r+b') as f:
                                    f.write(os.urandom(file_size))
                                os.remove(file_path)
                        for name in dirs:
                            os.rmdir(os.path.join(root, name))
                    os.rmdir(path)
                    print(f"securely deleted directory: {path}")
                    # Remove any selected items that were inside this directory
                    self.selected_items = [item for item in self.selected_items if not item.startswith(path)]
                except OSError as e:
                    print(f"error securely deleting directory {path}: {e}")
            else:
                print(f"unsupported path type for secure deletion: {path}")


    def mass_rename(self, new_name_pattern, start_num=1):
        if not self.selected_items:
            print("no items selected for renaming.")
            return

        # Create a copy of selected_items to iterate over, as list might change
        items_to_rename = list(self.selected_items)
        self.selected_items.clear() # Clear existing selection, will repopulate with new names

        for i, item in enumerate(items_to_rename):
            item_normalized = self._normalize_path(item)
            if not os.path.exists(item_normalized):
                print(f"skipped renaming, path not found: {item_normalized}")
                continue

            directory, old_name = os.path.split(item_normalized)
            name_without_ext, ext = os.path.splitext(old_name)

            try:
                # ensure unique names even if pattern doesn't use {num}
                if '{num}' in new_name_pattern:
                    new_name = new_name_pattern.format(num=start_num + i) + ext
                else:
                    new_name = f"{new_name_pattern}_{start_num + i}{ext}" # Fallback for non-{num} patterns

                new_path = os.path.join(directory, new_name)

                # Handle potential name collision before moving
                counter = 0
                original_new_path = new_path
                while os.path.exists(new_path) and new_path != item_normalized: # Avoid collision with itself
                    counter += 1
                    name_part, ext_part = os.path.splitext(original_new_path)
                    new_path = f"{name_part}_{counter}{ext_part}"

                shutil.move(item_normalized, new_path)
                print(f"renamed '{old_name}' to '{os.path.basename(new_path)}'")
                self.selected_items.append(new_path) # Add new path to selection
            except Exception as e:
                print(f"error renaming '{old_name}': {e}")


    def cut_selected(self, destination_folder_input):
        if not self.selected_items:
            print("no items selected for cutting.")
            return

        destination_folder = self._normalize_path(destination_folder_input)
        if not os.path.exists(destination_folder):
            try:
                os.makedirs(destination_folder)
                print(f"created destination folder: {destination_folder}")
            except OSError as e:
                print(f"error creating destination folder {destination_folder}: {e}")
                return

        moved_items = []
        # Iterate over a copy of selected_items as it will be modified
        for item in list(self.selected_items):
            item_normalized = self._normalize_path(item)
            if not os.path.exists(item_normalized):
                print(f"skipped moving, path not found: {item_normalized}")
                continue
            try:
                # Get the base name of the item to avoid issues with source folder structure
                dest_item_path = os.path.join(destination_folder, os.path.basename(item_normalized))
                shutil.move(item_normalized, dest_item_path)
                print(f"moved '{item_normalized}' to '{dest_item_path}'")
                moved_items.append(item_normalized)
            except shutil.Error as e:
                print(f"error moving '{item_normalized}': {e}")
            except Exception as e:
                print(f"an unexpected error occurred while moving '{item_normalized}': {e}")

        # Remove successfully moved items from selected_items
        self.selected_items = [item for item in self.selected_items if item not in moved_items]


    def calculate_size(self, paths_input):
        paths = [self._normalize_path(p) for p in paths_input]
        total_size = 0
        for path in paths:
            if not os.path.exists(path):
                print(f"path not found for size calculation: {path}")
                continue
            try:
                if os.path.isfile(path):
                    total_size += os.path.getsize(path)
                elif os.path.isdir(path):
                    for dirpath, dirnames, filenames in os.walk(path):
                        for f in filenames:
                            fp = os.path.join(dirpath, f)
                            if os.path.exists(fp):
                                total_size += os.path.getsize(fp)
            except OSError as e:
                print(f"error calculating size for {path}: {e}")
        return total_size # Returns size in bytes

class ContentManagement:
    def _normalize_path(self, path):
        return path.strip().strip('"')

    def extract_text(self, file_path_input):
        file_path = self._normalize_path(file_path_input)
        if not os.path.exists(file_path):
            print(f"file not found: {file_path}")
            return None

        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        if ext == '.txt':
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                print(f"extracted text from: {file_path}")
                return content
            except UnicodeDecodeError:
                try:
                    with open(file_path, 'r', encoding='latin-1') as f:
                        content = f.read()
                    print(f"extracted text from: {file_path} (latin-1 encoding)")
                    return content
                except Exception as e:
                    print(f"error extracting text from {file_path} (tried multiple encodings): {e}")
                    return None
            except Exception as e:
                print(f"error extracting text from {file_path}: {e}")
                return None
        elif ext == '.docx':
            try:
                doc = Document(file_path)
                full_text = []
                for para in doc.paragraphs:
                    full_text.append(para.text)
                print(f"extracted text from word document: {file_path}")
                return '\n'.join(full_text)
            except Exception as e:
                print(f"error extracting text from docx {file_path}: {e}")
                return None
        else:
            print(f"unsupported file type for text extraction: {ext}")
            return None

    def find_replace_in_file(self, file_path_input, find_str, replace_str):
        file_path = self._normalize_path(file_path_input)
        if not os.path.exists(file_path):
            print(f"file not found: {file_path}")
            return

        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        if ext == '.txt':
            try:
                # Read content with multiple encoding attempts
                content = None
                for encoding in ['utf-8', 'latin-1', 'cp1252']:
                    try:
                        with open(file_path, 'r', encoding=encoding) as f:
                            content = f.read()
                        break # Successfully read, break from loop
                    except UnicodeDecodeError:
                        continue # Try next encoding

                if content is None:
                    print(f"could not decode file {file_path} with common encodings.")
                    return

                new_content = content.replace(find_str, replace_str)
                with open(file_path, 'w', encoding='utf-8') as f: # Write back in utf-8
                    f.write(new_content)
                print(f"performed find/replace in: {file_path}")
            except Exception as e:
                print(f"error performing find/replace in {file_path}: {e}")
        elif ext == '.docx':
            print("find/replace for .docx files is complex and not directly supported in this console app without deeper library integration.")
            print("consider extracting text, modifying it, and then manually re-inserting or using a dedicated word processing library.")
        else:
            print(f"unsupported file type for find/replace: {ext}")

class OrganizationAutomation:
    def _normalize_path(self, path):
        return path.strip().strip('"')

    def organize_by_rules(self, folder_path_input, rules):
        folder_path = self._normalize_path(folder_path_input)
        if not os.path.isdir(folder_path):
            print(f"folder not found: {folder_path}")
            return

        # Get list of items to avoid issues if files are moved during iteration
        items_in_folder = list(os.listdir(folder_path))

        for item in items_in_folder:
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                moved = False
                for rule_ext, dest_folder_name in rules.items():
                    # Ensure rule_ext starts with a dot if it's a file extension
                    if not rule_ext.startswith('.'):
                        rule_ext = '.' + rule_ext
                    if item.lower().endswith(rule_ext.lower()):
                        dest_path = os.path.join(folder_path, self._normalize_path(dest_folder_name))
                        try:
                            if not os.path.exists(dest_path):
                                os.makedirs(dest_path)
                            shutil.move(item_path, dest_path)
                            print(f"moved '{item}' to '{dest_path}' based on rule '{rule_ext}'.")
                            moved = True
                            break
                        except shutil.Error as e:
                            print(f"error moving '{item}' to '{dest_path}': {e}")
                        except Exception as e:
                            print(f"an unexpected error occurred while organizing '{item}': {e}")
                if not moved:
                    print(f"no rule matched for '{item}'.")
            elif os.path.isdir(item_path):
                print(f"skipping directory '{item}' for organization by rules (only files are moved).")


    def create_zip_archives(self, files_input, base_name="archive"):
        if not files_input:
            print("no files provided for zipping.")
            return

        # files_input could be a list of paths or a comma-separated string
        if isinstance(files_input, str):
            files_list = [f.strip() for f in files_input.split(',')]
        else: # assume it's already a list
            files_list = files_input

        files_to_zip = [self._normalize_path(f) for f in files_list if os.path.isfile(self._normalize_path(f))]

        if not files_to_zip:
            print("no valid files found in the provided list to zip.")
            return

        for i, file_path in enumerate(files_to_zip):
            # Use current timestamp for uniqueness to avoid overwriting existing zips
            # Add file's original name to zip_filename for better distinction
            original_filename_no_ext = os.path.splitext(os.path.basename(file_path))[0]
            zip_filename = f"{base_name}_{original_filename_no_ext}_{datetime.now().strftime('%Y%m%d%H%M%S')}.zip"
            try:
                with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    # arcname parameter ensures only the file name is stored in zip, not full path
                    zipf.write(file_path, arcname=os.path.basename(file_path))
                print(f"created zip archive: {zip_filename} containing '{os.path.basename(file_path)}'")
            except Exception as e:
                print(f"error creating zip for '{file_path}': {e}")

class MediaHandling:
    def _normalize_path(self, path):
        return path.strip().strip('"')

    def create_playlist(self, media_files_input, playlist_name="playlist.m3u"):
        if not media_files_input:
            print("no media files provided for playlist creation.")
            return

        # media_files_input could be a list of paths or a comma-separated string
        if isinstance(media_files_input, str):
            media_files_list = [f.strip() for f in media_files_input.split(',')]
        else: # assume it's already a list
            media_files_list = media_files_input

        media_files = [self._normalize_path(f) for f in media_files_list if os.path.isfile(self._normalize_path(f))]
        if not media_files:
            print("no valid media files found in the provided list.")
            return

        supported_extensions = ('.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg',
                                '.mp4', '.avi', '.mkv', '.mov', '.wmv')

        filtered_media = [f for f in media_files if f.lower().endswith(supported_extensions)]

        if not filtered_media:
            print("no supported media files found in the selection to create a playlist.")
            return

        playlist_name = self._normalize_path(playlist_name)
        try:
            with open(playlist_name, 'w', encoding='utf-8') as f:
                for file in filtered_media:
                    f.write(file + '\n')
            print(f"playlist '{playlist_name}' created with {len(filtered_media)} files.")
        except Exception as e:
            print(f"error creating playlist '{playlist_name}': {e}")

    def extract_audio_segment(self, file_paths_input, start_ms, end_ms, output_prefix="output_audio"):
        # file_paths_input can be a single path string or a list of paths
        if isinstance(file_paths_input, str):
            files_to_process = [self._normalize_path(file_paths_input)]
        elif isinstance(file_paths_input, list):
            files_to_process = [self._normalize_path(f) for f in file_paths_input]
        else:
            print("invalid file path input. please provide a string or a list of paths.")
            return

        if not files_to_process:
            print("no files provided for audio extraction.")
            return

        for i, file_path in enumerate(files_to_process):
            if not os.path.exists(file_path):
                print(f"file not found: {file_path}")
                continue

            _, ext = os.path.splitext(file_path)
            ext = ext.lower()

            # Construct unique output filename for mass extraction
            original_name = os.path.splitext(os.path.basename(file_path))[0]
            output_filename = f"{output_prefix}_{original_name}_{i+1}.mp3"


            if ext in ['.mp3', '.wav', '.flac', '.ogg', '.m4a']: # Common audio formats
                try:
                    audio = AudioSegment.from_file(file_path, format=ext[1:]) # [1:] to remove the dot
                    segment = audio[start_ms:end_ms]
                    segment.export(output_filename, format="mp3") # Export as mp3 by default
                    print(f"extracted audio segment from '{file_path}' to '{output_filename}'.")
                except Exception as e:
                    print(f"error extracting audio segment from '{file_path}': {e}")
            else:
                print(f"unsupported file type for audio extraction: {ext} for file {file_path}")


    def trim_video(self, file_paths_input, start_sec, end_sec, output_prefix="output_video"):
        # file_paths_input can be a single path string or a list of paths
        if isinstance(file_paths_input, str):
            files_to_process = [self._normalize_path(file_paths_input)]
        elif isinstance(file_paths_input, list):
            files_to_process = [self._normalize_path(f) for f in file_paths_input]
        else:
            print("invalid file path input. please provide a string or a list of paths.")
            return

        if not files_to_process:
            print("no files provided for video trimming.")
            return

        for i, file_path in enumerate(files_to_process):
            if not os.path.exists(file_path):
                print(f"file not found: {file_path}")
                continue

            _, ext = os.path.splitext(file_path)
            ext = ext.lower()

            # Construct unique output filename for mass trimming
            original_name = os.path.splitext(os.path.basename(file_path))[0]
            output_filename = f"{output_prefix}_{original_name}_{i+1}.mp4"

            if ext in ['.mp4', '.avi', '.mkv', '.mov', '.wmv']: # Common video formats
                try:
                    clip = VideoFileClip(file_path)
                    trimmed_clip = clip.subclip(start_sec, end_sec)
                    trimmed_clip.write_videofile(output_filename, codec="libx264") # Using H.264 codec
                    clip.close()
                    print(f"trimmed video from '{file_path}' to '{output_filename}'.")
                except Exception as e:
                    print(f"error trimming video '{file_path}': {e}")
            else:
                print(f"unsupported file type for video trimming: {ext} for file {file_path}")


class DirectoryMapper:
    def _normalize_path(self, path):
        return path.strip().strip('"')

    def map_directory(self, start_path_input):
        start_path = self._normalize_path(start_path_input)
        if not os.path.isdir(start_path):
            print(f"directory not found: {start_path}")
            return

        while True:
            print("\n--- directory mapping output format ---")
            print("1. tree view")
            print("2. detailed list")
            print("3. table view") # New table view option
            print("4. simple list view") # New explicit option
            print("5. back to information & misc menu")
            output_choice = input("enter your choice: ")

            if output_choice == '1':
                self._print_tree_view(start_path)
                input("press enter to continue...")
            elif output_choice == '2':
                self._print_detailed_list(start_path)
                input("press enter to continue...")
            elif output_choice == '3':
                self._print_table_view(start_path)
                input("press enter to continue...")
            elif output_choice == '4': # Handle simple list view
                self._print_simple_list_view(start_path)
                input("press enter to continue...")
            elif output_choice == '5':
                break
            else:
                print("invalid choice. please try again.")
                input("press enter to continue...")

    def _print_tree_view(self, start_dir, indent="", is_last_dir=True):
        # File type icons
        file_icons = {
            '.txt': '📄', '.doc': '📄', '.docx': '📄', '.pdf': '📄',
            '.py': '🐍', '.js': '🟨', '.html': '🌐', '.css': '🎨',
            '.mp3': '🎵', '.wav': '🎵', '.mp4': '🎬', '.avi': '🎬',
            '.jpg': '🖼️', '.jpeg': '🖼️', '.png': '🖼️', '.gif': '🖼️',
            '.zip': '📦', '.rar': '📦', '.exe': '⚙️', '.log': '📜'
        }
        
        def get_file_icon(filename):
            ext = os.path.splitext(filename)[1].lower()
            return file_icons.get(ext, '📄')
        
        def get_file_size_str(file_path):
            try:
                size = os.path.getsize(file_path)
                if size < 1024:
                    return f"{size}B"
                elif size < 1024 * 1024:
                    return f"{size/1024:.1f}KB"
                elif size < 1024 * 1024 * 1024:
                    return f"{size/(1024*1024):.1f}MB"
                else:
                    return f"{size/(1024*1024*1024):.1f}GB"
            except OSError:
                return ""
        
        marker = "└── " if is_last_dir else "├── "
        dir_name = os.path.basename(start_dir)
        print(f"{indent}{marker}📁 {dir_name}/")

        # Prepare for sub-items
        sub_indent = indent + ("    " if is_last_dir else "│   ")

        try:
            items = sorted(os.listdir(start_dir), key=lambda s: (not os.path.isdir(os.path.join(start_dir, s)), s.lower()))
        except PermissionError:
            print(f"{sub_indent}├── 🚫 [Permission Denied]")
            return
        except OSError as e:
            print(f"{sub_indent}├── ❌ [Error: {e}]")
            return

        for i, item in enumerate(items):
            path = os.path.join(start_dir, item)
            is_last_item = (i == len(items) - 1)

            if os.path.isdir(path):
                self._print_tree_view(path, sub_indent, is_last_item)
            else:
                file_marker = "└── " if is_last_item else "├── "
                icon = get_file_icon(item)
                size_str = get_file_size_str(path)
                size_display = f" ({size_str})" if size_str else ""
                print(f"{sub_indent}{file_marker}{icon} {item}{size_display}")


    def _print_detailed_list(self, start_dir):
        print("\n" + "═" * 80)
        print(f"📋 DETAILED LIST VIEW - {start_dir}")
        print("═" * 80)
        
        # File type icons
        file_icons = {
            '.txt': '📄', '.doc': '📄', '.docx': '📄', '.pdf': '📄',
            '.py': '🐍', '.js': '🟨', '.html': '🌐', '.css': '🎨',
            '.mp3': '🎵', '.wav': '🎵', '.mp4': '🎬', '.avi': '🎬',
            '.jpg': '🖼️', '.jpeg': '🖼️', '.png': '🖼️', '.gif': '🖼️',
            '.zip': '📦', '.rar': '📦', '.exe': '⚙️', '.log': '📜'
        }
        
        def get_file_icon(filename):
            ext = os.path.splitext(filename)[1].lower()
            return file_icons.get(ext, '📄')
        
        def get_file_size_str(file_path):
            try:
                size = os.path.getsize(file_path)
                if size < 1024:
                    return f"{size}B"
                elif size < 1024 * 1024:
                    return f"{size/1024:.1f}KB"
                elif size < 1024 * 1024 * 1024:
                    return f"{size/(1024*1024):.1f}MB"
                else:
                    return f"{size/(1024*1024*1024):.1f}GB"
            except OSError:
                return "N/A"
        
        def get_file_date_str(file_path):
            try:
                timestamp = os.path.getmtime(file_path)
                return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
            except OSError:
                return "N/A"
        
        try:
            for root, dirs, files in os.walk(start_dir):
                level = root.replace(start_dir, '').count(os.sep)
                indent = '  ' * level
                rel_path = os.path.relpath(root, start_dir)
                dir_name = os.path.basename(root) if level > 0 else "."
                
                # Count items in directory
                try:
                    item_count = len(os.listdir(root))
                    count_str = f"({item_count} items)"
                except (PermissionError, OSError):
                    count_str = "(access denied)"
                
                print(f"{indent}📁 {dir_name}/ {count_str}")
                
                # Show files in current directory
                subindent = '  ' * (level + 1)
                for f in sorted(files, key=str.lower):
                    file_path = os.path.join(root, f)
                    icon = get_file_icon(f)
                    size_str = get_file_size_str(file_path)
                    date_str = get_file_date_str(file_path)
                    
                    print(f"{subindent}{icon} {f:<30} {size_str:>8} {date_str}")
                    
        except PermissionError as e:
            print(f"🚫 Permission denied accessing some directories: {e}")
        except OSError as e:
            print(f"❌ Error accessing directory structure: {e}")
        
        print("─" * 80)

    def _print_table_view(self, start_dir):
        print("\n" + "═" * 80)
        print(f"📊 TABLE VIEW - {start_dir}")
        print("═" * 80)

        # File type icons
        file_icons = {
            '.txt': '📄', '.doc': '📄', '.docx': '📄', '.pdf': '📄',
            '.py': '🐍', '.js': '🟨', '.html': '🌐', '.css': '🎨',
            '.mp3': '🎵', '.wav': '🎵', '.mp4': '🎬', '.avi': '🎬',
            '.jpg': '🖼️', '.jpeg': '🖼️', '.png': '🖼️', '.gif': '🖼️',
            '.zip': '📦', '.rar': '📦', '.exe': '⚙️', '.log': '📜'
        }
        
        data = []
        try:
            for root, dirs, files in os.walk(start_dir):
                relative_path = os.path.relpath(root, start_dir)
                if relative_path == ".":
                    relative_path = "" # For the root directory itself

                # Add directories
                for d in sorted(dirs, key=str.lower):
                    full_path = os.path.join(root, d)
                    try:
                        item_count = len(os.listdir(full_path))
                        count_str = f"({item_count} items)"
                    except (PermissionError, OSError):
                        count_str = "(access denied)"

                    data.append({
                        "type": "directory",
                        "name": d + "/",
                        "path": os.path.join(relative_path, d),
                        "size": count_str, # Size for directory not easily available without recursive calculation
                        "last_modified": "",
                        "icon": "📁"
                    })

                # Add files
                for f in sorted(files, key=str.lower):
                    full_path = os.path.join(root, f)
                    icon = '📄'
                    size_str = ""
                    last_mod = ""
                    try:
                        file_size = os.path.getsize(full_path)
                        size_str = f"{file_size / (1024*1024):.2f} MB"
                        last_mod_timestamp = os.path.getmtime(full_path)
                        last_mod = datetime.fromtimestamp(last_mod_timestamp).strftime('%Y-%m-%d %H:%M')
                        ext = os.path.splitext(f)[1].lower()
                        icon = file_icons.get(ext, '📄')
                    except OSError:
                        size_str = "N/A"
                        last_mod = "N/A"

                    data.append({
                        "type": "file",
                        "name": f,
                        "path": os.path.join(relative_path, f),
                        "size": size_str,
                        "last_modified": last_mod,
                        "icon": icon
                    })
        except PermissionError as e:
            print(f"Permission denied accessing some directories: {e}")
            return
        except OSError as e:
            print(f"Error accessing directory structure: {e}")
            return

        if not data:
            print("no items found to display.")
            return

        # Determine column widths
        col_name_width = max(len(d["name"]) for d in data) if data else 15
        col_type_width = max(len(d["type"]) for d in data) if data else 10
        col_path_width = max(len(d["path"]) for d in data) if data else 20
        col_size_width = max(len(d["size"]) for d in data) if data else 10
        col_mod_width = max(len(d["last_modified"]) for d in data) if data else 16

        # Add header lengths to width consideration
        col_name_width = max(col_name_width, len("📝 Name"))
        col_type_width = max(col_type_width, len("📁 Type"))
        col_path_width = max(col_path_width, len("📍 Path"))
        col_size_width = max(col_size_width, len("📊 Size"))
        col_mod_width = max(col_mod_width, len("📅 Modified"))

        # Create header format string
        header = f"{{:<{col_name_width}}} {{:<{col_type_width}}} {{:<{col_path_width}}} {{:<{col_size_width}}} {{:<{col_mod_width}}}"

        # Print table header
        print(header.format("📝 Name", "📁 Type", "📍 Path", "📊 Size", "📅 Modified"))
        print("─" * (col_name_width + col_type_width + col_path_width + col_size_width + col_mod_width + 4))

        # Print table rows
        for item in data:
            name_with_icon = f"{item['icon']} {item['name']}"
            print(header.format(name_with_icon, item["type"], item["path"], item["size"], item["last_modified"]))
            
        print("─" * 80)

    def _print_simple_list_view(self, start_dir):
        print(f"\n--- simple list view of {start_dir} ---")
        items = []
        # Add '..' to go up (optional for this view, but consistent with browser behavior)
        if os.path.dirname(start_dir) != start_dir:
            items.append(("..", "dir"))

        # List directories first, then files, sorted alphabetically
        with os.scandir(start_dir) as entries:
            for entry in sorted(entries, key=lambda e: (not e.is_dir(), e.name.lower())):
                if entry.is_dir():
                    items.append((entry.name, "dir"))
                elif entry.is_file():
                    items.append((entry.name, "file"))

        for i, (name, item_type) in enumerate(items):
            prefix = "[D]" if item_type == "dir" else "[F]"
            print(f"{i}. {prefix} {name}")


class SelectPlusApp:
    def __init__(self):
        self.file_manager = FileManagement()
        self.content_manager = ContentManagement()
        self.org_automation = OrganizationAutomation()
        self.media_handler = MediaHandling()
        self.directory_mapper = DirectoryMapper()
        self.custom_descriptions = {}
        self.interactive = InteractiveHandler()
        self.enhanced_file_manager = EnhancedFileManager()
        # Bytes to Gigabytes conversion factor
        self.gb_conversion_factor = 1024 ** 3
        # Clipboard for cut/copy operations
        self.clipboard = []
        self.clipboard_operation = None  # 'cut' or 'copy'
        # Multi-selection functionality
        self.selected_items = []
        self.multi_select_mode = False
        # User-configurable share programs
        self.share_programs = {
            "Email": "outlook",
            "WhatsApp": "whatsapp",
            "Telegram": "telegram",
            "Discord": "discord"
        }
        # User-configurable send-to locations
        self.send_to_locations = {
            "Desktop": os.path.expanduser("~/Desktop"),
            "Documents": os.path.expanduser("~/Documents"),
            "Downloads": os.path.expanduser("~/Downloads"),
            "Pictures": os.path.expanduser("~/Pictures"),
            "Videos": os.path.expanduser("~/Videos")
        }
        # Settings
        self.settings = {
            "browse_start_mode": "default",  # "default", "project", "custom"
            "custom_start_path": os.getcwd(),
            "project_start_path": os.getcwd(),
            "global_search_scope": "system",  # "system", "current_dir", "custom"
            "global_search_default_dir": os.path.expanduser("~"),
            "global_search_enabled": True
        }
        
        # Navigation history for enhanced back functionality
        self.navigation_history = []
        self.current_history_index = -1
        
        # Language manager
        self.lang = lang
        
        # Load settings from file
        self.load_settings()
        
    def load_settings(self):
        """Load settings from JSON file."""
        try:
            if os.path.exists("selectplus_settings.json"):
                with open("selectplus_settings.json", 'r', encoding='utf-8') as f:
                    file_settings = json.load(f)
                    # Update settings with values from file
                    for key, value in file_settings.items():
                        if key in self.settings:
                            self.settings[key] = value
                        # Handle special cases
                        if key == "global_search_default_dir" and value == "~":
                            self.settings[key] = os.path.expanduser("~")
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def save_settings(self):
        """Save settings to JSON file."""
        try:
            settings_to_save = self.settings.copy()
            # Convert paths to relative form if they're home directory
            if settings_to_save.get("global_search_default_dir") == os.path.expanduser("~"):
                settings_to_save["global_search_default_dir"] = "~"
            
            with open("selectplus_settings.json", 'w', encoding='utf-8') as f:
                json.dump(settings_to_save, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
        
    def handle_global_operation(self, operation, context_path=None, selected_item=None):
        """Handle global operations (add new, delete, others menu) for any context."""
        if operation == 'GLOBAL_ADD_NEW':
            if not context_path:
                context_path = os.getcwd()
            filename = self.interactive.show_text_input(
                "Enter new file name (with extension)", "newfile.txt", allow_extension_change=True
            )
            if filename:
                self.enhanced_file_manager.create_file(context_path, filename)
                print(f"✅ Created file '{filename}' in '{context_path}'")
                time.sleep(1)
                
        elif operation == 'GLOBAL_DELETE':
            if selected_item and os.path.exists(selected_item):
                item_type = "folder" if os.path.isdir(selected_item) else "file"
                if self.interactive.show_confirmation(
                    f"Delete {item_type} '{os.path.basename(selected_item)}'?", default=False
                ):
                    self.enhanced_file_manager.delete_item(selected_item)
                    print(f"✅ Deleted {item_type} '{os.path.basename(selected_item)}'")
                    time.sleep(1)
            else:
                print("❌ No item selected for deletion")
                time.sleep(1)
                
        elif operation == 'GLOBAL_OTHERS':
            if selected_item and os.path.exists(selected_item):
                self.show_context_menu(selected_item)
            else:
                print("❌ No item selected for operations")
                time.sleep(1)
                
        return True  # Indicate that operation was handled
    
    def toggle_multi_select_mode(self):
        """Toggle multi-selection mode on/off."""
        self.multi_select_mode = not self.multi_select_mode
        if not self.multi_select_mode:
            self.selected_items = []
        status = "ON" if self.multi_select_mode else "OFF"
        print(f"🔄 Multi-select mode: {status}")
        if self.multi_select_mode:
            print("💡 Use SPACE to select/deselect items, ENTER to confirm selection")
        time.sleep(1)
    
    def add_to_selection(self, item_path):
        """Add item to multi-selection."""
        abs_path = os.path.abspath(item_path)
        if abs_path not in self.selected_items:
            self.selected_items.append(abs_path)
            print(f"✅ Added to selection: {os.path.basename(abs_path)}")
        else:
            print(f"⚠️ Already selected: {os.path.basename(abs_path)}")
    
    def remove_from_selection(self, item_path):
        """Remove item from multi-selection."""
        abs_path = os.path.abspath(item_path)
        if abs_path in self.selected_items:
            self.selected_items.remove(abs_path)
            print(f"❌ Removed from selection: {os.path.basename(abs_path)}")
        else:
            print(f"⚠️ Not in selection: {os.path.basename(abs_path)}")
    
    def toggle_item_selection(self, item_path):
        """Toggle item in/out of selection."""
        abs_path = os.path.abspath(item_path)
        if abs_path in self.selected_items:
            self.remove_from_selection(item_path)
        else:
            self.add_to_selection(item_path)
    
    def clear_selection(self):
        """Clear all selected items."""
        count = len(self.selected_items)
        self.selected_items = []
        print(f"🗑️ Cleared {count} selected items")
    
    def add_to_navigation_history(self, path):
        """Add a path to navigation history."""
        # Remove any entries after current position (for when we go back and then navigate somewhere new)
        self.navigation_history = self.navigation_history[:self.current_history_index + 1]
        
        # Add new path if it's different from the current one
        if not self.navigation_history or self.navigation_history[-1] != path:
            self.navigation_history.append(path)
            self.current_history_index = len(self.navigation_history) - 1
            
            # Limit history to 50 items
            if len(self.navigation_history) > 50:
                self.navigation_history = self.navigation_history[-50:]
                self.current_history_index = len(self.navigation_history) - 1
    
    def go_back_in_history(self):
        """Go back one step in navigation history."""
        if self.current_history_index > 0:
            self.current_history_index -= 1
            return self.navigation_history[self.current_history_index]
        return None
    
    def go_forward_in_history(self):
        """Go forward one step in navigation history."""
        if self.current_history_index < len(self.navigation_history) - 1:
            self.current_history_index += 1
            return self.navigation_history[self.current_history_index]
        return None
    
    def global_search(self, search_term):
        """Perform global search based on current settings."""
        if not self.settings.get("global_search_enabled", True):
            print("❌ Global search is disabled")
            return []
        
        search_scope = self.settings.get("global_search_scope", "system")
        
        if search_scope == "system":
            # Search entire system - start from root/drives
            if os.name == 'nt':
                # Windows - search all drives
                search_roots = []
                import string
                for drive in string.ascii_uppercase:
                    drive_path = f"{drive}:\\"
                    if os.path.exists(drive_path):
                        search_roots.append(drive_path)
            else:
                # Unix systems - search from root
                search_roots = ["/"]
        elif search_scope == "current_dir":
            # Search current directory and subdirectories
            search_roots = [os.getcwd()]
        elif search_scope == "custom":
            # Search custom directory
            search_roots = [self.settings.get("global_search_default_dir", os.path.expanduser("~"))]
        else:
            # Default to home directory
            search_roots = [os.path.expanduser("~")]
        
        results = []
        max_results = 100  # Limit results to avoid overwhelming output
        
        print(f"🔍 Searching for '{search_term}' in scope: {search_scope}...")
        
        try:
            for root in search_roots:
                if len(results) >= max_results:
                    break
                    
                try:
                    # Limit search depth to avoid infinite loops
                    max_depth = 5 if search_scope == "system" else 10
                    for dirpath, dirnames, filenames in os.walk(root):
                        if len(results) >= max_results:
                            break
                        
                        # Calculate current depth
                        current_depth = dirpath.replace(root, '').count(os.sep)
                        if current_depth > max_depth:
                            continue
                        
                        try:
                            # Search in directory names
                            for dirname in dirnames[:50]:  # Limit to 50 items per directory
                                if search_term.lower() in dirname.lower():
                                    full_path = os.path.join(dirpath, dirname)
                                    results.append((full_path, "directory"))
                                    if len(results) >= max_results:
                                        break
                            
                            # Search in file names
                            for filename in filenames[:50]:  # Limit to 50 items per directory
                                if search_term.lower() in filename.lower():
                                    full_path = os.path.join(dirpath, filename)
                                    results.append((full_path, "file"))
                                    if len(results) >= max_results:
                                        break
                        except (PermissionError, OSError):
                            # Skip directories we can't access
                            continue
                            
                except (PermissionError, OSError):
                    # Skip root directories we can't access
                    continue
                        
        except KeyboardInterrupt:
            print(f"\n⚠️ Search interrupted by user")
            print(f"✅ Found {len(results)} results so far")
        except Exception as e:
            print(f"❌ Error during search: {e}")
        
        if len(results) >= max_results:
            print(f"⚠️ Search limited to first {max_results} results")
            
        return results
    
    def show_search_results(self, results, search_term):
        """Display search results in an interactive menu."""
        if not results:
            print(f"❌ No results found for '{search_term}'")
            time.sleep(2)
            return
        
        print(f"\n✅ Found {len(results)} results for '{search_term}'")
        
        # Create menu options from results
        options = []
        for path, item_type in results:
            icon = "📁" if item_type == "directory" else "📄"
            options.append(f"{icon} {os.path.basename(path)} ({os.path.dirname(path)})")
        
        options.append("🔙 Back")
        
        choice = self.interactive.show_interactive_menu(
            f"SEARCH RESULTS: '{search_term}'",
            options
        )
        if choice is not None and choice < len(results):
            selected_path, item_type = results[choice]
            
            if item_type == "directory":
                # Navigate to the directory
                self.add_to_navigation_history(selected_path)
                self._browse_path(selected_path)
            else:
                # Show context menu for the file
                self.show_context_menu(selected_path)
    
    def show_global_search_menu(self):
        """Show enhanced global search interface with searchbar."""
        while True:
            # Show search interface with current settings
            search_options = [
                "🔍 Quick Search",
                "🔎 Advanced Search",
                "📊 Search History",
                "⚙️ Search Settings",
                "🔙 Back to Main Menu"
            ]
            
            choice = self.interactive.show_interactive_menu(
                "GLOBAL SEARCH MENU",
                search_options,
                context_path=os.getcwd()
            )
            
            if choice is None or choice == 4:  # Back
                break
            elif choice == 0:  # Quick Search
                self.show_quick_search()
            elif choice == 1:  # Advanced Search
                self.show_advanced_search()
            elif choice == 2:  # Search History
                self.show_search_history()
            elif choice == 3:  # Search Settings
                self.show_global_search_settings()
    
    def show_quick_search(self):
        """Show quick search interface with searchbar."""
        while True:
            # Show current search scope
            scope_text = {
                "system": "System-wide",
                "current_dir": "Current Directory",
                "custom": "Custom Directory"
            }
            current_scope = self.settings.get("global_search_scope", "system")
            
            print("\n" + "═" * 80)
            print("🔍 QUICK SEARCH")
            print("═" * 80)
            print(f"📂 Search Scope: {scope_text.get(current_scope, 'Unknown')}")
            if current_scope == "custom":
                print(f"📁 Search Directory: {self.settings.get('global_search_default_dir', 'Unknown')}")
            print("─" * 80)
            
            search_term = self.interactive.show_text_input(
                "Enter search term (filename/directory name):"
            )
            
            if not search_term:
                break
                
            results = self.global_search(search_term)
            self.show_search_results(results, search_term)
            
            # Ask if user wants to search again
            if not self.interactive.show_confirmation("Search again?", default=False):
                break
    
    def show_advanced_search(self):
        """Show advanced search interface with more options."""
        while True:
            print("\n" + "═" * 80)
            print("🔎 ADVANCED SEARCH")
            print("═" * 80)
            
            # Get search parameters
            search_term = self.interactive.show_text_input(
                "Enter search term (filename/directory name):"
            )
            
            if not search_term:
                break
                
            # File type filter
            file_type = self.interactive.show_text_input(
                "File type filter (e.g., .txt, .pdf, or leave empty for all):"
            )
            
            # Size filter
            size_filter = self.interactive.show_text_input(
                "Size filter - min size in MB (or leave empty):"
            )
            
            # Perform search with filters
            results = self.advanced_search(search_term, file_type, size_filter)
            self.show_search_results(results, search_term)
            
            # Ask if user wants to search again
            if not self.interactive.show_confirmation("Search again?", default=False):
                break
    
    def show_search_history(self):
        """Show search history (placeholder for future implementation)."""
        print("\n" + "═" * 80)
        print("📊 SEARCH HISTORY")
        print("═" * 80)
        print("📝 Search history feature coming soon...")
        print("─" * 80)
        time.sleep(2)
    
    def advanced_search(self, search_term, file_type=None, size_filter=None):
        """Perform advanced search with additional filters."""
        if not self.settings.get("global_search_enabled", True):
            print("❌ Global search is disabled")
            return []
        
        # Get basic search results
        results = self.global_search(search_term)
        
        # Apply file type filter
        if file_type and file_type.strip():
            file_type = file_type.strip().lower()
            if not file_type.startswith('.'):
                file_type = '.' + file_type
            results = [(path, item_type) for path, item_type in results 
                      if item_type == "directory" or path.lower().endswith(file_type)]
        
        # Apply size filter
        if size_filter and size_filter.strip():
            try:
                min_size_mb = float(size_filter.strip())
                min_size_bytes = min_size_mb * 1024 * 1024
                filtered_results = []
                
                for path, item_type in results:
                    if item_type == "directory":
                        filtered_results.append((path, item_type))
                    else:
                        try:
                            if os.path.getsize(path) >= min_size_bytes:
                                filtered_results.append((path, item_type))
                        except OSError:
                            continue
                
                results = filtered_results
            except ValueError:
                print("⚠️ Invalid size filter, ignoring...")
                time.sleep(1)
        
        return results
    
    def show_selection_info(self):
        """Display current selection info."""
        if not self.selected_items:
            print("📁 No items selected")
        else:
            print(f"📁 Selected {len(self.selected_items)} items:")
            for i, item in enumerate(self.selected_items, 1):
                print(f"  {i}. {os.path.basename(item)}")
        
    def get_browse_start_path(self):
        """Get the starting path for file browsing based on settings."""
        if self.settings["browse_start_mode"] == "default":
            # Show all drives on Windows - use a special marker for drives view
            if os.name == 'nt':
                return "__DRIVES__"  # Special marker for drives view
            else:
                return "/"  # Start from root on Unix systems
        elif self.settings["browse_start_mode"] == "project":
            return self.settings["project_start_path"]
        elif self.settings["browse_start_mode"] == "custom":
            return self.settings["custom_start_path"]
        else:
            return os.getcwd()

    def _clear_screen(self):
        # for windows
        if os.name == 'nt':
            os.system('cls')
        # for mac and linux
        else:
            os.system('clear')

    def _browse_path(self, start_dir=None, select_type="any"):
        """
        Enhanced interactive file browser with keyboard navigation.
        select_type: "file", "dir", or "any"
        returns the absolute path of selected item or None if cancelled.
        """
        if start_dir is None:
            current_path = self.get_browse_start_path()
        else:
            current_path = start_dir if os.path.isdir(start_dir) else self.get_browse_start_path()
        
        # Add initial path to navigation history
        if current_path != "__DRIVES__":
            self.add_to_navigation_history(current_path)
            
        selected_index = 0
        viewport_start = 0
        history = []
        sort_by = "name"
        reverse_sort = False
        show_hidden = False

        while True:
            # Build items list
            items = []
            
            # Special handling for drives view
            if current_path == "__DRIVES__":
                # Show all available drives
                if os.name == 'nt':
                    import string
                    for drive in string.ascii_uppercase:
                        drive_path = f"{drive}:\\"
                        if os.path.exists(drive_path):
                            try:
                                # Get drive type info
                                import subprocess
                                result = subprocess.run(['wmic', 'logicaldisk', 'where', f'DeviceID="{drive}:"', 'get', 'Size,FreeSpace,VolumeLabel'], 
                                                      capture_output=True, text=True, timeout=2)
                                details = f"Drive {drive}:"
                            except:
                                details = f"Drive {drive}:"
                            items.append((drive_path, "dir", details))
                else:
                    # Unix systems - show root
                    items.append(("/", "dir", "Root Directory"))
            else:
                # Add '..' to go up (but not from drives view)
                if os.path.dirname(current_path) != current_path:
                    items.append(("..", "dir", "Parent Directory"))
                
                # Get directory entries
                try:
                    with os.scandir(current_path) as entries:
                        for entry in entries:
                            if not show_hidden and entry.name.startswith('.'):
                                continue
                            
                            try:
                                if entry.is_dir():
                                    # Count items in directory
                                    try:
                                        item_count = len(os.listdir(entry.path))
                                        details = f"{item_count} items"
                                    except (PermissionError, OSError):
                                        details = "Access denied"
                                    items.append((entry.name, "dir", details))
                                elif entry.is_file():
                                    # Get file size
                                    try:
                                        size = entry.stat().st_size
                                        if size < 1024:
                                            details = f"{size}B"
                                        elif size < 1024 * 1024:
                                            details = f"{size/1024:.1f}KB"
                                        elif size < 1024 * 1024 * 1024:
                                            details = f"{size/(1024*1024):.1f}MB"
                                        else:
                                            details = f"{size/(1024*1024*1024):.1f}GB"
                                    except OSError:
                                        details = "Unknown size"
                                    items.append((entry.name, "file", details))
                            except OSError:
                                continue
                except (PermissionError, OSError):
                    items.append(("[Access Denied]", "error", "Cannot read directory"))
            
            # Sort items
            if sort_by == "name":
                items.sort(key=lambda x: (x[1] != "dir", x[0].lower()), reverse=reverse_sort)
            elif sort_by == "size":
                items.sort(key=lambda x: (x[1] != "file", x[2]), reverse=reverse_sort)
            elif sort_by == "type":
                items.sort(key=lambda x: (x[1], x[0].lower()), reverse=reverse_sort)
            
            # Ensure selected index is valid
            if selected_index >= len(items):
                selected_index = len(items) - 1 if items else 0
            if selected_index < 0:
                selected_index = 0
            
            # Create info strings
            history_info = f"History: {len(history)} locations"
            sort_info = f"Sort: {sort_by}{'(reverse)' if reverse_sort else ''} | Hidden: {'shown' if show_hidden else 'hidden'}"
            
            # Show file browser
            action, new_index, new_viewport = self.interactive.show_file_browser(
                current_path, items, selected_index, sort_info, history_info, viewport_start, self.selected_items
            )
            
            viewport_start = new_viewport
            
            if action == 'navigate':
                selected_index = new_index
            elif action == 'select':
                if not items:
                    continue
                    
                item_name, item_type, _ = items[selected_index]
                
                if item_name == "..":
                    history.append(current_path)
                    if current_path == "__DRIVES__":
                        return None  # Can't go up from drives view
                    else:
                        parent = os.path.dirname(current_path)
                        # If we're going up to root level, go to drives view
                        if parent == current_path or (os.name == 'nt' and len(parent) <= 3):
                            current_path = "__DRIVES__"
                        else:
                            current_path = parent
                    selected_index = 0
                    viewport_start = 0
                elif item_type == "dir":
                    # For general browsing (select_type == "any"), directly enter directories
                    # For specific directory selection (select_type == "dir"), ask for confirmation
                    if select_type == "dir":
                        # Check if user wants to select this directory or enter it
                        if current_path == "__DRIVES__":
                            dir_path = item_name  # Drive paths are complete
                        else:
                            dir_path = os.path.join(current_path, item_name)
                        
                        if self.interactive.show_confirmation(
                            f"Select directory '{item_name}'?", default=False
                        ):
                            return os.path.abspath(dir_path)
                    
                    # Enter directory (for general browsing or if user chose not to select)
                    history.append(current_path)
                    if current_path == "__DRIVES__":
                        current_path = item_name  # Drive paths are complete
                    else:
                        current_path = os.path.join(current_path, item_name)
                    
                    # Add to navigation history
                    self.add_to_navigation_history(current_path)
                    selected_index = 0
                    viewport_start = 0
                elif item_type == "file":
                    if select_type == "file" or select_type == "any":
                        file_path = os.path.join(current_path, item_name)
                        return os.path.abspath(file_path)
                    else:
                        self.interactive.show_confirmation(
                            "Cannot select file, expecting a directory.", default=True
                        )
            elif action == 'back':
                # Try to use navigation history first for better back functionality
                back_path = self.go_back_in_history()
                if back_path and os.path.exists(back_path):
                    current_path = back_path
                    selected_index = 0
                    viewport_start = 0
                elif history:
                    current_path = history.pop()
                    selected_index = 0
                    viewport_start = 0
                else:
                    return None
            elif action == 'command':
                command = new_index
                if command == 's':
                    # Select current directory
                    if select_type == "dir" or select_type == "any":
                        return os.path.abspath(current_path)
                    else:
                        self.interactive.show_confirmation(
                            "Cannot select directory, expecting a file.", default=True
                        )
                elif command == 'h':
                    # Go home
                    history.append(current_path)
                    current_path = os.path.expanduser("~")
                    self.add_to_navigation_history(current_path)
                    selected_index = 0
                    viewport_start = 0
                elif command == 'q':
                    return None
                elif command == 'new_item_menu':
                    if current_path == "__DRIVES__":
                        self.interactive.show_confirmation(
                            "Cannot create items in drives view. Please navigate to a directory first.", default=True
                        )
                    else:
                        # Show menu to choose between file and folder
                        create_options = ["📄 New File", "📁 New Folder"]
                        choice = self.interactive.show_interactive_menu("CREATE NEW", create_options)
                        if choice == 0:  # New File
                            filename = self.interactive.show_text_input(
                                "Enter new file name (with extension)", "newfile.txt", allow_extension_change=True
                            )
                            if filename:
                                self.enhanced_file_manager.create_file(current_path, filename)
                                # Refresh the directory listing
                                continue
                        elif choice == 1:  # New Folder
                            dirname = self.interactive.show_text_input("Enter new directory name")
                            if dirname:
                                self.enhanced_file_manager.create_folder(current_path, dirname)
                                # Refresh the directory listing
                                continue
                elif command == 'new_file':
                    if current_path == "__DRIVES__":
                        self.interactive.show_confirmation(
                            "Cannot create files in drives view. Please navigate to a directory first.", default=True
                        )
                    else:
                        filename = self.interactive.show_text_input(
                            "Enter new file name (with extension)", "newfile.txt", allow_extension_change=True
                        )
                        if filename:
                            self.enhanced_file_manager.create_file(current_path, filename)
                            # Refresh the directory listing
                            continue
                elif command == 'new_dir':
                    if current_path == "__DRIVES__":
                        self.interactive.show_confirmation(
                            "Cannot create directories in drives view. Please navigate to a directory first.", default=True
                        )
                    else:
                        dirname = self.interactive.show_text_input("Enter new directory name")
                        if dirname:
                            self.enhanced_file_manager.create_folder(current_path, dirname)
                            # Refresh the directory listing
                            continue
                elif command == 'delete':
                    if current_path == "__DRIVES__":
                        self.interactive.show_confirmation(
                            "Cannot delete drives. Please navigate to a directory first.", default=True
                        )
                    elif items and selected_index < len(items):
                        item_name, item_type, _ = items[selected_index]
                        if item_name != "..":
                            item_path = os.path.join(current_path, item_name)
                            item_type_name = "folder" if item_type == "dir" else "file"
                            if self.interactive.show_confirmation(
                                f"Delete {item_type_name} '{item_name}'?", default=False
                            ):
                                self.enhanced_file_manager.delete_item(item_path)
                                # Refresh the directory listing
                                continue
                elif command == 'v':
                    # Show view options
                    view_options = [
                        "🌲 Tree View",
                        "📋 Detailed List",
                        "📊 Table View",
                        "📄 Simple List"
                    ]
                    view_choice = self.interactive.show_interactive_menu(
                        "SELECT VIEW", view_options
                    )
                    if view_choice == 0:
                        self.directory_mapper._print_tree_view(current_path)
                        input("\nPress Enter to continue...")
                    elif view_choice == 1:
                        self.directory_mapper._print_detailed_list(current_path)
                        input("\nPress Enter to continue...")
                    elif view_choice == 2:
                        self.directory_mapper._print_table_view(current_path)
                        input("\nPress Enter to continue...")
                    elif view_choice == 3:
                        self.directory_mapper._print_simple_list_view(current_path)
                        input("\nPress Enter to continue...")
                elif command == 'sn':
                    sort_by = "name"
                    reverse_sort = False
                elif command == 'ss':
                    sort_by = "size"
                    reverse_sort = False
                elif command == 'st':
                    sort_by = "type"
                    reverse_sort = False
                elif command == 'sr':
                    reverse_sort = not reverse_sort
                elif command == 'sh':
                    show_hidden = not show_hidden
                elif command == 'context':
                    if items and selected_index < len(items):
                        item_name, item_type, _ = items[selected_index]
                        if item_name != "..":
                            item_path = os.path.join(current_path, item_name)
                            self.show_context_menu(item_path)
                elif command == 'run':
                    if items and selected_index < len(items):
                        item_name, item_type, _ = items[selected_index]
                        if item_type == "file":
                            item_path = os.path.join(current_path, item_name)
                            self.enhanced_file_manager.run_file(item_path)
                elif command == 'properties':
                    if items and selected_index < len(items):
                        item_name, item_type, _ = items[selected_index]
                        if item_name != "..":
                            item_path = os.path.join(current_path, item_name)
                            self.enhanced_file_manager.show_properties(item_path)
                            input("\nPress Enter to continue...")
                elif command == 'multi_mode':
                    self.toggle_multi_select_mode()
                elif command == 'toggle_select':
                    if items and selected_index < len(items):
                        item_name, item_type, _ = items[selected_index]
                        if item_name != "..":
                            if current_path == "__DRIVES__":
                                item_path = item_name  # Drive paths are complete
                            else:
                                item_path = os.path.join(current_path, item_name)
                            self.toggle_item_selection(item_path)
                elif command == 'select_all':
                    # Add all items to selection
                    for item_name, item_type, _ in items:
                        if item_name != "..":
                            if current_path == "__DRIVES__":
                                item_path = item_name  # Drive paths are complete
                            else:
                                item_path = os.path.join(current_path, item_name)
                            self.add_to_selection(item_path)
                elif command == 'deselect_all':
                    # Clear all selections
                    self.clear_selection()
                elif command == 'clear_selection':
                    self.clear_selection()
                elif command == 'selection_info':
                    # Show properties of the currently selected item
                    if items and selected_index < len(items):
                        item_name, item_type, _ = items[selected_index]
                        if item_name != "..":
                            if current_path == "__DRIVES__":
                                item_path = item_name  # Drive paths are complete
                            else:
                                item_path = os.path.join(current_path, item_name)
                            
                            # For drives, show a simple info display
                            if current_path == "__DRIVES__":
                                self.show_drive_info(item_path)
                            else:
                                self.enhanced_file_manager.show_properties(item_path)
                            input("\nPress Enter to continue...")
                    else:
                        print("No item selected to show properties for.")
                        time.sleep(1)
                elif command == 'copy_path':
                    # Copy path of selected item
                    if items and selected_index < len(items):
                        item_name, item_type, _ = items[selected_index]
                        if item_name != "..":
                            if current_path == "__DRIVES__":
                                item_path = item_name  # Drive paths are complete
                            else:
                                item_path = os.path.join(current_path, item_name)
                            self.copy_path_to_clipboard(item_path)
                    else:
                        print("No item selected to copy path for.")
                        time.sleep(1)
                elif command == 'file_select':
                    # Open file selection menu
                    self._select_files_folders_menu()
                elif command == 'global_search':
                    # Open global search interface
                    self.show_global_search_menu()
    
    def show_drive_info(self, drive_path):
        """Show information about a drive."""
        try:
            import shutil
            print("\n" + "═" * 60)
            print(f"🔍 DRIVE INFORMATION: {drive_path}")
            print("═" * 60)
            
            # Get drive statistics
            try:
                total, used, free = shutil.disk_usage(drive_path)
                print(f"📁 Drive: {drive_path}")
                print(f"📊 Total Space: {total / (1024**3):.2f} GB")
                print(f"📊 Used Space: {used / (1024**3):.2f} GB")
                print(f"📊 Free Space: {free / (1024**3):.2f} GB")
                print(f"📊 Usage: {(used/total)*100:.1f}%")
                
                # Try to get volume label using Windows commands
                if os.name == 'nt':
                    try:
                        import subprocess
                        result = subprocess.run(['vol', drive_path[0] + ':'], 
                                              capture_output=True, text=True, timeout=5)
                        if result.returncode == 0:
                            lines = result.stdout.strip().split('\n')
                            for line in lines:
                                if 'Volume in drive' in line:
                                    label = line.split('is')[-1].strip() if 'is' in line else 'No label'
                                    print(f"🏷️ Volume Label: {label}")
                                    break
                    except Exception:
                        pass
                        
            except Exception as e:
                print(f"❌ Error getting drive information: {e}")
                
            print("─" * 60)
        except Exception as e:
            print(f"❌ Error displaying drive info: {e}")

    def show_context_menu(self, selected_path):
        """Show a comprehensive context menu for a file or directory."""
        # Check if we have multi-selected items
        items_to_operate = self.selected_items if self.selected_items else [selected_path]
        is_multi_selection = len(items_to_operate) > 1
        
        while True:
            options = [
                self.lang.get_text("cut"),
                self.lang.get_text("copy"), 
                self.lang.get_text("copy_path"),
                self.lang.get_text("paste"),
                self.lang.get_text("delete"),
            ]
            
            # Add rename only for single selection
            if not is_multi_selection:
                options.append(self.lang.get_text("rename"))
                rename_index = len(options) - 1
            else:
                rename_index = -1
            
            options.extend([
                self.lang.get_text("move"),
                self.lang.get_text("share"),
            ])
            move_index = len(options) - 2
            share_index = len(options) - 1
            
            # Add run/admin only for single files
            if not is_multi_selection and os.path.isfile(selected_path):
                options.extend([
                    self.lang.get_text("run"),
                    self.lang.get_text("run_as_admin"),
                ])
                run_index = len(options) - 2
                admin_index = len(options) - 1
            else:
                run_index = -1
                admin_index = -1
            
            options.extend([
                self.lang.get_text("compress"),
                self.lang.get_text("decompress"),
                self.lang.get_text("open_with"),
                self.lang.get_text("properties"),
                self.lang.get_text("create_shortcut"),
                self.lang.get_text("send_to"),
                self.lang.get_text("new_file"),
                self.lang.get_text("new_folder"),
                self.lang.get_text("back")
            ])
            
            # Calculate indices for the remaining options
            compress_index = len(options) - 9
            decompress_index = len(options) - 8
            open_with_index = len(options) - 7
            properties_index = len(options) - 6
            shortcut_index = len(options) - 5
            send_to_index = len(options) - 4
            new_file_index = len(options) - 3
            new_folder_index = len(options) - 2
            back_index = len(options) - 1
            
            # Create dynamic title based on selection
            if is_multi_selection:
                title = f"MULTI-SELECT MENU - {len(items_to_operate)} items selected"
            else:
                title = f"CONTEXT MENU - {os.path.basename(selected_path)}"
            
            choice = self.interactive.show_interactive_menu(title, options)
            
            if choice is None or choice == back_index:  # Back or Esc
                break
            elif choice == 0:  # Cut
                if is_multi_selection:
                    self.cut_multiple_to_clipboard(items_to_operate)
                else:
                    self.cut_to_clipboard(selected_path)
            elif choice == 1:  # Copy
                if is_multi_selection:
                    self.copy_multiple_to_clipboard(items_to_operate)
                else:
                    self.copy_to_clipboard(selected_path)
            elif choice == 2:  # Copy Path
                if is_multi_selection:
                    self.copy_multiple_paths_to_clipboard(items_to_operate)
                else:
                    self.copy_path_to_clipboard(selected_path)
            elif choice == 3:  # Paste
                self.paste_from_clipboard(os.path.dirname(selected_path))
            elif choice == 4:  # Delete
                if is_multi_selection:
                    if self.interactive.show_confirmation(
                        f"Delete {len(items_to_operate)} selected items?", default=False
                    ):
                        for item in items_to_operate:
                            self.enhanced_file_manager.delete_item(item)
                else:
                    item_type_name = "folder" if os.path.isdir(selected_path) else "file"
                    if self.interactive.show_confirmation(
                        f"Delete {item_type_name} '{os.path.basename(selected_path)}'?", default=False
                    ):
                        self.enhanced_file_manager.delete_item(selected_path)
            elif choice == rename_index and rename_index != -1:  # Rename (only for single selection)
                old_name = os.path.basename(selected_path)
                new_name = self.interactive.show_text_input(
                    "Enter new name (supports extension changes)", old_name, allow_extension_change=True
                )
                if new_name and new_name != old_name:
                    new_path = os.path.join(os.path.dirname(selected_path), new_name)
                    if self.enhanced_file_manager.move_item(selected_path, new_path):
                        print(f"✅ Successfully renamed '{old_name}' to '{new_name}'")
                        time.sleep(1)
            elif choice == move_index:  # Move
                dest = self._browse_path(select_type="dir")
                if dest:
                    if is_multi_selection:
                        for item in items_to_operate:
                            self.enhanced_file_manager.move_item(item, dest)
                    else:
                        self.enhanced_file_manager.move_item(selected_path, dest)
            elif choice == share_index:  # Share
                self.show_share_menu(selected_path)
            elif choice == run_index and run_index != -1:  # Run
                self.enhanced_file_manager.run_file(selected_path)
            elif choice == admin_index and admin_index != -1:  # Run as Admin
                self.enhanced_file_manager.run_as_admin(selected_path)
            elif choice == compress_index:  # Compress
                if is_multi_selection:
                    self.compress_multiple_items(items_to_operate)
                else:
                    self.compress_file(selected_path)
            elif choice == decompress_index:  # Decompress
                self.decompress_file(selected_path)
            elif choice == open_with_index:  # Open With
                self.show_open_with_menu(selected_path)
            elif choice == properties_index:  # Properties
                if is_multi_selection:
                    self.show_multiple_properties(items_to_operate)
                else:
                    self.enhanced_file_manager.show_properties(selected_path)
                    input("\nPress Enter to continue...")
            elif choice == shortcut_index:  # Create Shortcut
                if is_multi_selection:
                    self.create_multiple_shortcuts(items_to_operate)
                else:
                    self.create_shortcut(selected_path)
            elif choice == send_to_index:  # Send To
                if is_multi_selection:
                    self.send_multiple_to_location(items_to_operate)
                else:
                    self.show_send_to_menu(selected_path)
            elif choice == new_file_index:  # New File
                filename = self.interactive.show_text_input(
                    "Enter new file name (with extension)", "newfile.txt", allow_extension_change=True
                )
                if filename:
                    self.enhanced_file_manager.create_file(os.path.dirname(selected_path), filename)
            elif choice == new_folder_index:  # New Folder
                foldername = self.interactive.show_text_input("Enter new folder name")
                if foldername:
                    self.enhanced_file_manager.create_folder(os.path.dirname(selected_path), foldername)

    def cut_to_clipboard(self, path):
        """Cut file/folder to clipboard."""
        self.clipboard = [path]
        self.clipboard_operation = 'cut'
        item_type = "folder" if os.path.isdir(path) else "file"
        print(f"✂️ Cut {item_type} '{os.path.basename(path)}' to clipboard")
        time.sleep(1)

    def copy_to_clipboard(self, path):
        """Copy file/folder to clipboard."""
        self.clipboard = [path]
        self.clipboard_operation = 'copy'
        item_type = "folder" if os.path.isdir(path) else "file"
        print(f"📋 Copied {item_type} '{os.path.basename(path)}' to clipboard")
        time.sleep(1)
        
    def cut_multiple_to_clipboard(self, paths):
        """Cut multiple files/folders to clipboard."""
        self.clipboard = paths
        self.clipboard_operation = 'cut'
        print(f"✂️ Cut {len(paths)} items to clipboard:")
        for path in paths:
            print(f"  - {os.path.basename(path)}")
        time.sleep(1)
        
    def copy_multiple_to_clipboard(self, paths):
        """Copy multiple files/folders to clipboard."""
        self.clipboard = paths
        self.clipboard_operation = 'copy'
        print(f"📋 Copied {len(paths)} items to clipboard:")
        for path in paths:
            print(f"  - {os.path.basename(path)}")
        time.sleep(1)
        
    def copy_path_to_clipboard(self, path):
        """Copy file/folder path to clipboard."""
        try:
            abs_path = os.path.abspath(path)
            # Use PowerShell to copy path to clipboard
            ps_command = f'Set-Clipboard -Value "{abs_path}"'
            subprocess.run(["powershell", "-Command", ps_command], check=True)
            item_type = "folder" if os.path.isdir(path) else "file"
            print(f"📋 Copied {item_type} path to clipboard: {abs_path}")
        except Exception as e:
            print(f"❌ Error copying path to clipboard: {e}")
        time.sleep(1)
        
    def copy_multiple_paths_to_clipboard(self, paths):
        """Copy multiple file/folder paths to clipboard."""
        try:
            abs_paths = [os.path.abspath(path) for path in paths]
            paths_text = "\n".join(abs_paths)
            # Use PowerShell to copy paths to clipboard
            ps_command = f'Set-Clipboard -Value "{paths_text}"'
            subprocess.run(["powershell", "-Command", ps_command], check=True)
            print(f"📋 Copied {len(paths)} item paths to clipboard:")
            for path in abs_paths:
                print(f"  - {path}")
        except Exception as e:
            print(f"❌ Error copying paths to clipboard: {e}")
        time.sleep(1)

    def paste_from_clipboard(self, dest_dir):
        """Paste from clipboard to destination directory."""
        if not self.clipboard:
            print("📋 Clipboard is empty")
            time.sleep(1)
            return
        
        for item in self.clipboard:
            if not os.path.exists(item):
                print(f"❌ Source '{item}' no longer exists")
                continue
            
            dest_path = os.path.join(dest_dir, os.path.basename(item))
            item_type = "folder" if os.path.isdir(item) else "file"
            operation = "moved" if self.clipboard_operation == 'cut' else "copied"
            
            if self.clipboard_operation == 'cut':
                self.enhanced_file_manager.move_item(item, dest_path)
                print(f"✅ Moved {item_type} '{os.path.basename(item)}' to '{dest_dir}'")
            elif self.clipboard_operation == 'copy':
                self.enhanced_file_manager.copy_item(item, dest_path)
                print(f"✅ Copied {item_type} '{os.path.basename(item)}' to '{dest_dir}'")
        
        if self.clipboard_operation == 'cut':
            self.clipboard = []  # Clear clipboard after cut operation
        time.sleep(1)

    def show_share_menu(self, path):
        """Show share menu with configurable programs."""
        while True:
            options = list(self.share_programs.keys()) + ["➕ Add Program", "➖ Remove Program", "🔙 Back"]
            
            choice = self.interactive.show_interactive_menu(
                "SHARE WITH", options
            )
            
            if choice is None or choice == len(options) - 1:  # Back
                break
            elif choice == len(options) - 3:  # Add Program
                name = self.interactive.show_text_input("Enter program name")
                if name:
                    command = self.interactive.show_text_input("Enter command/executable")
                    if command:
                        self.share_programs[name] = command
            elif choice == len(options) - 2:  # Remove Program
                if self.share_programs:
                    remove_options = list(self.share_programs.keys())
                    remove_choice = self.interactive.show_interactive_menu(
                        "REMOVE PROGRAM", remove_options
                    )
                    if remove_choice is not None:
                        del self.share_programs[remove_options[remove_choice]]
            else:
                program_name = options[choice]
                command = self.share_programs[program_name]
                item_type = "folder" if os.path.isdir(path) else "file"
                
                # Handle multi-selection for sharing
                items_to_share = self.selected_items if self.selected_items else [path]
                
                # Display file paths and copy actual files/folders to clipboard
                print(f"\n📁 Sharing {len(items_to_share)} item(s) with {program_name}:")
                print("="*60)
                for i, item in enumerate(items_to_share, 1):
                    abs_path = os.path.abspath(item)
                    item_type = "📁" if os.path.isdir(item) else "📄"
                    print(f"  {i}. {item_type} {abs_path}")
                print("="*60)
                
                print(f"📋 Copying {len(items_to_share)} item(s) to clipboard...")
                
                try:
                    # Copy actual files/folders to clipboard using PowerShell
                    # This copies the actual files/folders, not just the paths
                    if len(items_to_share) == 1:
                        # Single item - use Get-Item directly
                        ps_command = f'Set-Clipboard -Path "{os.path.abspath(items_to_share[0])}"'
                    else:
                        # Multiple items - create an array of paths
                        paths_quoted = [f'"{os.path.abspath(item)}"' for item in items_to_share]
                        paths_array = ','.join(paths_quoted)
                        ps_command = f'Set-Clipboard -Path @({paths_array})'
                    
                    subprocess.run(["powershell", "-Command", ps_command], check=True)
                    print(f"✅ {len(items_to_share)} item(s) copied to clipboard (actual files/folders)!")
                    print("💡 You can now paste these items anywhere (Ctrl+V)!")
                except Exception as e:
                    print(f"⚠️ Could not copy items to clipboard: {e}")
                    print("📝 Fallback: Copying file paths as text...")
                    try:
                        # Fallback to copying paths as text
                        paths_text = "\n".join([os.path.abspath(item) for item in items_to_share])
                        ps_command = f'Set-Clipboard -Value "{paths_text}"'
                        subprocess.run(["powershell", "-Command", ps_command], check=True)
                        print(f"✅ {len(items_to_share)} file path(s) copied to clipboard as text!")
                    except Exception as e2:
                        print(f"❌ Could not copy paths to clipboard: {e2}")
                
                # Launch the external app
                try:
                    subprocess.run([command, path], check=False)
                    print(f"✅ Shared {item_type} '{os.path.basename(path)}' with {program_name}")
                    print(f"📋 File path is ready in clipboard for easy pasting!")
                except Exception as e:
                    print(f"❌ Error sharing {item_type} with {program_name}: {e}")
                time.sleep(2)  # Give more time to read the output

    def show_open_with_menu(self, path):
        """Show open with menu."""
        options = [
            "📝 Notepad",
            "💻 Visual Studio Code",
            "🔧 Default Program",
            "🔍 Choose Program",
            "🔙 Back"
        ]
        
        choice = self.interactive.show_interactive_menu(
            "OPEN WITH", options
        )
        
        if choice is None or choice == 4:  # Back
            return
        elif choice == 0:  # Notepad
            try:
                subprocess.run(["notepad", path], check=False)
            except Exception as e:
                print(f"❌ Error opening with Notepad: {e}")
        elif choice == 1:  # VS Code
            try:
                subprocess.run(["code", path], check=False)
            except Exception as e:
                print(f"❌ Error opening with VS Code: {e}")
        elif choice == 2:  # Default
            self.enhanced_file_manager.run_file(path)
        elif choice == 3:  # Choose Program
            program = self.interactive.show_text_input("Enter program path/command")
            if program:
                try:
                    subprocess.run([program, path], check=False)
                    print(f"✅ Opened with {program}")
                except Exception as e:
                    print(f"❌ Error opening with {program}: {e}")
        time.sleep(1)

    def show_send_to_menu(self, path):
        """Show send to menu with configurable locations."""
        while True:
            options = list(self.send_to_locations.keys()) + ["➕ Add Location", "➖ Remove Location", "🔙 Back"]
            
            choice = self.interactive.show_interactive_menu(
                "SEND TO", options
            )
            
            if choice is None or choice == len(options) - 1:  # Back
                break
            elif choice == len(options) - 3:  # Add Location
                name = self.interactive.show_text_input("Enter location name")
                if name:
                    location = self._browse_path(select_type="dir")
                    if location:
                        self.send_to_locations[name] = location
            elif choice == len(options) - 2:  # Remove Location
                if self.send_to_locations:
                    remove_options = list(self.send_to_locations.keys())
                    remove_choice = self.interactive.show_interactive_menu(
                        "REMOVE LOCATION", remove_options
                    )
                    if remove_choice is not None:
                        del self.send_to_locations[remove_options[remove_choice]]
            else:
                location_name = options[choice]
                dest_path = self.send_to_locations[location_name]
                item_type = "folder" if os.path.isdir(path) else "file"
                if os.path.exists(dest_path):
                    self.enhanced_file_manager.copy_item(path, dest_path)
                    print(f"✅ Sent {item_type} '{os.path.basename(path)}' to {location_name}")
                else:
                    print(f"❌ Location '{location_name}' does not exist")
                time.sleep(1)

    def compress_file(self, path):
        """Compress file or folder."""
        item_type = "folder" if os.path.isdir(path) else "file"
        archive_name = self.interactive.show_text_input(
            f"Enter archive name for {item_type} (without extension)", 
            os.path.basename(path)
        )
        if archive_name:
            if not archive_name.endswith('.zip'):
                archive_name += '.zip'
            archive_path = os.path.join(os.path.dirname(path), archive_name)
            self.enhanced_file_manager.compress_items([path], archive_path)
            print(f"✅ Compressed {item_type} '{os.path.basename(path)}' to '{archive_name}'")
            time.sleep(1)

    def decompress_file(self, path):
        """Decompress archive file."""
        if not path.lower().endswith('.zip'):
            print("❌ Only ZIP files are supported for decompression")
            time.sleep(1)
            return
        
        extract_to = self.interactive.show_text_input(
            "Enter extraction directory", 
            os.path.dirname(path)
        )
        if extract_to:
            self.enhanced_file_manager.decompress_archive(path, extract_to)
            time.sleep(1)

    def create_shortcut(self, path):
        """Create a shortcut to the file or folder."""
        if os.name != 'nt':
            print("❌ Shortcut creation is only supported on Windows")
            time.sleep(1)
            return
        
        item_type = "folder" if os.path.isdir(path) else "file"
        shortcut_name = self.interactive.show_text_input(
            f"Enter shortcut name for {item_type}", 
            os.path.basename(path)
        )
        if shortcut_name:
            if not shortcut_name.endswith('.lnk'):
                shortcut_name += '.lnk'
            
            shortcut_location = self._browse_path(select_type="dir")
            if shortcut_location:
                shortcut_path = os.path.join(shortcut_location, shortcut_name)
                try:
                    # Create shortcut using PowerShell
                    ps_cmd = f'''$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut("{shortcut_path}"); $Shortcut.TargetPath = "{path}"; $Shortcut.Save()'''
                    subprocess.run(["powershell", "-Command", ps_cmd], check=True)
                    print(f"✅ Shortcut created for {item_type}: {shortcut_path}")
                except Exception as e:
                    print(f"❌ Error creating shortcut for {item_type}: {e}")
                time.sleep(1)

    def _file_folder_menu(self):
        while True:
            options = [
                self.lang.get_text("select_files_folders"),
                self.lang.get_text("clear_current_selection"),
                self.lang.get_text("filter_selected_files"),
                self.lang.get_text("secure_delete_selected"),
                self.lang.get_text("mass_rename_selected"),
                self.lang.get_text("cut_selected_items"),
                self.lang.get_text("back_to_main")
            ]
            
            choice = self.interactive.show_interactive_menu(
                self.lang.get_text("file_folder_management_title"), 
                options,
                context_path=os.getcwd()
            )
            
            # Handle global operations
            if isinstance(choice, str) and choice.startswith('GLOBAL_'):
                if choice == 'GLOBAL_DELETE' and self.file_manager.selected_items:
                    # For file management, use the first selected item for deletion
                    selected_item = self.file_manager.selected_items[0]
                    self.handle_global_operation(choice, context_path=os.getcwd(), selected_item=selected_item)
                else:
                    self.handle_global_operation(choice, context_path=os.getcwd())
                continue
            
            if choice is None or choice == 6:  # Back or Esc
                break

            elif choice == 0:  # Select files/folders
                input_options = [
                    self.lang.get_text("manually_enter_paths"),
                    self.lang.get_text("browse_for_paths")
                ]
                input_method = self.interactive.show_interactive_menu(
                    self.lang.get_text("select_input_method"), input_options,
                    context_path=os.getcwd()
                )
                
                # Handle global operations
                if isinstance(input_method, str) and input_method.startswith('GLOBAL_'):
                    self.handle_global_operation(input_method, context_path=os.getcwd())
                    continue
                
                if input_method == 0:  # Manual entry
                    paths_input = self.interactive.show_text_input(
                        self.lang.get_text("enter_paths_comma_separated")
                    )
                    if paths_input:
                        self.file_manager.select_items(paths_input)
                elif input_method == 1:  # Browse
                    selected_path = self._browse_path(select_type="any")
                    if selected_path:
                        self.file_manager.select_items(selected_path)
                        
            elif choice == 1:  # Clear selection
                if self.interactive.show_confirmation(
                    self.lang.get_text("clear_all_selected"), default=True
                ):
                    self.file_manager.clear_selection()
                    
            elif choice == 2:  # Filter files
                extensions_input = self.interactive.show_text_input(
                    "Enter extensions (e.g., .txt, .jpg, comma-separated)"
                )
                extensions = [ext.strip() for ext in extensions_input.split(',')] if extensions_input else None
                
                min_size_input = self.interactive.show_text_input(
                    "Enter minimum size in bytes (leave empty for 0)"
                )
                min_size = int(min_size_input) if min_size_input and min_size_input.isdigit() else 0
                
                max_size_input = self.interactive.show_text_input(
                    "Enter maximum size in bytes (leave empty for unlimited)"
                )
                max_size = int(max_size_input) if max_size_input and max_size_input.isdigit() else float('inf')
                
                self.file_manager.filter_files(extensions, min_size, max_size)
                
            elif choice == 3:  # Secure delete
                if not self.file_manager.selected_items:
                    self.interactive.show_confirmation(
                        "No items selected for deletion.", default=True
                    )
                else:
                    # Show selected items
                    print("\n═" * 60)
                    print("🛡️ ITEMS TO BE DELETED:")
                    print("═" * 60)
                    for item in self.file_manager.selected_items:
                        print(f"  ❌ {item}")
                    print("─" * 60)
                    
                    if self.interactive.show_confirmation(
                        f"PERMANENTLY DELETE {len(self.file_manager.selected_items)} items?", 
                        default=False
                    ):
                        items_to_delete = list(self.file_manager.selected_items)
                        self.file_manager.secure_delete(items_to_delete)
                        
            elif choice == 4:  # Mass rename
                if not self.file_manager.selected_items:
                    self.interactive.show_confirmation(
                        "No items selected for renaming.", default=True
                    )
                else:
                    pattern = self.interactive.show_text_input(
                        "Enter new name pattern (e.g., 'document_{num}', use {num} for numbering)"
                    )
                    if pattern:
                        start_num_input = self.interactive.show_text_input(
                            "Enter starting number for rename", "1"
                        )
                        start_num = int(start_num_input) if start_num_input and start_num_input.isdigit() else 1
                        self.file_manager.mass_rename(pattern, start_num)
                        
            elif choice == 5:  # Cut items
                if not self.file_manager.selected_items:
                    self.interactive.show_confirmation(
                        "No items selected for cutting.", default=True
                    )
                else:
                    dest_options = [
                        "✏️ Manually Enter Path",
                        "🗂️ Browse for Path"
                    ]
                    dest_method = self.interactive.show_interactive_menu(
                        "CUT ITEMS - DESTINATION METHOD", dest_options
                    )
                    
                    dest = None
                    if dest_method == 0:  # Manual entry
                        dest = self.interactive.show_text_input("Enter destination folder")
                    elif dest_method == 1:  # Browse
                        dest = self._browse_path(select_type="dir")
                    
                    if dest:
                        self.file_manager.cut_selected(dest)

    def _content_menu(self):
        while True:
            options = [
                self.lang.get_text("extract_text_file"),
                self.lang.get_text("find_replace_file"),
                self.lang.get_text("back_to_main")
            ]
            
            choice = self.interactive.show_interactive_menu(
                self.lang.get_text("content_management_title"), 
                options,
                context_path=os.getcwd()
            )
            
            # Handle global operations
            if isinstance(choice, str) and choice.startswith('GLOBAL_'):
                self.handle_global_operation(choice, context_path=os.getcwd())
                continue
            
            if choice is None or choice == 2:  # Back or Esc
                break
            elif choice == 0:  # Extract text
                self._extract_text_submenu()
            elif choice == 1:  # Find/Replace
                self._find_replace_submenu()
    
    def _extract_text_submenu(self):
        """Extract text from file submenu."""
        while True:
            input_options = [
                "✏️ Manually Enter Path",
                "🗂️ Browse for File",
                "🔙 Back"
            ]
            
            input_method = self.interactive.show_interactive_menu(
                "EXTRACT TEXT - SELECT FILE", 
                input_options,
                context_path=os.getcwd()
            )
            
            # Handle global operations
            if isinstance(input_method, str) and input_method.startswith('GLOBAL_'):
                self.handle_global_operation(input_method, context_path=os.getcwd())
                continue
            
            if input_method is None or input_method == 2:  # Back
                break
            
            file_path = None
            if input_method == 0:  # Manual entry
                file_path = self.interactive.show_text_input(
                    "Enter file path to extract text from (.txt or .docx)"
                )
            elif input_method == 1:  # Browse
                file_path = self._browse_path(select_type="file")
            
            if file_path:
                text = self.content_manager.extract_text(file_path)
                if text:
                    print("\n" + "═" * 80)
                    print("📄 EXTRACTED CONTENT")
                    print("═" * 80)
                    # Show first 2000 characters with option to see more
                    display_text = text[:2000] + "..." if len(text) > 2000 else text
                    print(display_text)
                    print("─" * 80)
                    if len(text) > 2000:
                        print(f"📊 Showing first 2000 of {len(text)} characters")
                    print("─" * 80)
                    input("Press Enter to continue...")
                else:
                    print("❌ Could not extract text from file")
                    time.sleep(2)
            else:
                print("⚠️ No file selected")
                time.sleep(1)
    
    def _find_replace_submenu(self):
        """Find/Replace in file submenu."""
        while True:
            input_options = [
                "✏️ Manually Enter Path",
                "🗂️ Browse for File",
                "🔙 Back"
            ]
            
            input_method = self.interactive.show_interactive_menu(
                "FIND/REPLACE - SELECT FILE", 
                input_options,
                context_path=os.getcwd()
            )
            
            # Handle global operations
            if isinstance(input_method, str) and input_method.startswith('GLOBAL_'):
                self.handle_global_operation(input_method, context_path=os.getcwd())
                continue
            
            if input_method is None or input_method == 2:  # Back
                break
            
            file_path = None
            if input_method == 0:  # Manual entry
                file_path = self.interactive.show_text_input(
                    "Enter file path to perform find/replace (.txt files only)"
                )
            elif input_method == 1:  # Browse
                file_path = self._browse_path(select_type="file")
            
            if file_path:
                find_str = self.interactive.show_text_input("Enter string to find")
                if find_str:
                    replace_str = self.interactive.show_text_input("Enter string to replace with")
                    if replace_str is not None:  # Allow empty string
                        if self.interactive.show_confirmation(
                            f"Replace '{find_str}' with '{replace_str}' in {os.path.basename(file_path)}?",
                            default=False
                        ):
                            self.content_manager.find_replace_in_file(file_path, find_str, replace_str)
                            print("✅ Find/Replace operation completed")
                            time.sleep(2)
                        else:
                            print("❌ Operation cancelled")
                            time.sleep(1)
                    else:
                        print("❌ Operation cancelled")
                        time.sleep(1)
                else:
                    print("❌ No search string entered")
                    time.sleep(1)
            else:
                print("⚠️ No file selected")
                time.sleep(1)

    def _organization_menu(self):
        while True:
            options = [
                self.lang.get_text("organize_folders_rules"),
                self.lang.get_text("create_zip_archives"),
                self.lang.get_text("back_to_main")
            ]
            
            choice = self.interactive.show_interactive_menu(
                self.lang.get_text("organization_title"), 
                options,
                context_path=os.getcwd()
            )
            
            # Handle global operations
            if isinstance(choice, str) and choice.startswith('GLOBAL_'):
                self.handle_global_operation(choice, context_path=os.getcwd())
                continue
            
            if choice is None or choice == 2:  # Back or Esc
                break
            elif choice == 0:  # Organize folders
                self._organize_folders_submenu()
            elif choice == 1:  # Create zip archives
                self._create_zip_submenu()
    
    def _organize_folders_submenu(self):
        """Organize folders by rules submenu."""
        while True:
            input_options = [
                self.lang.get_text("manually_enter_path"),
                self.lang.get_text("browse_for_folder"),
                self.lang.get_text("back")
            ]
            
            input_method = self.interactive.show_interactive_menu(
                self.lang.get_text("select_folder_method"), 
                input_options,
                context_path=os.getcwd()
            )
            
            # Handle global operations
            if isinstance(input_method, str) and input_method.startswith('GLOBAL_'):
                self.handle_global_operation(input_method, context_path=os.getcwd())
                continue
            
            if input_method is None or input_method == 2:  # Back
                break
            
            folder = None
            if input_method == 0:  # Manual entry
                folder = self.interactive.show_text_input(
                    self.lang.get_text("enter_folder_path")
                )
            elif input_method == 1:  # Browse
                folder = self._browse_path(select_type="dir")
            
            if folder:
                rules_input = self.interactive.show_text_input(
                    self.lang.get_text("enter_organization_rules")
                )
                if rules_input:
                    rules = {}
                    for rule_pair in rules_input.split(','):
                        if ':' in rule_pair:
                            ext, dest = rule_pair.strip().split(':', 1)
                            rules[ext.strip()] = dest.strip()
                    if rules:
                        self.org_automation.organize_by_rules(folder, rules)
                        print(self.lang.get_text("folder_organization_completed"))
                        time.sleep(2)
                    else:
                        print(self.lang.get_text("no_valid_rules"))
                        time.sleep(1)
                else:
                    print(self.lang.get_text("no_rules_entered"))
                    time.sleep(1)
            else:
                print("⚠️ No folder selected")
                time.sleep(1)
    
    def _create_zip_submenu(self):
        """Create zip archives submenu."""
        if not self.file_manager.selected_items:
            print(self.lang.get_text("no_files_for_zipping"))
            time.sleep(1)
            return
        
        # Pass the selected items directly, create_zip_archives will handle filtering
        self.org_automation.create_zip_archives(self.file_manager.selected_items)
        print(self.lang.get_text("zip_creation_completed"))
        time.sleep(2)

    def _media_menu(self):
        while True:
            options = [
                self.lang.get_text("create_playlist"),
                self.lang.get_text("mass_extract_audio"),
                self.lang.get_text("mass_trim_videos"),
                self.lang.get_text("back_to_main")
            ]
            
            choice = self.interactive.show_interactive_menu(
                self.lang.get_text("media_handling_title"), 
                options,
                context_path=os.getcwd()
            )
            
            # Handle global operations
            if isinstance(choice, str) and choice.startswith('GLOBAL_'):
                self.handle_global_operation(choice, context_path=os.getcwd())
                continue
            
            if choice is None or choice == 3:  # Back or Esc
                break
            elif choice == 0:  # Create Playlist
                self._create_playlist()
            elif choice == 1:  # Mass Extract Audio Segments
                self._mass_extract_audio()
            elif choice == 2:  # Mass Trim Videos
                self._mass_trim_videos()
    
    def _create_playlist(self):
        """Create a playlist from selected media files."""
        if not self.file_manager.selected_items:
            print(self.lang.get_text("no_media_files"))
            time.sleep(1)
            return
        
        playlist_name = self.interactive.show_text_input(
            self.lang.get_text("enter_playlist_name")
        ) or "playlist.m3u"
        self.media_handler.create_playlist(self.file_manager.selected_items, playlist_name)
        print(self.lang.get_text("playlist_created"))
        time.sleep(2)
    
    def _mass_extract_audio(self):
        """Mass extract audio segments from media files."""
        while True:
            input_options = [
                self.lang.get_text("use_selected_files"),
                self.lang.get_text("specify_new_file"),
                self.lang.get_text("back")
            ]
            
            input_method = self.interactive.show_interactive_menu(
                "MASS EXTRACT AUDIO - SELECT FILES", 
                input_options,
                context_path=os.getcwd()
            )
            
            # Handle global operations
            if isinstance(input_method, str) and input_method.startswith('GLOBAL_'):
                self.handle_global_operation(input_method, context_path=os.getcwd())
                continue
            
            if input_method is None or input_method == 2:  # Back
                break
            
            files_to_process = []
            if input_method == 0:  # Use selected files
                files_to_process = self.file_manager.selected_items
                if not files_to_process:
                    print(self.lang.get_text("no_files_selected"))
                    time.sleep(1)
                    continue
            elif input_method == 1:  # Specify new file
                file_path = self._browse_path(select_type="file")
                if file_path:
                    files_to_process = [file_path]
                else:
                    print("⚠️ No file selected.")
                    time.sleep(1)
                    continue
            
            try:
                start_ms = int(self.interactive.show_text_input(self.lang.get_text("enter_start_time_ms")))
                end_ms = int(self.interactive.show_text_input(self.lang.get_text("enter_end_time_ms")))
                output_prefix = self.interactive.show_text_input(
                    self.lang.get_text("enter_output_prefix_audio")
                ) or "output_audio"
                self.media_handler.extract_audio_segment(files_to_process, start_ms, end_ms, output_prefix)
                print(self.lang.get_text("audio_segments_extracted"))
                time.sleep(2)
            except ValueError:
                print(self.lang.get_text("invalid_time_input"))
                time.sleep(2)
    
    def _mass_trim_videos(self):
        """Mass trim video files."""
        while True:
            input_options = [
                "🗂️ Use Selected Files",
                "✏️ Specify New File",
                "🔙 Back"
            ]
            
            input_method = self.interactive.show_interactive_menu(
                "MASS TRIM VIDEOS - SELECT FILES", 
                input_options,
                context_path=os.getcwd()
            )
            
            # Handle global operations
            if isinstance(input_method, str) and input_method.startswith('GLOBAL_'):
                self.handle_global_operation(input_method, context_path=os.getcwd())
                continue
            
            if input_method is None or input_method == 2:  # Back
                break
            
            files_to_process = []
            if input_method == 0:  # Use selected files
                files_to_process = self.file_manager.selected_items
                if not files_to_process:
                    print("⚠️ No files currently selected.")
                    time.sleep(1)
                    continue
            elif input_method == 1:  # Specify new file
                file_path = self._browse_path(select_type="file")
                if file_path:
                    files_to_process = [file_path]
                else:
                    print("⚠️ No file selected.")
                    time.sleep(1)
                    continue
            
            try:
                start_sec = float(self.interactive.show_text_input("Enter start time in seconds (e.g., 5.5)"))
                end_sec = float(self.interactive.show_text_input("Enter end time in seconds (e.g., 60.0)"))
                output_prefix = self.interactive.show_text_input(
                    "Enter output filename prefix (e.g., 'trimmed', default 'output_video')"
                ) or "output_video"
                self.media_handler.trim_video(files_to_process, start_sec, end_sec, output_prefix)
                print("✅ Videos trimmed")
                time.sleep(2)
            except ValueError:
                print("❌ Invalid time input. Please enter numbers.")
                time.sleep(2)

    def _info_menu(self):
        while True:
            options = [
                self.lang.get_text("calculate_size"),
                self.lang.get_text("compare_sizes"),
                self.lang.get_text("add_file_description"),
                self.lang.get_text("view_file_description"),
                self.lang.get_text("directory_mapping"),
                self.lang.get_text("back_to_main")
            ]
            
            choice = self.interactive.show_interactive_menu(
                self.lang.get_text("information_title"), 
                options,
                context_path=os.getcwd()
            )
            
            # Handle global operations
            if isinstance(choice, str) and choice.startswith('GLOBAL_'):
                self.handle_global_operation(choice, context_path=os.getcwd())
                continue
            
            if choice is None or choice == 5:  # Back or Esc
                break
            elif choice == 0:  # Calculate size
                self._calculate_size_submenu()
            elif choice == 1:  # Compare sizes
                self._compare_sizes_submenu()
            elif choice == 2:  # Add file description
                self._add_file_description_submenu()
            elif choice == 3:  # View file description
                self._view_file_description_submenu()
            elif choice == 4:  # Directory mapping
                self._directory_mapping_submenu()
    
    def _calculate_size_submenu(self):
        """Calculate size submenu."""
        while True:
            input_options = [
                "🗂️ Use Selected Files",
                "🔍 Browse for Path",
                "✏️ Manually Enter Paths",
                "🔙 Back"
            ]
            
            input_method = self.interactive.show_interactive_menu(
                "CALCULATE SIZE - SELECT FILES", 
                input_options,
                context_path=os.getcwd()
            )
            
            # Handle global operations
            if isinstance(input_method, str) and input_method.startswith('GLOBAL_'):
                self.handle_global_operation(input_method, context_path=os.getcwd())
                continue
            
            if input_method is None or input_method == 3:  # Back
                break
            
            paths_to_calc = []
            if input_method == 0:  # Use current selection
                paths_to_calc = self.file_manager.selected_items
            elif input_method == 1:  # Browse
                selected_path = self._browse_path(select_type="any")
                if selected_path:
                    paths_to_calc = [selected_path]
            elif input_method == 2:  # Manual entry
                paths_input_str = self.interactive.show_text_input(
                    "Enter paths (comma-separated, leave empty for current selection)"
                )
                if paths_input_str:
                    paths_to_calc = [p.strip() for p in paths_input_str.split(',')]
                else:
                    paths_to_calc = self.file_manager.selected_items
            
            if not paths_to_calc:
                print("⚠️ No paths specified or selected for size calculation.")
                time.sleep(1)
            else:
                total_bytes = self.file_manager.calculate_size(paths_to_calc)
                total_gb = total_bytes / self.gb_conversion_factor
                print(f"📏 Total size: {total_bytes} bytes ({total_gb:.2f} GB)")
                time.sleep(2)
    
    def _compare_sizes_submenu(self):
        """Compare sizes submenu."""
        if not self.file_manager.selected_items:
            print("⚠️ No items selected for comparison.")
            time.sleep(1)
            return
        
        selected_bytes = self.file_manager.calculate_size(self.file_manager.selected_items)
        selected_gb = selected_bytes / self.gb_conversion_factor
        print(f"📏 Size of current selection: {selected_bytes} bytes ({selected_gb:.2f} GB)")
        
        while True:
            input_options = [
                "🔍 Browse for Path",
                "✏️ Manually Enter Path",
                "🔙 Back"
            ]
            
            input_method = self.interactive.show_interactive_menu(
                "COMPARE SIZES - SELECT COMPARISON PATH", 
                input_options,
                context_path=os.getcwd()
            )
            
            # Handle global operations
            if isinstance(input_method, str) and input_method.startswith('GLOBAL_'):
                self.handle_global_operation(input_method, context_path=os.getcwd())
                continue
            
            if input_method is None or input_method == 2:  # Back
                break
            
            compare_path = None
            if input_method == 0:  # Browse
                compare_path = self._browse_path(select_type="any")
            elif input_method == 1:  # Manual entry
                compare_path = self.interactive.show_text_input("Enter path to compare with")
            
            if compare_path:
                compare_path_normalized = self.file_manager._normalize_path(compare_path)

                if not os.path.exists(compare_path_normalized):
                    print("❌ Comparison path not found.")
                    time.sleep(1)
                else:
                    compare_bytes = self.file_manager.calculate_size([compare_path_normalized])
                    compare_gb = compare_bytes / self.gb_conversion_factor
                    print(f"📏 Size of '{compare_path_normalized}': {compare_bytes} bytes ({compare_gb:.2f} GB)")
                    
                    if selected_bytes > compare_bytes:
                        print("📊 Current selection is larger.")
                    elif selected_bytes < compare_bytes:
                        print("📊 Current selection is smaller.")
                    else:
                        print("📏 Sizes are equal.")
                    time.sleep(2)
            else:
                print("⚠️ No comparison path selected.")
                time.sleep(1)
    
    def _add_file_description_submenu(self):
        """Add file description submenu."""
        while True:
            input_options = [
                "✏️ Manually Enter Path",
                "🗂️ Browse for File",
                "🔙 Back"
            ]
            
            input_method = self.interactive.show_interactive_menu(
                "ADD FILE DESCRIPTION - SELECT FILE", 
                input_options,
                context_path=os.getcwd()
            )
            
            # Handle global operations
            if isinstance(input_method, str) and input_method.startswith('GLOBAL_'):
                self.handle_global_operation(input_method, context_path=os.getcwd())
                continue
            
            if input_method is None or input_method == 2:  # Back
                break
            
            file_path = None
            if input_method == 0:  # Manual entry
                file_path = self.interactive.show_text_input("Enter file path to add description to")
            elif input_method == 1:  # Browse
                file_path = self._browse_path(select_type="file")
            
            if file_path:
                normalized_path = self.file_manager._normalize_path(file_path)
                if os.path.exists(normalized_path):
                    description = self.interactive.show_text_input("Enter description")
                    self.custom_descriptions[normalized_path] = description
                    print(f"✅ Description added for '{normalized_path}'.")
                    time.sleep(2)
                else:
                    print("❌ File not found.")
                    time.sleep(1)
            else:
                print("⚠️ No file selected")
                time.sleep(1)
    
    def _view_file_description_submenu(self):
        """View file description submenu."""
        while True:
            input_options = [
                "✏️ Manually Enter Path",
                "🗂️ Browse for File",
                "🔙 Back"
            ]
            
            input_method = self.interactive.show_interactive_menu(
                "VIEW FILE DESCRIPTION - SELECT FILE", 
                input_options,
                context_path=os.getcwd()
            )
            
            # Handle global operations
            if isinstance(input_method, str) and input_method.startswith('GLOBAL_'):
                self.handle_global_operation(input_method, context_path=os.getcwd())
                continue
            
            if input_method is None or input_method == 2:  # Back
                break
            
            file_path = None
            if input_method == 0:  # Manual entry
                file_path = self.interactive.show_text_input("Enter file path to view description")
            elif input_method == 1:  # Browse
                file_path = self._browse_path(select_type="file")
            
            if file_path:
                normalized_path = self.file_manager._normalize_path(file_path)
                if normalized_path in self.custom_descriptions:
                    print(f"📄 Description for '{normalized_path}': {self.custom_descriptions[normalized_path]}")
                else:
                    print("❌ No description found for this file.")
                time.sleep(2)
            else:
                print("⚠️ No file selected")
                time.sleep(1)
    
    def _directory_mapping_submenu(self):
        """Directory mapping submenu."""
        while True:
            input_options = [
                "✏️ Manually Enter Path",
                "🗺️ Browse for Directory",
                "🔙 Back"
            ]
            
            input_method = self.interactive.show_interactive_menu(
                "DIRECTORY MAPPING - SELECT DIRECTORY", 
                input_options,
                context_path=os.getcwd()
            )
            
            # Handle global operations
            if isinstance(input_method, str) and input_method.startswith('GLOBAL_'):
                self.handle_global_operation(input_method, context_path=os.getcwd())
                continue
            
            if input_method is None or input_method == 2:  # Back
                break
            
            dir_path = None
            if input_method == 0:  # Manual entry
                dir_path = self.interactive.show_text_input("Enter directory path to map")
            elif input_method == 1:  # Browse
                dir_path = self._browse_path(select_type="dir")
            
            if dir_path:
                self.directory_mapper.map_directory(dir_path)
                # directory_mapper handles its own input and pausing
            else:
                print("⚠️ No directory selected")
                time.sleep(1)

    def browse_files_no_purpose(self):
        """General file browsing with full action support."""
        self.interactive.hide_cursor()
        try:
            while True:
                selected_path = self._browse_path(select_type="any")
                if selected_path is None:
                    break

                # Context menu
                self.show_context_menu(selected_path)
                
        finally:
            self.interactive.show_cursor()

    def _general_browsing_and_management_menu(self):
        """Combined general browsing and file management menu."""
        while True:
            options = [
                self.lang.get_text("file_browsing"),
                self.lang.get_text("select_files_folders"),
                self.lang.get_text("back_to_main")
            ]
            
            choice = self.interactive.show_interactive_menu(
                self.lang.get_text("general_browsing_and_management_title"), 
                options,
                context_path=os.getcwd()
            )
            
            # Handle global operations
            if isinstance(choice, str) and choice.startswith('GLOBAL_'):
                if choice == 'GLOBAL_DELETE' and self.file_manager.selected_items:
                    # For file management, use the first selected item for deletion
                    selected_item = self.file_manager.selected_items[0]
                    self.handle_global_operation(choice, context_path=os.getcwd(), selected_item=selected_item)
                else:
                    self.handle_global_operation(choice, context_path=os.getcwd())
                continue
            
            if choice is None or choice == 2:  # Back or Esc
                break

            elif choice == 0:  # File browsing
                self.browse_files_no_purpose()
                
            elif choice == 1:  # Select files/folders
                self._select_files_folders_menu()

    def _select_files_folders_menu(self):
        """Operations for selected files and folders."""
        while True:
            options = [
                self.lang.get_text("manually_enter_paths"),
                self.lang.get_text("browse_for_paths"),
                self.lang.get_text("selected_files_operations"),
                self.lang.get_text("clear_current_selection"),
                self.lang.get_text("back_to_main")
            ]

            choice = self.interactive.show_interactive_menu(
                self.lang.get_text("select_input_method"),
                options,
                context_path=os.getcwd()
            )

            if choice is None or choice == 4:  # Back or Esc
                break

            elif choice == 0:  # Manual entry
                paths_input = self.interactive.show_text_input(
                    self.lang.get_text("enter_paths_comma_separated")
                )
                if paths_input:
                    self.file_manager.select_items(paths_input)
                    
            elif choice == 1:  # Browse
                selected_path = self._browse_path(select_type="any")
                if selected_path:
                    self.file_manager.select_items(selected_path)
                    
            elif choice == 2:  # Selected files operations menu
                self._selected_files_operations_submenu()

            elif choice == 3:  # Clear selection
                if self.interactive.show_confirmation(
                    self.lang.get_text("clear_all_selected"), default=True
                ):
                    self.file_manager.clear_selection()

            
    def _selected_files_operations_submenu(self):
        """Operations for selected files."""
        while True:
            options = [
                self.lang.get_text("filter_selected_files"),
                self.lang.get_text("secure_delete_selected"),
                self.lang.get_text("mass_rename_selected"),
                self.lang.get_text("cut_selected_items"),
                self.lang.get_text("back_to_main")
            ]

            choice = self.interactive.show_interactive_menu(
                self.lang.get_text("selected_files_operations_title"),
                options,
                context_path=os.getcwd()
            )

            if choice is None or choice == 4:  # Back or Esc
                break

            elif choice == 0:  # Filter files
                extensions_input = self.interactive.show_text_input(
                    "Enter extensions (e.g., .txt, .jpg, comma-separated)"
                )
                extensions = [ext.strip() for ext in extensions_input.split(',')] if extensions_input else None
                
                min_size_input = self.interactive.show_text_input(
                    "Enter minimum size in bytes (leave empty for 0)"
                )
                min_size = int(min_size_input) if min_size_input and min_size_input.isdigit() else 0
                
                max_size_input = self.interactive.show_text_input(
                    "Enter maximum size in bytes (leave empty for unlimited)"
                )
                max_size = int(max_size_input) if max_size_input and max_size_input.isdigit() else float('inf')
                
                self.file_manager.filter_files(extensions, min_size, max_size)

            elif choice == 1:  # Secure delete
                if not self.file_manager.selected_items:
                    self.interactive.show_confirmation(
                        "No items selected for deletion.", default=True
                    )
                else:
                    # Show selected items
                    print("\n═" * 60)
                    print("🛡️ ITEMS TO BE DELETED:")
                    print("═" * 60)
                    for item in self.file_manager.selected_items:
                        print(f"  ❌ {item}")
                    print("─" * 60)
                    
                    if self.interactive.show_confirmation(
                        f"PERMANENTLY DELETE {len(self.file_manager.selected_items)} items?", 
                        default=False
                    ):
                        items_to_delete = list(self.file_manager.selected_items)
                        self.file_manager.secure_delete(items_to_delete)
                        
            elif choice == 2:  # Mass rename
                if not self.file_manager.selected_items:
                    self.interactive.show_confirmation(
                        "No items selected for renaming.", default=True
                    )
                else:
                    pattern = self.interactive.show_text_input(
                        "Enter new name pattern (e.g., 'document_{num}', use {num} for numbering)"
                    )
                    if pattern:
                        start_num_input = self.interactive.show_text_input(
                            "Enter starting number for rename", "1"
                        )
                        start_num = int(start_num_input) if start_num_input and start_num_input.isdigit() else 1
                        self.file_manager.mass_rename(pattern, start_num)
                        
            elif choice == 3:  # Cut items
                if not self.file_manager.selected_items:
                    self.interactive.show_confirmation(
                        "No items selected for cutting.", default=True
                    )
                else:
                    dest_options = [
                        "✏️ Manually Enter Path",
                        "🗂️ Browse for Path"
                    ]
                    dest_method = self.interactive.show_interactive_menu(
                        "CUT ITEMS - DESTINATION METHOD", dest_options
                    )
                    
                    dest = None
                    if dest_method == 0:  # Manual entry
                        dest = self.interactive.show_text_input("Enter destination folder")
                    elif dest_method == 1:  # Browse
                        dest = self._browse_path(select_type="dir")
                    
                    if dest:
                        self.file_manager.cut_selected(dest)


    def show_settings(self):
        """Show settings menu with language and browsing options."""
        while True:
            options = [
                self.lang.get_text("browse_start_mode"),
                self.lang.get_text("language_settings"),
                "🔍 Global Search Settings",
                self.lang.get_text("back_to_main")
            ]
            
            choice = self.interactive.show_interactive_menu(
                self.lang.get_text("settings_menu"), 
                options,
                context_path=os.getcwd()
            )
            
            # Handle global operations
            if isinstance(choice, str) and choice.startswith('GLOBAL_'):
                self.handle_global_operation(choice, context_path=os.getcwd())
                continue
            
            if choice is None or choice == 3:  # Back
                break
            elif choice == 0:  # Browse start mode
                self.show_browse_start_mode_settings()
            elif choice == 1:  # Language settings
                self.show_language_settings()
            elif choice == 2:  # Global search settings
                self.show_global_search_settings()
    
    def show_browse_start_mode_settings(self):
        """Show browse start mode settings."""
        while True:
            start_mode_options = [
                self.lang.get_text("default_drives"),
                self.lang.get_text("project_starting"),
                self.lang.get_text("custom_location")
            ]

            current_mode = self.settings["browse_start_mode"]
            current_path = ""
            if current_mode == "custom":
                current_path = f" (Current: {self.settings['custom_start_path']})"
            elif current_mode == "project":
                current_path = f" (Current: {self.settings['project_start_path']})"
            
            print(f"\n--- Settings - Browse Start Mode: {current_mode.title()}{current_path} ---")
            initial_choice = {"default": 0, "project": 1, "custom": 2}[self.settings["browse_start_mode"]]
            start_mode_choice = self.interactive.show_interactive_menu(
                self.lang.get_text("browse_start_selection"), start_mode_options, initial_choice,
                context_path=os.getcwd()
            )

            # Handle global operations
            if isinstance(start_mode_choice, str) and start_mode_choice.startswith('GLOBAL_'):
                self.handle_global_operation(start_mode_choice, context_path=os.getcwd())
                continue

            if start_mode_choice is None:
                break
            elif start_mode_choice == 0:
                self.settings["browse_start_mode"] = "default"
            elif start_mode_choice == 1:
                self.settings["browse_start_mode"] = "project"
            elif start_mode_choice == 2:
                # Ask how to set custom location
                custom_options = [
                    "Browse for Location",
                    "Manually Enter Path"
                ]
                custom_choice = self.interactive.show_interactive_menu(
                    "Set Custom Location", custom_options,
                    context_path=os.getcwd()
                )
                
                # Handle global operations
                if isinstance(custom_choice, str) and custom_choice.startswith('GLOBAL_'):
                    self.handle_global_operation(custom_choice, context_path=os.getcwd())
                    continue
                
                if custom_choice == 0:  # Browse
                    custom_path = self._browse_path(select_type="dir")
                    if custom_path:
                        self.settings["browse_start_mode"] = "custom"
                        self.settings["custom_start_path"] = os.path.abspath(custom_path)
                elif custom_choice == 1:  # Manual entry
                    custom_path = self.interactive.show_text_input("Enter custom start path")
                    if custom_path and os.path.isdir(custom_path):
                        self.settings["browse_start_mode"] = "custom"
                        self.settings["custom_start_path"] = os.path.abspath(custom_path)
                    elif custom_path:
                        self.interactive.show_confirmation("Invalid directory path.", default=True)
    
    def show_global_search_settings(self):
        """Show global search configuration settings."""
        while True:
            # Create dynamic options based on current settings
            scope_text = {
                "system": "🌐 System-wide (All drives)",
                "current_dir": "📁 Current Directory",
                "custom": "📍 Custom Directory"
            }
            
            current_scope = self.settings.get("global_search_scope", "system")
            enabled_status = "✅ Enabled" if self.settings.get("global_search_enabled", True) else "❌ Disabled"
            
            options = [
                f"🔍 Global Search: {enabled_status}",
                f"📂 Search Scope: {scope_text.get(current_scope, 'Unknown')}",
                "📁 Set Custom Search Directory",
                "🔙 Back"
            ]
            
            choice = self.interactive.show_interactive_menu(
                "GLOBAL SEARCH SETTINGS",
                options,
                context_path=os.getcwd()
            )
            
            # Handle global operations
            if isinstance(choice, str) and choice.startswith('GLOBAL_'):
                self.handle_global_operation(choice, context_path=os.getcwd())
                continue
            
            if choice is None or choice == 3:  # Back
                break
            elif choice == 0:  # Toggle global search
                self.settings["global_search_enabled"] = not self.settings.get("global_search_enabled", True)
                status = "enabled" if self.settings["global_search_enabled"] else "disabled"
                print(f"✅ Global search {status}")
                self.save_settings()
                time.sleep(1)
            elif choice == 1:  # Change search scope
                scope_options = [
                    "🌐 System-wide (All drives)",
                    "📁 Current Directory",
                    "📍 Custom Directory",
                    "🔙 Back"
                ]
                
                scope_choice = self.interactive.show_interactive_menu(
                    "SELECT SEARCH SCOPE",
                    scope_options,
                    context_path=os.getcwd()
                )
                
                if scope_choice == 0:
                    self.settings["global_search_scope"] = "system"
                    print("✅ Search scope set to system-wide")
                    self.save_settings()
                    time.sleep(1)
                elif scope_choice == 1:
                    self.settings["global_search_scope"] = "current_dir"
                    print("✅ Search scope set to current directory")
                    self.save_settings()
                    time.sleep(1)
                elif scope_choice == 2:
                    self.settings["global_search_scope"] = "custom"
                    print("✅ Search scope set to custom directory")
                    self.save_settings()
                    time.sleep(1)
                    
            elif choice == 2:  # Set custom directory
                custom_options = [
                    "🗂️ Browse for Directory",
                    "✏️ Manually Enter Path",
                    "🔙 Back"
                ]
                
                custom_choice = self.interactive.show_interactive_menu(
                    "SET CUSTOM SEARCH DIRECTORY",
                    custom_options,
                    context_path=os.getcwd()
                )
                
                if custom_choice == 0:  # Browse
                    custom_path = self._browse_path(select_type="dir")
                    if custom_path:
                        self.settings["global_search_default_dir"] = os.path.abspath(custom_path)
                        print(f"✅ Custom search directory set to: {custom_path}")
                        self.save_settings()
                        time.sleep(2)
                elif custom_choice == 1:  # Manual entry
                    custom_path = self.interactive.show_text_input(
                        "Enter custom search directory path",
                        self.settings.get("global_search_default_dir", os.path.expanduser("~"))
                    )
                    if custom_path and os.path.isdir(custom_path):
                        self.settings["global_search_default_dir"] = os.path.abspath(custom_path)
                        print(f"✅ Custom search directory set to: {custom_path}")
                        self.save_settings()
                        time.sleep(2)
                    elif custom_path:
                        self.interactive.show_confirmation("Invalid directory path.", default=True)
    
    def show_language_settings(self):
        """Show language selection menu."""
        while True:
            options = [
                self.lang.get_text("english"),
                self.lang.get_text("bulgarian"),
                self.lang.get_text("back")
            ]
            
            # Mark current language
            current_lang = self.lang.current_language
            if current_lang == "en":
                options[0] += " ✓"
            elif current_lang == "bg":
                options[1] += " ✓"
            
            choice = self.interactive.show_interactive_menu(
                self.lang.get_text("language_selection"), 
                options,
                context_path=os.getcwd()
            )
            
            # Handle global operations
            if isinstance(choice, str) and choice.startswith('GLOBAL_'):
                self.handle_global_operation(choice, context_path=os.getcwd())
                continue
            
            if choice is None or choice == 2:  # Back
                break
            elif choice == 0:  # English
                if self.lang.set_language("en"):
                    print(self.lang.get_text("language_changed", "English"))
                    print(self.lang.get_text("restart_required"))
                    time.sleep(2)
                    break
            elif choice == 1:  # Bulgarian
                if self.lang.set_language("bg"):
                    print(self.lang.get_text("language_changed", "Български"))
                    print(self.lang.get_text("restart_required"))
                    time.sleep(2)
                    break

    def run(self):
        """Main application loop with interactive menu."""
        while True:
            options = [
                self.lang.get_text("general_browsing_and_management"),
                self.lang.get_text("content_management"),
                self.lang.get_text("organization_automation"),
                self.lang.get_text("media_handling"),
                self.lang.get_text("information_misc"),
                "🔍 Global Search",
                self.lang.get_text("settings"),
                self.lang.get_text("exit_application")
            ]
            
            choice = self.interactive.show_interactive_menu(
                self.lang.get_text("app_title", VERSION, VERSION_DATE), 
                options,
                context_path=os.getcwd()
            )
            
            # Handle global operations
            if isinstance(choice, str) and choice.startswith('GLOBAL_'):
                self.handle_global_operation(choice, context_path=os.getcwd())
                continue
            
            if choice is None or choice == 7:  # Exit or Esc
                print("\n" + self.lang.get_text("exiting_app"))
                break
            elif choice == 0:
                self._general_browsing_and_management_menu()
            elif choice == 1:
                self._content_menu()
            elif choice == 2:
                self._organization_menu()
            elif choice == 3:
                self._media_menu()
            elif choice == 4:
                self._info_menu()
            elif choice == 5:
                self.show_global_search_menu()
            elif choice == 6:
                self.show_settings()

    def compress_multiple_items(self, items):
        """Compress multiple files/folders into a single archive."""
        archive_name = self.interactive.show_text_input(
            f"Enter archive name for {len(items)} items (without extension)", 
            "multi_archive"
        )
        if archive_name:
            if not archive_name.endswith('.zip'):
                archive_name += '.zip'
            # Use the directory of the first item as the archive location
            archive_path = os.path.join(os.path.dirname(items[0]), archive_name)
            self.enhanced_file_manager.compress_items(items, archive_path)
            print(f"✅ Compressed {len(items)} items to '{archive_name}'")
            time.sleep(1)
    
    def show_multiple_properties(self, items):
        """Show properties for multiple items."""
        print("\n" + "═" * 80)
        print(f"🔍 PROPERTIES: {len(items)} selected items")
        print("═" * 80)
        
        total_size = 0
        file_count = 0
        dir_count = 0
        
        for i, item in enumerate(items, 1):
            print(f"\n📁 Item {i}: {os.path.basename(item)}")
            print(f"📍 Path: {item}")
            
            if os.path.isdir(item):
                dir_count += 1
                print("📂 Type: Directory")
                try:
                    item_count = len(os.listdir(item))
                    print(f"📊 Contents: {item_count} items")
                except:
                    print("📊 Contents: Access denied")
            else:
                file_count += 1
                print("📄 Type: File")
                try:
                    size = os.path.getsize(item)
                    total_size += size
                    print(f"📊 Size: {size:,} bytes")
                except:
                    print("📊 Size: Unknown")
        
        print("\n" + "─" * 80)
        print(f"📊 SUMMARY: {file_count} files, {dir_count} directories")
        print(f"📊 Total size: {total_size:,} bytes ({total_size/(1024**3):.2f} GB)")
        print("─" * 80)
    
    def create_multiple_shortcuts(self, items):
        """Create shortcuts for multiple items."""
        if os.name != 'nt':
            print("❌ Shortcut creation is only supported on Windows")
            time.sleep(1)
            return
        
        shortcut_location = self._browse_path(select_type="dir")
        if shortcut_location:
            for item in items:
                item_name = os.path.basename(item)
                shortcut_name = f"{item_name}.lnk"
                shortcut_path = os.path.join(shortcut_location, shortcut_name)
                
                try:
                    ps_cmd = f'''$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut("{shortcut_path}"); $Shortcut.TargetPath = "{item}"; $Shortcut.Save()'''
                    subprocess.run(["powershell", "-Command", ps_cmd], check=True)
                    print(f"✅ Shortcut created: {shortcut_name}")
                except Exception as e:
                    print(f"❌ Error creating shortcut for {item_name}: {e}")
            time.sleep(1)
    
    def send_multiple_to_location(self, items):
        """Send multiple items to a location."""
        while True:
            options = list(self.send_to_locations.keys()) + ["🔗 Browse for Location", "🔙 Back"]
            
            choice = self.interactive.show_interactive_menu(
                f"SEND {len(items)} ITEMS TO", options
            )
            
            if choice is None or choice == len(options) - 1:  # Back
                break
            elif choice == len(options) - 2:  # Browse for Location
                dest_path = self._browse_path(select_type="dir")
                if dest_path:
                    for item in items:
                        item_name = os.path.basename(item)
                        dest_item_path = os.path.join(dest_path, item_name)
                        self.enhanced_file_manager.copy_item(item, dest_item_path)
                        print(f"✅ Sent '{item_name}' to {dest_path}")
                    time.sleep(1)
            else:
                location_name = options[choice]
                dest_path = self.send_to_locations[location_name]
                if os.path.exists(dest_path):
                    for item in items:
                        item_name = os.path.basename(item)
                        dest_item_path = os.path.join(dest_path, item_name)
                        self.enhanced_file_manager.copy_item(item, dest_item_path)
                        print(f"✅ Sent '{item_name}' to {location_name}")
                    time.sleep(1)
                else:
                    print(f"❌ Location '{location_name}' does not exist")
                    time.sleep(1)

if __name__ == "__main__":
    app = SelectPlusApp()
    app.run()
