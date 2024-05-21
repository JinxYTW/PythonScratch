from PyQt6.QtWidgets import QMainWindow, QGridLayout, QVBoxLayout, QWidget, QPushButton, QListWidgetItem
from PyQt6.QtGui import QDrag, QCursor, QIcon,QPen
from PyQt6.QtCore import Qt
from ui.work_area import WorkArea
from ui.block_list import BlockList
from blocks.for_block_item import ForBlockItem

from functions.blocklist_function import BlocklistFunction
from functions.work_area_function import WorkAreaFunction


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Get Jinxed !")
        self.setGeometry(100, 100, 800, 600)
        self.work_area = WorkArea(self)

        self.work_area_function = WorkAreaFunction(self.work_area)
        
        self.blocklist_function = BlocklistFunction(self.work_area)
        self.block_list = BlockList(self.blocklist_function, parent=self.work_area)

        block_names = ["Connection", "For", "While", "If", "Else", "Elif", "Walk", "Dance", "Rotate", "Side Step", "Scan", "Eye Move", "Stop", "Wait"]

        for name in block_names:
            item = QListWidgetItem(name)
            self.block_list.addItem(item)

        button_names = ["On/Off", "Up", "Down", "Left", "Right", "Turn Left", "Turn Right"]
        button_layout = QVBoxLayout()

        for name in button_names:
            button = QPushButton(name)
            button_layout.addWidget(button)
            if name == "On/Off":
                button.clicked.connect(self.work_area_function.on_off_clicked)
            elif name == "Up":
                button.clicked.connect(self.work_area_function.down_clicked)
            elif name == "Down":
                button.clicked.connect(self.work_area_function.down_clicked)
            elif name == "Left":
                button.clicked.connect(self.work_area_function.left_clicked)
            elif name == "Right":
                button.clicked.connect(self.work_area_function.right_clicked)
            elif name == "Turn Left":
                button.clicked.connect(self.work_area_function.turn_left_clicked)
            elif name == "Turn Right":
                button.clicked.connect(self.work_area_function.turn_right_clicked)

        main_layout = QGridLayout()
        main_layout.addWidget(self.block_list, 0, 0)
        main_layout.addWidget(self.work_area, 0, 1)
        main_layout.addLayout(button_layout, 0, 2)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self.setWindowIcon(QIcon('hehehe'))

    

    

    