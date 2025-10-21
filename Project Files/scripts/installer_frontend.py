import os
import sys
import subprocess
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import json

# Localization
TRANSLATIONS = {
    'EN': {
        'title': 'SelectPlus V3.2 Installer',
        'welcome': '🎉 Welcome to SelectPlus V3.2 Setup',
        'choose_language': '🌍 Choose your language:',
        'english': '🇺🇸 English',
        'bulgarian': '🇧🇬 Български',
        'next': '➡️ Next',
        'back': '⬅️ Back',
        'install': '🚀 Install',
        'browse': '📁 Browse',
        'installation_path': '📂 Installation Directory:',
        'installing': '⚙️ Installing SelectPlus V3.2...',
        'progress_messages': [
            '📦 Downloading dependencies...',
            '🔧 Installing Python packages...',
            '📄 Copying files...',
            '🔗 Creating shortcuts...',
            '✅ Finalizing installation...'
        ],
        'success': '🎉 Installation Complete!',
        'success_message': 'SelectPlus V3.2 has been installed successfully!\n\n🖥️ Desktop shortcut created\n🎯 Ready to use!',
        'error': '❌ Error',
        'error_directory': 'Cannot create installation directory.',
        'default_path': 'C:\\Programs\\SelectPlus'
    },
    'BG': {
        'title': 'SelectPlus V3.2 Инсталатор',
        'welcome': '🎉 Добре дошли в SelectPlus V3.2 Setup',
        'choose_language': '🌍 Изберете език:',
        'english': '🇺🇸 English',
        'bulgarian': '🇧🇬 Български',
        'next': '➡️ Напред',
        'back': '⬅️ Назад',
        'install': '🚀 Инсталирай',
        'browse': '📁 Преглед',
        'installation_path': '📂 Директория за инсталация:',
        'installing': '⚙️ Инсталиране на SelectPlus V3.2...',
        'progress_messages': [
            '📦 Изтегляне на зависимости...',
            '🔧 Инсталиране на Python пакети...',
            '📄 Копиране на файлове...',
            '🔗 Създаване на пряки пътища...',
            '✅ Финализиране на инсталацията...'
        ],
        'success': '🎉 Инсталацията е завършена!',
        'success_message': 'SelectPlus V3.2 беше инсталиран успешно!\n\n🖥️ Създаден е пряк път на работния плот\n🎯 Готов за употреба!',
        'error': '❌ Грешка',
        'error_directory': 'Не може да се създаде директория за инсталация.',
        'default_path': 'C:\\Programs\\SelectPlus'
    }
}

class InstallerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SelectPlus V3.2 Installer")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Center window
        self.root.eval('tk::PlaceWindow . center')
        
        # Variables
        self.lang_var = tk.StringVar(value='EN')
        self.current_lang = 'EN'
        self.install_path = ''
        
        # Style
        self.style = ttk.Style()
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        self.style.configure('Heading.TLabel', font=('Arial', 12, 'bold'))
        
        self.draw_language_selection()
    
    def get_text(self, key):
        return TRANSLATIONS[self.current_lang].get(key, key)
    
    def draw_language_selection(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title(self.get_text('title'))
        
        # Main container
        container = ttk.Frame(self.root, padding="20")
        container.pack(expand=True, fill="both")
        
        # Welcome message
        welcome_label = ttk.Label(container, text=self.get_text('welcome'), style='Title.TLabel')
        welcome_label.pack(pady=(0, 30))
        
        # Language selection
        lang_label = ttk.Label(container, text=self.get_text('choose_language'), style='Heading.TLabel')
        lang_label.pack(pady=(0, 15))
        
        # Language buttons frame
        lang_frame = ttk.Frame(container)
        lang_frame.pack(pady=(0, 30))
        
        # English button
        en_btn = ttk.Radiobutton(lang_frame, text=self.get_text('english'), 
                                variable=self.lang_var, value='EN',
                                command=self.language_changed)
        en_btn.pack(anchor='w', pady=5)
        
        # Bulgarian button
        bg_btn = ttk.Radiobutton(lang_frame, text=self.get_text('bulgarian'), 
                                variable=self.lang_var, value='BG',
                                command=self.language_changed)
        bg_btn.pack(anchor='w', pady=5)
        
        # Next button
        next_btn = ttk.Button(container, text=self.get_text('next'), 
                             command=self.show_installation_path)
        next_btn.pack(pady=20)
    
    def language_changed(self):
        self.current_lang = self.lang_var.get()
        self.draw_language_selection()
    
    def show_installation_path(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title(self.get_text('title'))
        
        # Main container
        container = ttk.Frame(self.root, padding="20")
        container.pack(expand=True, fill="both")
        
        # Title
        title_label = ttk.Label(container, text=self.get_text('welcome'), style='Title.TLabel')
        title_label.pack(pady=(0, 30))
        
        # Path selection
        path_label = ttk.Label(container, text=self.get_text('installation_path'), style='Heading.TLabel')
        path_label.pack(pady=(0, 10))
        
        # Path frame
        path_frame = ttk.Frame(container)
        path_frame.pack(fill='x', pady=(0, 20))
        
        self.path_var = tk.StringVar(value=self.get_text('default_path'))
        path_entry = ttk.Entry(path_frame, textvariable=self.path_var, width=40)
        path_entry.pack(side='left', expand=True, fill='x')
        
        browse_btn = ttk.Button(path_frame, text=self.get_text('browse'), 
                               command=self.browse_directory)
        browse_btn.pack(side='right', padx=(10, 0))
        
        # Buttons frame
        btn_frame = ttk.Frame(container)
        btn_frame.pack(pady=20)
        
        back_btn = ttk.Button(btn_frame, text=self.get_text('back'), 
                             command=self.draw_language_selection)
        back_btn.pack(side='left', padx=(0, 10))
        
        install_btn = ttk.Button(btn_frame, text=self.get_text('install'), 
                                command=self.start_installation)
        install_btn.pack(side='right')
    
    def browse_directory(self):
        directory = filedialog.askdirectory(initialdir=self.path_var.get())
        if directory:
            self.path_var.set(directory)
    
    def start_installation(self):
        install_path = self.path_var.get()
        
        if not install_path:
            messagebox.showerror(self.get_text('error'), self.get_text('error_directory'))
            return
        
        # Create directory if it doesn't exist
        if not os.path.exists(install_path):
            try:
                os.makedirs(install_path)
            except Exception as e:
                messagebox.showerror(self.get_text('error'), self.get_text('error_directory'))
                return
        
        self.install_path = install_path
        self.show_progress()
    
    def show_progress(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title(self.get_text('installing'))
        
        # Main container
        container = ttk.Frame(self.root, padding="20")
        container.pack(expand=True, fill="both")
        
        # Installing message
        self.status_label = ttk.Label(container, text=self.get_text('installing'), style='Title.TLabel')
        self.status_label.pack(pady=(0, 30))
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(container, mode='determinate', length=400)
        self.progress_bar.pack(pady=(0, 20))
        
        # Progress message
        self.progress_label = ttk.Label(container, text=self.get_text('progress_messages')[0])
        self.progress_label.pack(pady=(0, 20))
        
        # Start installation in background
        self.start_background_installation()
    
    def start_background_installation(self):
        # Save language preference
        self.save_language_preference()
        
        # Start installation thread
        install_thread = threading.Thread(target=self.run_installation)
        install_thread.daemon = True
        install_thread.start()
        
        # Start progress animation
        self.animate_progress()
    
    def save_language_preference(self):
        """Save language preference to settings file"""
        settings = {'language': 'en' if self.current_lang == 'EN' else 'bg'}
        try:
            settings_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'selectplus_settings.json')
            with open(settings_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def run_installation(self):
        """Run the actual installation process"""
        try:
            # Run the batch file silently
            batch_file = os.path.join(os.getcwd(), "Install_SelectPlus_V3.2.bat")
            subprocess.run(["cmd.exe", "/c", batch_file], 
                         creationflags=subprocess.CREATE_NO_WINDOW)
        except Exception as e:
            print(f"Installation error: {e}")
    
    def animate_progress(self):
        """Animate the progress bar and messages"""
        messages = self.get_text('progress_messages')
        total_duration = 10000  # 10 seconds
        steps = len(messages)
        step_duration = total_duration // steps
        
        for i, message in enumerate(messages):
            progress = (i + 1) * (100 // steps)
            
            # Update progress bar and message
            self.root.after(i * step_duration, lambda p=progress, m=message: self.update_progress(p, m))
        
        # Show completion
        self.root.after(total_duration, self.show_completion)
    
    def update_progress(self, progress, message):
        """Update progress bar and message"""
        self.progress_bar['value'] = progress
        self.progress_label.config(text=message)
    
    def show_completion(self):
        """Show installation completion"""
        self.progress_bar['value'] = 100
        self.progress_label.config(text=self.get_text('progress_messages')[-1])
        
        # Wait a moment then show success message
        self.root.after(1000, self.show_success)
    
    def show_success(self):
        """Show success message and close installer"""
        messagebox.showinfo(self.get_text('success'), self.get_text('success_message'))
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = InstallerApp(root)
    root.mainloop()

