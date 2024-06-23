from PyQt6.QtWidgets import QLabel, QLineEdit, QGraphicsWidget, QGraphicsProxyWidget, QGraphicsGridLayout
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt

from blocks.connection_point import ConnectionPoint

class RotateBlockWidget(QGraphicsWidget):
    def __init__(self):
        super().__init__()

        layout = QGraphicsGridLayout()
        self.setLayout(layout)
        self.input_connection_points = []
        self.output_connection_points = []

        rotate_label = QLabel("ROTATE")
        rotate_label.setStyleSheet(
            "font-size: 10px; color: ; border: none; padding-right: 5px; background-color: transparent;"
        )

        angle_label = QLabel("Angle:")
        self.angle_edit = QLineEdit("90")
        self.angle_edit.setFixedWidth(30)

        rotate_label_proxy = QGraphicsProxyWidget()
        rotate_label_proxy.setWidget(rotate_label)

        angle_label_proxy = QGraphicsProxyWidget()
        angle_label_proxy.setWidget(angle_label)

        angle_edit_proxy = QGraphicsProxyWidget()
        angle_edit_proxy.setWidget(self.angle_edit)

        layout.addItem(rotate_label_proxy, 0, 0)
        layout.addItem(angle_label_proxy, 1, 0)
        layout.addItem(angle_edit_proxy, 1, 1)

        layout.setHorizontalSpacing(10)
        layout.setVerticalSpacing(5)
        layout.setContentsMargins(10, 10, 10, 10)

        layout.setMinimumSize(200, 50)

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

    def get_angle(self):
        return self.angle_edit.text()
