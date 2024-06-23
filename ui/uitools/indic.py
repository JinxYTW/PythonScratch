import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt


class RectWidget(QWidget):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.initUI()

    def initUI(self):
        self.setMinimumSize(70, 70)

    def changeColour(self,colour):
        self.color = colour

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(self.color))
        painter.drawRect(10, 10, 70, 30)
        



