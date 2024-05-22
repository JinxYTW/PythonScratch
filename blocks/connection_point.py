from PyQt6.QtWidgets import  QLabel, QLineEdit,QGraphicsWidget, QGraphicsProxyWidget, QGraphicsLinearLayout,QGraphicsGridLayout
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsEllipseItem

class ConnectionPoint(QGraphicsEllipseItem):
    def __init__(self, parent_block, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent_block = parent_block
        self.setAcceptHoverEvents(True)
        self.isConnectionPoint = True
        self.default_color = Qt.GlobalColor.black
        self.hover_color = Qt.GlobalColor.green
        self.clicked_color = Qt.GlobalColor.red
        self.setBrush(self.default_color)
       

    def hoverEnterEvent(self, event):
        self.setBrush(self.hover_color)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setBrush(self.default_color)
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        self.setBrush(self.clicked_color)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.setBrush(self.default_color)
        super().mouseReleaseEvent(event)






class WhileBlockWidget(QGraphicsWidget):
    def __init__(self):
        super().__init__()

        # Create a layout for organizing the internal widgets
        layout = QGraphicsLinearLayout(Qt.Orientation.Vertical)
        self.setLayout(layout)

        # Add widgets for editing parameters
        condition_edit = QLineEdit("i < 10")

        condition_edit_proxy = QGraphicsProxyWidget()
        condition_edit_proxy.setWidget(condition_edit)

        layout.addItem(condition_edit_proxy)

        # Set the minimum size of the block
        layout.setMinimumSize(200, 100)

    def paint(self, painter, option, widget):
        """
        Override the paint method to draw connection points.
        """
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Get widget dimensions
        width = self.size().width()
        
        height = self.size().height()
        

        # Draw input connection points
        painter.setBrush(Qt.GlobalColor.black)
        painter.drawEllipse(int(width - 10), int(height / 4), 10, 10)
        painter.drawEllipse(int(width - 10), int(height * 3 / 4), 10, 10)

        # Draw output connection points
        painter.setBrush(Qt.GlobalColor.red)
        painter.drawEllipse(0, int(height / 2 - 5), 10, 10)

