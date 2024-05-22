from PyQt6.QtWidgets import  QLabel, QLineEdit,QGraphicsWidget, QGraphicsProxyWidget, QGraphicsLinearLayout,QGraphicsGridLayout
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsEllipseItem

from blocks.connection_point import ConnectionPoint

class WalkBlockWidget(QGraphicsWidget):
    def __init__(self):
        super().__init__()

        # Create a layout for organizing the internal widgets
        layout = QGraphicsGridLayout()
        self.setLayout(layout)
        self.input_connection_points = []
        self.output_connection_points = []

        # Ajouter des étiquettes et des zones d'édition pour la distance
        distance_label = QLabel("WALK:")
        distance_label.setStyleSheet(
            "font-size: 8px; color: ; border: none; padding-right: 5px; background-color: transparent;"
        )
        
        distance_label_proxy = QGraphicsProxyWidget()
        distance_label_proxy.setWidget(distance_label)

        # Add widgets for editing parameters
        self.distance_edit = QLineEdit("10")
        self.distance_edit.setFixedWidth(30)

        distance_edit_proxy = QGraphicsProxyWidget()
        distance_edit_proxy.setWidget(self.distance_edit)

        layout.addItem(distance_label_proxy, 0, 0)
        layout.addItem(distance_edit_proxy, 0, 1)

        # Adjust spacing and margins
        layout.setHorizontalSpacing(10)  # Set horizontal spacing between columns
        layout.setVerticalSpacing(5)  # Set vertical spacing between rows
        layout.setContentsMargins(10, 10, 10, 10)  # Set margins around the layout

        # Set the minimum size of the block
        layout.setMinimumSize(200, 100)

    def add_input_connection_points(self):
        input_point = ConnectionPoint(self)
        input_point.setPos(20, 50)
        input_point.setRect(-5, -5, 10, 10)
        self.input_connection_points.append(input_point)

        self.scene().addItem(input_point)

    def add_output_connection_points(self):
        output_point1 = ConnectionPoint(self)
        output_point1.setPos(180, 25)
        output_point1.setRect(-5, -5, 10, 10)

        output_point2 = ConnectionPoint(self)
        output_point2.setPos(180, 75)
        output_point2.setRect(-5, -5, 10, 10)

        self.output_connection_points.extend([output_point1, output_point2])
        for point in [output_point1, output_point2]:
            self.scene().addItem(point)

    def paint(self, painter, option, widget):
        if not self.input_connection_points:
            self.add_input_connection_points()
        if not self.output_connection_points:
            self.add_output_connection_points()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        super().paint(painter, option, widget)

        painter.setBrush(Qt.GlobalColor.black)
        for ellipse in self.input_connection_points:
            painter.drawEllipse(ellipse.rect())

        painter.setBrush(Qt.GlobalColor.red)
        painter.drawEllipse(self.output_connection_points[0].rect())
        # Hide the second output connection point (body_code)
        # You can choose to not draw it, or simply not add it to the scene

    def get_distance(self):
        return int(self.distance_edit.text())