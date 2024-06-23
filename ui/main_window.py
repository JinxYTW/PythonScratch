from PyQt6.QtWidgets import QMainWindow, QGridLayout, QVBoxLayout, QWidget, QPushButton, QListWidgetItem, QProgressBar
from PyQt6.QtGui import QDrag, QCursor, QIcon,QPen
from PyQt6.QtCore import Qt ,QTimer
from ui.work_area import WorkArea
from ui.block_list import BlockList
from blocks.for_block_item import ForBlockItem

import random

from functions.blocklist_function import BlocklistFunction
from functions.work_area_function import WorkAreaFunction
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QProgressBar
from PyQt6.QtCore import QTimer
from ui.uitools.indic import RectWidget
from ui.uitools.label import Label
from ui.uitools.batteryToHexColor import intToHexColor

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Get Jinxed !")
        self.setGeometry(100, 100, 800, 600)
        self.work_area = WorkArea(self)

        self.timer = QTimer(self)

        self.work_area_function = WorkAreaFunction(self.work_area)
        self.blocklist_function = BlocklistFunction(self.work_area)
        self.block_list = BlockList(self.blocklist_function, parent=self.work_area)

        block_names = ["Connection", "For",  "Walk", "Dance", "Rotate", "SideStep",  "Wait","Auto"]

        for name in block_names:
            item = QListWidgetItem(name)
            self.block_list.addItem(item)

        button_names = ["On/Off", "Up", "Down", "Left", "Right", "Turn Left", "Turn Right","Auto"]
        button_layout = QVBoxLayout()

        for name in button_names:
            button = QPushButton(name)
            button_layout.addWidget(button)
            if name == "On/Off":
                button.clicked.connect(self.work_area_function.on_off_clicked)
            elif name == "Up":
                button.clicked.connect(self.work_area_function.up_clicked)
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
            elif name == "Auto":
                button.clicked.connect(self.work_area_function.auto_clicked)
    


        dashboard_names = ["Connection","Battery"]
        dashboard_layout = QVBoxLayout()

        for name in dashboard_names :
            if name == "Connection":
                dashboardslabel = Label(name)
                dashboard_layout.addWidget(dashboardslabel)
                if self.work_area_function.is_connected:
                    self.indic_connect = RectWidget("#00FF00")

                else:
                    self.indic_connect = RectWidget("#FF0000")

                dashboard_layout.addWidget(self.indic_connect)

                self.timer.timeout.connect(self.update_connection_status)
                self.timer.start(1000)
            elif name =="Battery":
                dashboardslabel = Label(name)
                dashboard_layout.addWidget(dashboardslabel)

                self.battery_indicator = QProgressBar(self)
                dashboard_layout.addWidget(self.battery_indicator)

        # Créer un minuteur pour mettre à jour l'indicateur de batterie périodiquement
                
                self.timer.timeout.connect(self.update_battery_level)
                self.timer.start(1000)
            else:
                dashboardslabel = Label(name)
                dashboard_layout.addWidget(dashboardslabel)
                indic = RectWidget("#000000")
                dashboard_layout.addWidget(indic)


            
        inter_layout= QGridLayout()

        main_layout = QGridLayout()
        main_layout.addWidget(self.block_list, 0, 0)
        main_layout.addWidget(self.work_area, 0, 1)
        main_layout.addLayout(button_layout, 0, 2)
        main_layout.addLayout(inter_layout, 0, 3)
        main_layout.addLayout(dashboard_layout, 0 , 4)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self.setWindowIcon(QIcon('hehehe'))




    def update_battery_level(self):
        try:
            battery_level = self.work_area_function.marty.get_battery()
        except:
            battery_level = 0
        # Mettre à jour l'indicateur de batterie (barre de progression)
        self.battery_indicator.setValue(battery_level)

    def update_connection_status(self):
        try:
            if(self.work_area_function.is_connected):
                self.indic_connect.changeColour("#00FF00")
            else:
                self.indic_connect.changeColour("#FF0000")
        except:
            self.indic_connect.changeColour("#FF0000")