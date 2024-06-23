from blocks.for_block_item import ForBlockItem
from blocks.walk_block_item import WalkBlockItem
from blocks.connect_block_item import ConnectBlockItem
from blocks.dance_block_item import DanceBlockItem
from blocks.rotate_block_item import RotateBlockItem
from blocks.side_step_block_item import SideStepBlockItem
from blocks.wait_block_item import WaitBlockItem


class BlockManager:
    def __init__(self, scene, work_area):
        self.scene = scene
        self.work_area = work_area
        self.block_types = {
            "For": ForBlockManager,
            "Walk": WalkBlockManager,
            "Connection": ConnectBlockManager,
            "Dance": DanceBlockManager,
            "Rotate": RotateBlockManager,
            "SideStep": SideStepBlockManager,
            "Wait": WaitBlockManager
            # Ajoutez ici d'autres types de blocs avec leurs gestionnaires respectifs
        }

    def create_block(self, block_type, x, y, width, height):
        if block_type in self.block_types:
            manager_class = self.block_types[block_type]
            manager = manager_class(self.scene, self.work_area)
            manager.create_block(x, y, width, height)


class ForBlockManager:
    def __init__(self, scene, work_area):
        self.scene = scene
        self.work_area = work_area

    def create_block(self, x, y, width, height):
        block = ForBlockItem(x, y, width, height, self.work_area)
        block.setZValue(0)
        self.scene.addItem(block)

        # Ajouter les points de connexion de block à la scène
        for input_point in block.for_block.input_connection_points:
            input_point.setZValue(2) 

        for output_point in block.for_block.output_connection_points:
            output_point.setZValue(2)

        block.setPos(x - width / 2, y - height / 2)

class WalkBlockManager:
    def __init__(self, scene, work_area):
        self.scene = scene
        self.work_area = work_area

    def create_block(self, x, y, width, height):
        block = WalkBlockItem(x, y, width, height, self.work_area)
        block.setZValue(0)
        self.scene.addItem(block)

        # Add block's connection points to the scene
        for input_point in block.walk_block.input_connection_points:
            input_point.setZValue(2) 

        for output_point in block.walk_block.output_connection_points:
            output_point.setZValue(2)

        block.setPos(x - width / 2, y - height / 2)

class ConnectBlockManager:
    def __init__(self, scene, work_area):
        self.scene = scene
        self.work_area = work_area

    def create_block(self, x, y, width, height):
        block = ConnectBlockItem(x, y, width, height, self.work_area)
        block.setZValue(0)
        self.scene.addItem(block)
        print("Connect block added to scene")

        # Add block's connection points to the scene
        for input_point in block.connect_block.input_connection_points:
            input_point.setZValue(2) 

        for output_point in block.connect_block.output_connection_points:
            output_point.setZValue(2)

        block.setPos(x - width / 2, y - height / 2)

class DanceBlockManager:
    def __init__(self, scene, work_area):
        self.scene = scene
        self.work_area = work_area

    def create_block(self, x, y, width, height):
        block = DanceBlockItem(x, y, width, height, self.work_area)
        block.setZValue(0)
        self.scene.addItem(block)

        for input_point in block.dance_block.input_connection_points:
            input_point.setZValue(2) 

        for output_point in block.dance_block.output_connection_points:
            output_point.setZValue(2)

        block.setPos(x - width / 2, y - height / 2)

class RotateBlockManager:
    def __init__(self, scene, work_area):
        self.scene = scene
        self.work_area = work_area

    def create_block(self, x, y, width, height):
        block = RotateBlockItem(x, y, width, height, self.work_area)
        block.setZValue(0)
        self.scene.addItem(block)

        for input_point in block.rotate_block.input_connection_points:
            input_point.setZValue(2) 

        for output_point in block.rotate_block.output_connection_points:
            output_point.setZValue(2)

        block.setPos(x - width / 2, y - height / 2)

class SideStepBlockManager:
    def __init__(self, scene, work_area):
        self.scene = scene
        self.work_area = work_area

    def create_block(self, x, y, width, height):
        block = SideStepBlockItem(x, y, width, height, self.work_area)
        block.setZValue(0)
        self.scene.addItem(block)

        for input_point in block.side_step_block.input_connection_points:
            input_point.setZValue(2) 

        for output_point in block.side_step_block.output_connection_points:
            output_point.setZValue(2)

        block.setPos(x - width / 2, y - height / 2)
class WaitBlockManager:
    def __init__(self, scene, work_area):
        self.scene = scene
        self.work_area = work_area

    def create_block(self, x, y, width, height):
        block = WaitBlockItem(x, y, width, height, self.work_area)
        block.setZValue(0)
        self.scene.addItem(block)

        for input_point in block.wait_block.input_connection_points:
            input_point.setZValue(2) 

        for output_point in block.wait_block.output_connection_points:
            output_point.setZValue(2)

        block.setPos(x - width / 2, y - height / 2)









