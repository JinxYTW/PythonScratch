from blocks.for_block_item import ForBlockItem

class BlockManager:
    def __init__(self, scene, work_area):
        self.scene = scene
        self.work_area = work_area
        self.block_types = {
            "For": ForBlockManager,
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









# Dans votre dropEvent
def dropEvent(self, event):
    block_type = event.mimeData().text()
    point = event.position().toPoint()
    pos = self.mapToScene(point)
    x, y, width, height = pos.x(), pos.y(), 100, 100  
    work_area = self  # Pass a reference to the work area

    block_manager = BlockManager(self.scene)
    block_manager.create_block(block_type, x, y, width, height)
    #block.setPos(pos.x() - width / 2, pos.y() - height / 2)
    event.acceptProposedAction()
    self.scene.update()
