import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
import subprocess
import os

class SelectPlusGUI(QWidget):
    def __init__(self):
        super().__init__()
        # Determine the base path of the project. Assumes this script is in a subdirectory.
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        # If the script is inside the 'app' or 'Project Files' dir, the root is one level up
        if os.path.basename(self.base_path) in ['scripts', 'src', 'app']:
             self.base_path = os.path.dirname(self.base_path)
        if os.path.basename(self.base_path) == 'Project Files':
            self.base_path = os.path.dirname(self.base_path)

        self.initUI()

    def initUI(self):
        self.setWindowTitle('SelectPlus V3.3 Launcher')
        self.setGeometry(100, 100, 300, 200)
        
        layout = QVBoxLayout()
        
        self.label = QLabel('SelectPlus V3.3 - Enhanced File Manager', self)
        layout.addWidget(self.label)

        self.start_button = QPushButton('Start SelectPlus', self)
        self.start_button.clicked.connect(self.start_selectplus)
        layout.addWidget(self.start_button)

        self.close_button = QPushButton('Close', self)
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)
    
    def start_selectplus(self):
        # The main installer creates `run_SelectPlus.bat` in the root directory.
        launcher_path = os.path.join(self.base_path, 'run_SelectPlus.bat')

        if not os.path.exists(launcher_path):
            # Fallback for development structure, looking for the dev script
            launcher_path = os.path.join(self.base_path, 'Project Files', 'scripts', 'SelectPlus_V3.3.bat')

        if not os.path.exists(launcher_path):
            QMessageBox.critical(self, 'Error', f'Launcher script not found!\nExpected at: {os.path.join(self.base_path, "run_SelectPlus.bat")}\n\nPlease run install.bat from the root directory first.')
            return

        try:
            # Use Popen to start the batch file in a new console window.
            # The 'start' command in cmd is used for this purpose.
            # We also set the working directory to the base path.
            subprocess.Popen(f'start "SelectPlus" "{launcher_path}"', shell=True, cwd=self.base_path)
            # Close the launcher GUI after successfully starting the app.
            QApplication.instance().quit()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred while trying to start SelectPlus: {e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
