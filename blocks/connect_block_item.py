from PyQt6.QtWidgets import QGraphicsProxyWidget, QGraphicsView
from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtWidgets import QGraphicsScene
from blocks.connect_block_widget import ConnectBlockWidget

class ConnectBlockItem(QGraphicsProxyWidget):
    def __init__(self, x, y, width, height, work_area):
        super().__init__()
        self.setGeometry(QRectF(x, y, width, height))
        self.work_area = work_area
        self.connect_block = ConnectBlockWidget()
        
        # Create a QGraphicsView
        view = QGraphicsView()

        # Disable vertical and horizontal scrollbars
        view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Set the scene of the QGraphicsView to the scene
        scene = QGraphicsScene()
        scene.addItem(self.connect_block)

        view.setScene(scene)

        # Now you can add the QGraphicsView to your main widget
        self.setWidget(view)

        # Dictionary to track the state of each connection point
        self.input_connection_states = {}
        self.output_connection_states = {}

        # Add connection points
        self.connect_block.add_input_connection_points()  # Add input connection points
        self.connect_block.add_output_connection_points()  # Add output connection points

        scene.update()
        # Pass mouse events to connection points
        for point in self.connect_block.input_connection_points:
            point.setParentItem(self)
        for point in self.connect_block.output_connection_points:
            point.setParentItem(self)

        # Initialize the state of each connection point as available (True)
        for point in self.input_connection_states:
            self.input_connection_states[point] = True
        
        for point in self.output_connection_states:
            self.output_connection_states[point] = True

        # Enable hover events reception
        self.setAcceptHoverEvents(True)
