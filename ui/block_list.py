from PyQt6.QtWidgets import QListWidget
from PyQt6.QtGui import QDrag
from PyQt6.QtCore import QMimeData
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QFrame  # Import the QFrame class
from PyQt6.QtWidgets import QVBoxLayout  # Import the QVBoxLayout class

class BlockList(QListWidget):
    def __init__(self, parent=None):
        

        super().__init__(parent)
        self.setDragEnabled(True)
        self.setAcceptDrops(False)
        self.layout = QVBoxLayout()  # Create the QVBoxLayout object
        # Set the spacing between items in the layout
        self.layout.setSpacing(0)  # No spacing between item
        # Add the block list to the layout
        self.setLayout(self.layout)

        # Set a stretch to push buttons and separator to the bottom
        self.layout.addStretch(1)

        # Create the buttons
        button1 = QPushButton('Clear')
        button2 = QPushButton('Launch')
        button3 = QPushButton('Save')

        button1.clicked.connect(self.clear)
        button2.clicked.connect(self.launch)

        # Create the separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)

        # Add the separator to the layout
        self.layout.addWidget(separator)

        # Add the buttons to the layout
        self.layout.addWidget(button1)
        self.layout.addWidget(button2)
        self.layout.addWidget(button3)

    def startDrag(self, supportedActions):
        item = self.currentItem()
        mime_data = QMimeData()
        mime_data.setText(item.text())  # Assurez-vous que les données MIME contiennent le texte du bloc
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setHotSpot(self.rect().topLeft())
        drag.exec()

    def clear(self):
        print("Le bouton 'Clear' a été cliqué!")

        

    def launch(self):
       

        print("Le bouton 'Launch' a été cliqué!")

    def save(self):
            print("Le bouton 'Save' a été cliqué!")