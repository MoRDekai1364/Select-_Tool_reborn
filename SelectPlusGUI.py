import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
import subprocess

class SelectPlusGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('SelectPlus V3.2')
        self.setGeometry(100, 100, 800, 600)
        
        layout = QVBoxLayout()
        
        self.label = QLabel('SelectPlus V3.2 - Enhanced File Manager', self)
        layout.addWidget(self.label)

        self.start_button = QPushButton('Start SelectPlus', self)
        self.start_button.clicked.connect(self.start_selectplus)
        layout.addWidget(self.start_button)

        self.close_button = QPushButton('Close', self)
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)
    
    def start_selectplus(self):
        # Run the batch file to start SelectPlus
        try:
            subprocess.run(['cmd.exe', '/c', 'D:\Apps\SelectPlus_V3\Project Files\scripts\SelectPlus_V3.2.bat'], check=True)
            QMessageBox.information(self, 'Success', 'SelectPlus has started successfully!')
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SelectPlusGUI()
    ex.show()
    sys.exit(app.exec())

