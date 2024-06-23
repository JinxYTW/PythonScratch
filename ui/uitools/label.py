import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel

class Label(QWidget):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Simple Text Box')
        self.setMinimumSize(150, 10)

        # Create a QLabel instance
        self.label = QLabel(self.text, self)
