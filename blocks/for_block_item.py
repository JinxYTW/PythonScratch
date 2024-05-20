from PyQt6.QtWidgets import QGraphicsProxyWidget, QGraphicsView
from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtWidgets import QGraphicsScene
from blocks.design import ForBlockWidget


class ForBlockItem(QGraphicsProxyWidget):
    def __init__(self, x, y, width, height, work_area):
        super().__init__()
        self.setGeometry(QRectF(x, y, width, height))
        self.work_area = work_area
        self.for_block = ForBlockWidget()
        
         # Create a QGraphicsView
        view = QGraphicsView()

        # Désactiver les scrollbars verticales et horizontales
        view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Set the scene of the QGraphicsView to the scene
        scene = QGraphicsScene()
        scene.addItem(self.for_block)

        view.setScene(scene)
        

        # Now you can add the QGraphicsView to your main widget
        self.setWidget(view)

        # Dictionnaire pour suivre l'état de chaque point de connexion
        self.input_connection_states = {}
        self.output_connection_states = {}

        #Ajour des points de connexion
        self.for_block.add_input_connection_points()  # Ajouter les points de connexion d'entrée
        self.for_block.add_output_connection_points()  # Ajouter les points de connexion de sortie

        scene.update()
        # Passer les événements de souris aux points de connexion
        for point in self.for_block.input_connection_points:
            point.setParentItem(self)
        for point in self.for_block.output_connection_points:
            point.setParentItem(self)

        # Initialiser l'état de chaque point de connexion comme disponible (True)
        for point in self.input_connection_states:
            self.input_connection_states[point] = True
        
        for point in self.output_connection_states:
            self.output_connection_states[point] = True
            

        # Activer la réception des événements de survol
        self.setAcceptHoverEvents(True)