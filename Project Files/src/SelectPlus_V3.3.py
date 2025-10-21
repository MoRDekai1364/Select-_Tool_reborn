# ##############################################################################
# #                                                                            #
# #                SelectPlus v3.3 - Enhanced Console File Manager             #
# #                                                                            #
# ##############################################################################

import os
import sys
import json
import time
import shutil
import atexit
import hashlib
import tempfile
import threading
import subprocess
from datetime import datetime

# --- Lazy Loading for Optional Dependencies ---
_Image = None
_AudioSegment = None

def get_pil_image():
    """Lazily imports and returns the Image class from Pillow."""
    global _Image
    if _Image is None:
        try:
            from PIL import Image
            _Image = Image
        except ImportError:
            pass # Will be handled by the functions that need it
    return _Image

def get_audio_segment():
    """Lazily imports and returns the AudioSegment class from pydub."""
    global _AudioSegment
    if _AudioSegment is None:
        try:
            from pydub import AudioSegment
            _AudioSegment = AudioSegment
        except ImportError:
            pass # Will be handled by the functions that need it
    return _AudioSegment

def configure_ffmpeg():
    """
    Locates the ffmpeg executable required for media operations and configures
    the necessary libraries to use it. This version checks the script's installation directory.
    """
    try:
        AudioSegment = get_audio_segment()
        if AudioSegment is None:
            # This is not an error, just means media features are off
            return False

        # For system-wide install, ffmpeg.exe is in the parent directory of 'src'
        # __file__ is .../SelectPlus/src/SelectPlus_V3.3.py
        # os.path.dirname(__file__) is .../SelectPlus/src
        # os.path.dirname(os.path.dirname(__file__)) is .../SelectPlus
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ffmpeg_path = os.path.join(base_path, "ffmpeg.exe")

        if os.path.exists(ffmpeg_path):
            # Explicitly tell pydub where to find ffmpeg
            AudioSegment.converter = ffmpeg_path
            return True
        else:
            # Fallback for portable dev environment
            portable_bin_path = os.path.join(os.path.dirname(base_path), "bin", "ffmpeg.exe")
            if os.path.exists(portable_bin_path):
                 AudioSegment.converter = portable_bin_path
                 return True
            return False
    except Exception:
        return False

# Version information
VERSION = "3.3"

# --- Global State & Configuration ---
class AppState:
    def __init__(self):
        self.current_directory = os.getcwd()
        self.history = [self.current_directory]
        self.history_position = 0
        self.selection = []
        self.clipboard = []
        self.clipboard_mode = None  # 'copy' or 'cut'
        self.last_find_results = []
        self.view_mode = "columns"
        self.show_hidden = False
        self.settings = self.load_settings()
        self.ffmpeg_configured = configure_ffmpeg()
        self.running = True
        self.lock = threading.Lock()
        self.background_tasks = {}

    def load_settings(self):
        """Loads settings from a JSON file."""
        try:
            # Path relative to the script's location
            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(script_dir, '..', 'config', 'selectplus_settings.json')
            with open(config_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "show_full_path": False,
                "default_sort": "name",
                "show_confirmation": True,
                "enable_media_info": True,
                "fast_dir_size": True
            }

    def get_setting(self, key, default=None):
        """Safely gets a setting value."""
        return self.settings.get(key, default)

state = AppState()

# --- Utility Functions ---

def format_size(size_bytes):
    """Formats a size in bytes to a human-readable string."""
    if size_bytes is None:
        return "N/A"
    if size_bytes < 1024:
        return f"{size_bytes} B"
    for unit in ['KB', 'MB', 'GB', 'TB']:
        size_bytes /= 1024.0
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
    return f"{size_bytes:.2f} PB"

def get_terminal_width():
    """Gets the width of the terminal."""
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80  # Default width

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Prints the application header and current path."""
    width = get_terminal_width()
    path = state.current_directory if state.get_setting("show_full_path") else os.path.basename(state.current_directory)
    if not state.get_setting("show_full_path") and state.current_directory.strip().endswith((':', ':/', ':\\')):
         path = state.current_directory # Show full path for root drives
    header_text = f" SelectPlus v{VERSION} | Path: {path} "
    
    # Ensure header doesn't exceed terminal width
    if len(header_text) > width - 2:
        max_path_len = width - (len(header_text) - len(path)) - 5
        path = "..." + path[-max_path_len:]
        header_text = f" SelectPlus v{VERSION} | Path: {path} "

    print("=" * width)
    print(header_text.center(width))
    print("=" * width)
    
    # Show selection info
    if state.selection:
        print(f"[{len(state.selection)} item(s) selected]".center(width))
    if state.clipboard:
        mode = "CUT" if state.clipboard_mode == 'cut' else "COPY"
        print(f"[{len(state.clipboard)} item(s) on clipboard ({mode})]".center(width))

def get_directory_contents(path):
    """Gets and sorts the contents of a directory."""
    try:
        all_files = os.listdir(path)
        if not state.show_hidden:
            all_files = [f for f in all_files if not f.startswith('.')]
        
        dirs = sorted([d for d in all_files if os.path.isdir(os.path.join(path, d))], key=str.lower)
        files = sorted([f for f in all_files if not os.path.isdir(os.path.join(path, f))], key=str.lower)

        return dirs, files
    except PermissionError:
        print("\n[ERROR] Permission denied.")
        return [], []
    except FileNotFoundError:
        print("\n[ERROR] Directory not found.")
        return [], []

def get_item_properties(item_path):
    """Gets properties (size, modification date) for a file or directory."""
    try:
        stat = os.stat(item_path)
        mod_time = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
        if os.path.isdir(item_path):
            if state.get_setting('fast_dir_size', True):
                return 'DIR', mod_time
            size = get_directory_size(item_path)
            return format_size(size), mod_time
        else:
            return format_size(stat.st_size), mod_time
    except (FileNotFoundError, PermissionError):
        return 'N/A', 'N/A'

def get_directory_size(path):
    """Recursively calculates the size of a directory."""
    total_size = 0
    try:
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
    except (PermissionError, FileNotFoundError):
        return None
    return total_size

# --- Display Functions ---

def display_columns():
    """Displays directory contents in a multi-column format."""
    width = get_terminal_width()
    dirs, files = get_directory_contents(state.current_directory)
    items = dirs + files

    if not items:
        print("\n< Empty Directory >".center(width))
        return

    # Calculate column layout
    max_len = max(len(item) for item in items) if items else 0
    col_width = max_len + 4  # Name + index + padding
    num_cols = max(1, width // col_width)
    num_rows = (len(items) + num_cols - 1) // num_cols

    for i in range(num_rows):
        for j in range(num_cols):
            index = i + j * num_rows
            if index < len(items):
                item = items[index]
                display_index = index + 1
                is_dir = os.path.isdir(os.path.join(state.current_directory, item))
                indicator = " [D]" if is_dir else ""
                
                # Truncate if necessary
                available_space = col_width - len(f"{display_index}. ") - len(indicator) - 1
                display_item = item if len(item) <= available_space else item[:available_space-3] + "..."

                # Highlight selected items
                prefix = "*" if item in state.selection else " "
                
                print(f"{prefix}{display_index:<3}. {display_item}{indicator}".ljust(col_width), end="")
        print() # Newline after each row

def display_list():
    """Displays directory contents in a detailed list format."""
    width = get_terminal_width()
    dirs, files = get_directory_contents(state.current_directory)
    items = dirs + files

    if not items:
        print("\n< Empty Directory >".center(width))
        return

    # Prepare data for display
    display_data = []
    max_name_len = 0
    for i, item in enumerate(items):
        item_path = os.path.join(state.current_directory, item)
        size, mod_time = get_item_properties(item_path)
        is_dir = size == 'DIR'
        
        display_data.append({
            "index": i + 1,
            "name": item,
            "size": "—" if is_dir else size,
            "type": "Folder" if is_dir else "File",
            "modified": mod_time,
            "is_dir": is_dir
        })
        if len(item) > max_name_len:
            max_name_len = len(item)
    
    # Calculate column widths
    size_col_width = max(len(d['size']) for d in display_data) if display_data else 5
    type_col_width = 7 # "Folder"
    mod_col_width = 17 # YYYY-MM-DD HH:MM
    
    # Header
    print(f"\n {'#':<4} {'Name':<{max_name_len}} {'Size':>{size_col_width}}  {'Type':<{type_col_width}}  {'Modified':<{mod_col_width}}")
    print("-" * width)

    for data in display_data:
        prefix = "*" if data['name'] in state.selection else " "
        
        # Truncate name if it's too long
        name_width_available = width - (4 + size_col_width + type_col_width + mod_col_width + 10)
        display_name = data['name']
        if len(display_name) > name_width_available:
            display_name = display_name[:name_width_available-3] + "..."

        print(f"{prefix}{data['index']:<3} {display_name:<{name_width_available}} "
              f"{data['size']:>{size_col_width}}  "
              f"{data['type']:<{type_col_width}}  "
              f"{data['modified']:<{mod_col_width}}")

def refresh_display():
    """Clears the screen and redisplays the content."""
    clear_screen()
    print_header()
    if state.view_mode == "columns":
        display_columns()
    else:
        display_list()
    print("\n" + "-" * get_terminal_width())
    print("Type 'help' for a list of commands.")

# --- File Operations ---

def change_directory(target):
    """Changes the current directory."""
    new_path = ""
    if target == "..":
        new_path = os.path.dirname(state.current_directory)
    elif target == "-":
        # Go to previous directory in history
        if len(state.history) > 1:
            state.history_position = max(0, state.history_position -1) if state.history_position > 0 else len(state.history)-2
            new_path = state.history[state.history_position]
        else:
            print("[INFO] No previous directory in history.")
            return
    elif os.path.isabs(target):
        new_path = target
    else:
        new_path = os.path.join(state.current_directory, target)

    if os.path.isdir(new_path):
        try:
            # Test if we can list the directory before changing
            os.listdir(new_path)
            state.current_directory = os.path.normpath(new_path)
            # Update history
            if state.history[-1] != state.current_directory:
                state.history.append(state.current_directory)
            state.history_position = len(state.history) - 1
            state.selection.clear()
        except PermissionError:
            print("[ERROR] Permission denied.")
    else:
        print(f"[ERROR] Directory not found: {new_path}")

def handle_selection(args):
    """Handles adding/removing items from selection."""
    dirs, files = get_directory_contents(state.current_directory)
    items = dirs + files

    if not args or args[0].lower() == 'clear':
        state.selection.clear()
        print("Selection cleared.")
        return
    if args[0].lower() == 'all':
        state.selection = list(items)
        print("All items selected.")
        return
    if args[0].lower() == 'invert':
        new_selection = [item for item in items if item not in state.selection]
        state.selection = new_selection
        print("Selection inverted.")
        return

    for arg in args:
        try:
            if '-' in arg: # Range selection
                start, end = map(int, arg.split('-'))
                for i in range(start, end + 1):
                    if 1 <= i <= len(items):
                        item = items[i-1]
                        if item not in state.selection:
                            state.selection.append(item)
            else:
                index = int(arg)
                if 1 <= index <= len(items):
                    item = items[index-1]
                    if item in state.selection:
                        state.selection.remove(item)
                    else:
                        state.selection.append(item)
        except (ValueError, IndexError):
            print(f"[ERROR] Invalid index or range: {arg}")

def confirm_action(prompt):
    """Asks for user confirmation if the setting is enabled."""
    if not state.get_setting("show_confirmation", True):
        return True
    
    response = input(f"{prompt} (y/n): ").lower()
    return response == 'y'

def delete_selected():
    """Deletes selected files and directories."""
    if not state.selection:
        print("[ERROR] No items selected to delete.")
        return

    if not confirm_action(f"Permanently delete {len(state.selection)} item(s)?"):
        print("Deletion cancelled.")
        return
    
    for item_name in state.selection:
        item_path = os.path.join(state.current_directory, item_name)
        try:
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Deleted directory: {item_name}")
            else:
                os.remove(item_path)
                print(f"Deleted file: {item_name}")
        except Exception as e:
            print(f"[ERROR] Could not delete {item_name}: {e}")
    state.selection.clear()

def create_item(item_type, name):
    """Creates a new file or directory."""
    item_path = os.path.join(state.current_directory, name)
    if os.path.exists(item_path):
        print(f"[ERROR] '{name}' already exists.")
        return

    try:
        if item_type == "dir":
            os.makedirs(item_path)
            print(f"Directory '{name}' created.")
        else: # file
            open(item_path, 'a').close()
            print(f"File '{name}' created.")
    except Exception as e:
        print(f"[ERROR] Could not create '{name}': {e}")

def rename_item(old_name_arg, new_name):
    """Renames a file or directory."""
    dirs, files = get_directory_contents(state.current_directory)
    items = dirs + files

    try:
        # Try to resolve by index first
        index = int(old_name_arg) - 1
        if not (0 <= index < len(items)):
            raise ValueError()
        old_name = items[index]
    except (ValueError, IndexError):
        # Fallback to resolving by name
        old_name = old_name_arg
        if old_name not in items:
            print(f"[ERROR] Item '{old_name}' not found.")
            return

    old_path = os.path.join(state.current_directory, old_name)
    new_path = os.path.join(state.current_directory, new_name)

    if os.path.exists(new_path):
        print(f"[ERROR] Destination '{new_name}' already exists.")
        return

    try:
        os.rename(old_path, new_path)
        print(f"Renamed '{old_name}' to '{new_name}'")
    except Exception as e:
        print(f"[ERROR] Could not rename: {e}")

def copy_paste_handler(mode):
    """Handles copy and cut operations."""
    if not state.selection:
        print(f"[ERROR] Nothing selected to {mode}.")
        return

    state.clipboard = [os.path.join(state.current_directory, item) for item in state.selection]
    state.clipboard_mode = mode
    print(f"{len(state.clipboard)} item(s) ready to be {'moved' if mode == 'cut' else 'pasted'}.")
    state.selection.clear()

def paste_handler():
    """Handles the paste operation."""
    if not state.clipboard:
        print("[ERROR] Clipboard is empty.")
        return

    destination_dir = state.current_directory
    print(f"Pasting {len(state.clipboard)} item(s) to {destination_dir}...")
    
    for source_path in state.clipboard:
        item_name = os.path.basename(source_path)
        dest_path = os.path.join(destination_dir, item_name)

        if os.path.exists(dest_path):
            print(f"[WARN] '{item_name}' already exists. Skipping.")
            continue
        
        try:
            if state.clipboard_mode == 'cut':
                shutil.move(source_path, dest_path)
                print(f"Moved: {item_name}")
            else: # copy
                if os.path.isdir(source_path):
                    shutil.copytree(source_path, dest_path)
                else:
                    shutil.copy2(source_path, dest_path)
                print(f"Copied: {item_name}")
        except Exception as e:
            print(f"[ERROR] Failed to paste '{item_name}': {e}")
    
    # Clear clipboard after cut
    if state.clipboard_mode == 'cut':
        state.clipboard.clear()
        state.clipboard_mode = None

# --- Advanced Features ---

def find_files(pattern):
    """Finds files/directories matching a pattern recursively."""
    print(f"Searching for '{pattern}' in {state.current_directory}...")
    results = []
    try:
        for root, dirs, files in os.walk(state.current_directory):
            for name in dirs + files:
                if pattern.lower() in name.lower():
                    full_path = os.path.join(root, name)
                    results.append(full_path)
    except Exception as e:
        print(f"[ERROR] Search failed: {e}")
        return

    if not results:
        print("No results found.")
    else:
        state.last_find_results = results
        print(f"Found {len(results)} result(s):")
        for i, path in enumerate(results):
            # Make path relative for cleaner display
            try:
                display_path = os.path.relpath(path, state.current_directory)
            except ValueError:
                display_path = path
            print(f"  {i+1}. {display_path}")

def get_item_info(item_arg):
    """Displays detailed information about a file or directory."""
    dirs, files = get_directory_contents(state.current_directory)
    items = dirs + files
    item_name = ""

    try:
        index = int(item_arg) - 1
        if 0 <= index < len(items):
            item_name = items[index]
        else:
            print("[ERROR] Invalid index.")
            return
    except ValueError:
        if item_arg in items:
            item_name = item_arg
        else:
            print(f"[ERROR] Item '{item_arg}' not found.")
            return

    item_path = os.path.join(state.current_directory, item_name)
    print(f"\n--- Info for: {item_name} ---")
    
    try:
        stat = os.stat(item_path)
        print(f"  Full Path: {item_path}")
        print(f"  Type: {'Directory' if os.path.isdir(item_path) else 'File'}")
        print(f"  Size: {format_size(stat.st_size)}")
        if os.path.isdir(item_path):
             size_on_disk = get_directory_size(item_path)
             print(f"  Size on Disk (recursive): {format_size(size_on_disk)}")
        
        print(f"  Created: {datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Modified: {datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Accessed: {datetime.fromtimestamp(stat.st_atime).strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Media info
        if state.ffmpeg_configured and state.get_setting("enable_media_info"):
            get_media_info(item_path)

        # Image info
        Image = get_pil_image()
        if Image and not os.path.isdir(item_path):
            try:
                with Image.open(item_path) as img:
                    print(f"  Image Info: {img.format}, {img.size[0]}x{img.size[1]}, {img.mode}")
            except Exception:
                pass # Not an image or unsupported format

    except FileNotFoundError:
        print("  [ERROR] File not found.")
    except Exception as e:
        print(f"  [ERROR] Could not get info: {e}")
    print("--------------------------")

def get_media_info(file_path):
    """Uses ffprobe (via pydub) to get media file information."""
    AudioSegment = get_audio_segment()
    if not AudioSegment: return

    try:
        info = AudioSegment.from_file(file_path).info
        duration_s = float(info.get('duration', 0))
        bit_rate_kbps = int(info.get('bit_rate', 0)) / 1000
        codec = info.get('codec_name', 'N/A')
        sample_rate = info.get('sample_rate', 'N/A')
        
        print(f"  Media Info: Codec: {codec}, Duration: {duration_s:.2f}s, Bitrate: {bit_rate_kbps:.0f} kbps")
    except Exception:
        # Fails silently if it's not a media file
        pass

def open_file(item_arg):
    """Opens a file or directory with the default system application."""
    dirs, files = get_directory_contents(state.current_directory)
    items = dirs + files

    try:
        index = int(item_arg) - 1
        if not (0 <= index < len(items)):
            raise ValueError()
        item_name = items[index]
    except ValueError:
        item_name = item_arg
        if item_name not in items:
            print(f"[ERROR] Item '{item_name}' not found.")
            return

    item_path = os.path.join(state.current_directory, item_name)
    print(f"Opening '{item_name}'...")
    try:
        os.startfile(item_path)
    except Exception as e:
        print(f"[ERROR] Could not open file: {e}")

def open_terminal():
    """Opens a new terminal in the current directory."""
    try:
        if sys.platform == "win32":
            os.system(f"start cmd.exe /K cd /d \"{state.current_directory}\"")
        elif sys.platform == "darwin":
            subprocess.run(["open", "-a", "Terminal", state.current_directory])
        else: # Linux
            # Try a few common terminals
            terminals = ["gnome-terminal", "konsole", "xfce4-terminal", "xterm"]
            for term in terminals:
                if shutil.which(term):
                    subprocess.run([term, "--working-directory", state.current_directory])
                    return
            print("[ERROR] Could not detect a known terminal emulator.")
    except Exception as e:
        print(f"[ERROR] Failed to open new terminal: {e}")

def hash_file(filepath):
    """Calculates SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error reading {os.path.basename(filepath)}: {e}")
        return None

def find_duplicates():
    """Finds duplicate files in the current directory and subdirectories based on content hash."""
    hashes = {}
    duplicates = {}
    
    print("Scanning for duplicate files... (This may take a while)")
    
    file_count = 0
    for dirpath, _, filenames in os.walk(state.current_directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.islink(file_path) or os.path.getsize(file_path) == 0:
                continue
            
            file_count += 1
            sys.stdout.write(f"\rScanned {file_count} files...")
            sys.stdout.flush()

            file_hash = hash_file(file_path)
            if file_hash:
                if file_hash in hashes:
                    if file_hash not in duplicates:
                        duplicates[file_hash] = [hashes[file_hash]]
                    duplicates[file_hash].append(file_path)
                else:
                    hashes[file_hash] = file_path

    print("\nScan complete.")
    if not duplicates:
        print("No duplicate files found.")
    else:
        print(f"Found {len(duplicates)} set(s) of duplicates:")
        for i, (hash_val, files) in enumerate(duplicates.items()):
            print(f"\n--- Set {i+1} (Size: {format_size(os.path.getsize(files[0]))}) ---")
            for f in files:
                print(f"  - {os.path.relpath(f, state.current_directory)}")

# --- Command Handling ---

def display_help():
    """Displays the help message with all available commands."""
    print("\n--- SelectPlus Help ---")
    commands = {
        "Navigation": {
            "ls": "Refresh display.",
            "cd <dir>": "Change directory. Use '..' to go up, '-' for previous.",
            "cd <index>": "Enter directory by its number.",
            "back": "Go back in history.",
            "forward": "Go forward in history."
        },
        "Selection": {
            "s <index>": "Toggle selection for an item by number.",
            "s <start-end>": "Select a range of items (e.g., 's 5-10').",
            "s all/clear/invert": "Select all, clear, or invert selection."
        },
        "File Operations": {
            "del": "Delete selected items.",
            "copy": "Copy selected items to clipboard.",
            "cut": "Cut selected items to clipboard.",
            "paste": "Paste items from clipboard here.",
            "newfile <name>": "Create a new empty file.",
            "newdir <name>": "Create a new directory.",
            "ren <index/name> <new>": "Rename an item."
        },
        "System & View": {
            "open <index/name>": "Open a file or directory.",
            "view columns/list": "Change display mode.",
            "hidden on/off": "Toggle visibility of hidden files.",
            "cmd": "Open a new terminal in this directory.",
            "exit/q": "Quit the application."
        },
        "Utilities": {
            "find <pattern>": "Find files/dirs recursively.",
            "info <index/name>": "Show detailed info for an item.",
            "dupes": "Find duplicate files in current tree.",
            "help": "Show this help message."
        }
    }
    for category, cmds in commands.items():
        print(f"\n{category}:")
        for cmd, desc in cmds.items():
            print(f"  {cmd:<20} {desc}")
    print("-" * 23)

def process_command(user_input):
    """Processes the user's command input."""
    parts = user_input.strip().split()
    if not parts:
        return

    command = parts[0].lower()
    args = parts[1:]

    # Navigation
    if command == "cd":
        if not args:
            print("[ERROR] 'cd' requires a target directory or index.")
        else:
            target = " ".join(args)
            try:
                # Try to cd by index
                index = int(target) - 1
                dirs, _ = get_directory_contents(state.current_directory)
                if 0 <= index < len(dirs):
                    change_directory(dirs[index])
                else:
                    print("[ERROR] Invalid directory index.")
            except ValueError:
                # cd by name
                change_directory(target)
    elif command in ["exit", "q"]:
        state.running = False
    elif command == "ls":
        pass # The loop will refresh automatically
    elif command == "back":
        if state.history_position > 0:
            state.history_position -= 1
            state.current_directory = state.history[state.history_position]
    elif command == "forward":
        if state.history_position < len(state.history) - 1:
            state.history_position += 1
            state.current_directory = state.history[state.history_position]

    # Selection
    elif command in ["s", "sel", "select"]:
        handle_selection(args)
    
    # File Ops
    elif command in ["del", "rm"]:
        delete_selected()
    elif command == "copy":
        copy_paste_handler('copy')
    elif command == "cut":
        copy_paste_handler('cut')
    elif command == "paste":
        paste_handler()
    elif command == "newfile":
        if not args: print("[ERROR] 'newfile' requires a name.")
        else: create_item("file", " ".join(args))
    elif command == "newdir":
        if not args: print("[ERROR] 'newdir' requires a name.")
        else: create_item("dir", " ".join(args))
    elif command == "ren":
        if len(args) < 2: print("[ERROR] 'ren' requires <old_name/index> and <new_name>.")
        else: rename_item(args[0], " ".join(args[1:]))

    # System & View
    elif command == "open":
        if not args: print("[ERROR] 'open' requires an index or name.")
        else: open_file(" ".join(args))
    elif command == "view":
        if args and args[0].lower() in ["columns", "list"]:
            state.view_mode = args[0].lower()
        else:
            print("[ERROR] Usage: view columns|list")
    elif command == "hidden":
        if args and args[0].lower() in ["on", "off"]:
            state.show_hidden = (args[0].lower() == "on")
        else:
            print("[ERROR] Usage: hidden on|off")
    elif command == "cmd":
        open_terminal()

    # Utilities
    elif command == "find":
        if not args: print("[ERROR] 'find' requires a search pattern.")
        else: find_files(" ".join(args))
    elif command == "info":
        if not args: print("[ERROR] 'info' requires an index or name.")
        else: get_item_info(" ".join(args))
    elif command == "dupes":
        find_duplicates()
    elif command == "help":
        display_help()
    
    else:
        print(f"[ERROR] Unknown command: '{command}'")
        return # Avoid full refresh for unknown command

    # After a successful command, refresh the display
    refresh_display()

# --- Main Application Loop ---

def main():
    """The main entry point and loop for the application."""
    atexit.register(lambda: print("\nExiting SelectPlus. Goodbye!"))
    
    # Initial display
    refresh_display()

    while state.running:
        try:
            prompt = f"\n{state.current_directory}> "
            user_input = input(prompt)
            if user_input:
                # Process command without full refresh, let functions handle it
                process_command(user_input)
            else:
                # Just pressing enter refreshes
                refresh_display()

        except KeyboardInterrupt:
            print("\nUse 'exit' or 'q' to quit.")
        except Exception as e:
            print(f"\n[FATAL ERROR] An unexpected error occurred: {e}")
            print("Please restart the application.")
            time.sleep(3)


if __name__ == "__main__":
    main()
