from PyQt6.QtWidgets import QGraphicsProxyWidget, QGraphicsView
from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtWidgets import QGraphicsScene
from blocks.rotate_block_widget import RotateBlockWidget

class RotateBlockItem(QGraphicsProxyWidget):
    def __init__(self, x, y, width, height, work_area):
        super().__init__()
        self.setGeometry(QRectF(x, y, width, height))
        self.work_area = work_area
        self.rotate_block = RotateBlockWidget()
        
        view = QGraphicsView()
        view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        scene = QGraphicsScene()
        scene.addItem(self.rotate_block)
        view.setScene(scene)

        self.setWidget(view)

        self.input_connection_states = {}
        self.output_connection_states = {}

        self.rotate_block.add_input_connection_points()
        self.rotate_block.add_output_connection_points()

        scene.update()

        for point in self.rotate_block.input_connection_points:
            point.setParentItem(self)
        for point in self.rotate_block.output_connection_points:
            point.setParentItem(self)

        for point in self.input_connection_states:
            self.input_connection_states[point] = True
        for point in self.output_connection_states:
            self.output_connection_states[point] = True
            
        self.setAcceptHoverEvents(True)
