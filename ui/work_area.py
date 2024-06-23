from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsLineItem, QGraphicsEllipseItem
from PyQt6.QtCore import Qt, QPoint, QPointF, QMimeData
from PyQt6.QtGui import QDrag, QPen, QBrush


from models.connection_manager import ConnectionManager
from models.block_manager import BlockManager
from blocks.connection_point import ConnectionPoint
from blocks.for_block_item import ForBlockItem
from blocks.walk_block_item import WalkBlockItem
from blocks.connect_block_item import ConnectBlockItem
from blocks.dance_block_item import DanceBlockItem
from blocks.rotate_block_item import RotateBlockItem
from blocks.side_step_block_item import SideStepBlockItem
from blocks.wait_block_item import WaitBlockItem


class WorkArea(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setSceneRect(0, 0, 800, 600)
        self.installEventFilter(self)
        self.setMouseTracking(True)
        self.connection_manager = ConnectionManager()
        self.block_manager = BlockManager(self.scene, self)
        self.temp_connection_start = None  # Point de départ temporaire pour la connexion en cours
        self.temp_connection_end = None  # Point de fin temporaire pour la connexion en cours
        self.used_connection_points = set()  # Garder une trace des points de connexion utilisés

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

        

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        block_type = event.mimeData().text()
        point = event.position().toPoint()  
        pos = self.mapToScene(point)
        x, y, width, height = pos.x(), pos.y(), 100, 100
        self.block_manager.create_block(block_type, x, y, width, height)
        event.acceptProposedAction()
        self.scene.update()


    def wheelEvent(self, event):
        factor = 1.15 if event.angleDelta().y() > 0 else 1 / 1.15
        self.scale(factor, factor)

    def mousePressEvent(self, event):
        scene_pos = self.mapToScene(event.pos())
        scene_pos_int = QPoint(int(scene_pos.x()), int(scene_pos.y()))
        items = self.items(scene_pos_int)

        for item in items:
            if isinstance(item, ConnectionPoint):
                if self.temp_connection_start is None:
                    self.temp_connection_start = item
                elif id(self.temp_connection_start) != id(item):
                    self.temp_connection_end = item
                    start_block = self.temp_connection_start.parent_block
                    end_block = self.temp_connection_end.parent_block
                    if not self.connection_manager.has_connection(start_block, end_block):
                        self.create_connection(self.temp_connection_start, self.temp_connection_end)
                    self.temp_connection_start = None
                    self.temp_connection_end = None
                break
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.connection_manager.print_connections()
        super().mouseReleaseEvent(event)

    def create_connection(self, start_point, end_point):
        if not self.is_valid_connection(start_point, end_point):
            print("Connection not allowed")
            return

        start_block = start_point.parent_block
        end_block = end_point.parent_block
        
        if not self.connection_manager.has_connection(start_block, end_block):
            start_pos = start_point.scenePos()
            end_pos = end_point.scenePos()
            line = QGraphicsLineItem(start_pos.x(), start_pos.y(), end_pos.x(), end_pos.y())
            line.setPen(QPen(Qt.GlobalColor.blue, 2))
            self.scene.addItem(line)
            self.connection_manager.add_connection(start_block, end_block, start_point)
            self.used_connection_points.add(start_point)
            self.used_connection_points.add(end_point)

    def is_valid_connection(self, start_point, end_point):
        start_block = start_point.parent_block
        end_block = end_point.parent_block
        if start_block == end_block:
            return False
        if start_point in self.used_connection_points or end_point in self.used_connection_points:
            return False
        if self.connection_manager.has_connection(start_block, end_block):
            return False
        return True

    def get_widgets(self):
        blocks = []
        for item in self.scene.items():
            if isinstance(item, ForBlockItem) :
                blocks.append(item.for_block)
            elif isinstance(item, WalkBlockItem):
                blocks.append(item.walk_block)
            elif isinstance(item, ConnectBlockItem):
                blocks.append(item.connect_block)
            elif isinstance(item, DanceBlockItem):
                blocks.append(item.dance_block)
            elif isinstance(item, RotateBlockItem):
                blocks.append(item.rotate_block)
            elif isinstance(item, SideStepBlockItem):
                blocks.append(item.side_step_block)
            elif isinstance(item, WaitBlockItem):
                blocks.append(item.wait_block)
                
        return blocks

    def get_connections(self):
        return self.connection_manager.connections

    def organize_blocks_for_execution(self):
        blocks = self.get_widgets()
        print(blocks)
        connections = self.get_connections()
        print (connections)
        next_blocks = {block: {'loop_exit': [], 'body_code': []} for block in blocks}

        for start_block, end_block, connection_point in connections:
            connection_type = self.connection_manager.get_connection_type(connection_point)
            if connection_type:
                next_blocks[start_block][connection_type].append(end_block)

        first_block = None
        for block in blocks:
            has_incoming_connection = any(block == end_block for _, end_block, _ in connections)
            if not has_incoming_connection:
                first_block = block
                break

        ordered_blocks = []

        def build_ordered_blocks(block):
            body_code_blocks = next_blocks[block]['body_code']
            current_block_info = [block, []]
            for next_block in body_code_blocks:
                current_block_info[1].append(build_ordered_blocks(next_block))
            for next_block in next_blocks[block]['loop_exit']:
                ordered_blocks.append(build_ordered_blocks(next_block))
            return current_block_info

        if first_block:
            ordered_blocks.append(build_ordered_blocks(first_block))

        def print_block_info(block_info, level=0):
            indent = "    " * level
            print(f"{indent}{block_info[0]} => body_code: {len(block_info[1])} sub-blocks")
            for sub_block_info in block_info[1]:
                print_block_info(sub_block_info, level + 1)

        ordered_blocks.reverse()
        print("Ordered Blocks:")
        for block_info in ordered_blocks:
            print_block_info(block_info)


    