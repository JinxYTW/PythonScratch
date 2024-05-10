from PyQt6.QtWidgets import QApplication, QMainWindow,QGridLayout, QPushButton, QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QGraphicsScene, QGraphicsView, QGraphicsProxyWidget,QGraphicsEllipseItem, QGraphicsLineItem,QFrame
from PyQt6.QtCore import Qt, QMimeData, QRectF, QPoint
from PyQt6.QtGui import QDrag, QCursor, QIcon,QPen

from design import ForBlockWidget, WhileBlockWidget,ConnectionPoint




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
    
        
class WhileBlockItem(QGraphicsProxyWidget):
    def __init__(self, x, y, width, height, work_area):
        super().__init__()
        self.setGeometry(QRectF(x, y, width, height))
        self.work_area = work_area
        self.while_block = WhileBlockWidget()
        
         # Create a QGraphicsView
        view = QGraphicsView()

        # Set the scene of the QGraphicsView to the scene
        scene = QGraphicsScene()
        scene.addItem(self.while_block)
        view.setScene(scene)

        # Now you can add the QGraphicsView to your main widget
        self.setWidget(view)
        


#Initialisation de la class BlockList
class BlockList(QListWidget):
    """
    A custom QListWidget subclass that allows dragging items.
    """

    def __init__(self, parent=None):
        """
        Initializes the BlockList.

        Args:
            parent: The parent widget (default: None).
        """
        super().__init__(parent)
         # Créer la WorkArea
        self.work_area = WorkArea()
        
        
        
        
        self.setDragEnabled(True)
          # Create the layout
        self.layout = QVBoxLayout()
        

        # Set the spacing between items in the layout
        self.layout.setSpacing(0)  # No spacing between item
        # Add the block list to the layout
        self.setLayout(self.layout)

        # Set a stretch to push buttons and separator to the bottom
        self.layout.addStretch(1)

        # Create the buttons
        button1 = QPushButton('Clear')
        button2 = QPushButton('Launch')
        button3 = QPushButton('Save')
        button1.clicked.connect(self.clear)
        button2.clicked.connect(self.launch)

        # Create the separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)

        # Add the separator to the layout
        self.layout.addWidget(separator)

        # Add the buttons to the layout
        self.layout.addWidget(button1)
        self.layout.addWidget(button2)
        self.layout.addWidget(button3)

        

    def clear(self):
        print("Le bouton 'Clear' a été cliqué!")

        

    def launch(self):
       

        print("Le bouton 'Launch' a été cliqué!")

    def save(self):
            print("Le bouton 'Save' a été cliqué!")

        

        

        

        
        
        

    def startDrag(self, event):
        """
        Starts the drag operation.

        Args:
            actions: The drag actions.

        Returns:
            None
        """
        block_type = self.currentItem().text()
        mouse_position = QCursor.pos()

        
        
        

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(block_type)
        drag.setMimeData(mime_data)
        drag.exec()

class ConnectionManager:
    def __init__(self):
        self.connections = []
        self.connection_types = {}  # Dictionnaire pour stocker les types de connexion

    def add_connection(self, start_block, end_block, connection_point):
        """
        Add a connection between two blocks with a specific connection point.

        Args:
            start_block: The block where the connection starts.
            end_block: The block where the connection ends.
            connection_point: The point of connection (tuple of coordinates).
        """
        # Vérifier si une connexion entre les mêmes blocs avec le même type de connexion existe déjà
        existing_connection = self.get_existing_connection(start_block, end_block)
        if existing_connection:
            # Si une connexion existe déjà, ne pas ajouter une nouvelle connexion
            print(f"Connection already exists between {start_block} and {end_block} with type {existing_connection[2]}")
            return

        # Ajouter la nouvelle connexion
        self.connections.append((start_block, end_block, connection_point))
        
        # Déterminer le type de connexion à partir du point de connexion
        connection_type = self.get_connection_type(connection_point)
        if connection_type:
            # Convertir le QPointF en tuple (x, y) pour l'utiliser comme clé hashable
            connection_point_tuple = (connection_point.x(), connection_point.y())
            # Ajouter le type de connexion au dictionnaire de types de connexion
            self.connection_types[(start_block, connection_point_tuple)] = connection_type

    def get_existing_connection(self, start_block, end_block):
        """
        Get an existing connection between two blocks.

        Args:
            start_block: The block where the connection starts.
            end_block: The block where the connection ends.

        Returns:
            The existing connection if found (start_block, end_block, connection_point), None otherwise.
        """
        for connection in self.connections:
            if connection[0] == start_block and connection[1] == end_block:
                return connection
        return None


    def remove_connection(self, start_block, end_block, connection_point):
        """
        Remove a connection between two blocks with a specific connection point.

        Args:
            start_block: The block where the connection starts.
            end_block: The block where the connection ends.
            connection_point: The point of connection (tuple of coordinates).
        """
        connection_tuple = (start_block, end_block, connection_point)
        if connection_tuple in self.connections:
            self.connections.remove(connection_tuple)
            if (start_block, connection_point) in self.connection_types:
                del self.connection_types[(start_block, connection_point)]

    def has_connection(self, start_block, end_block):
        """
        Check if there is a connection between two blocks.

        Args:
            start_block: The block where the connection starts.
            end_block: The block where the connection ends.

        Returns:
            True if there is a connection, False otherwise.
        """
        return (start_block, end_block) in self.connections

    def get_connection_type(self, connection_point):
        """
        Determine the type of connection (input or output) based on the position of the connection point.

        Args:
            connection_point: The QPointF object representing the connection point.

        Returns:
            The connection type ('input' or 'output').
        """
        x = connection_point.x()
        y = connection_point.y()

        # Determine the connection type based on the y-coordinate of the connection point
        if x == 180 and y == 25:
            return 'body_code'  # This corresponds to the 'body_code' connection point
        elif x == 180 and y == 75:
            return 'loop_exit'  # This corresponds to the 'loop_exit' connection point
        else:
            return None  # Unknown connection type

    def print_connections(self):
        """
        Print all existing connections in the work area.
        """
        for connection in self.connections:
            start_block, end_block, connection_point = connection
            print(f"Connection from {start_block} to {end_block} at {connection_point} ({self.get_connection_type(connection_point)})")
    

class WorkArea(QGraphicsView):
    """
    A custom QListView subclass that allows dropping items.

    Inherits from QGraphicsView.
    """

    def __init__(self, parent=None):
        """
        Initializes the WorkArea.

        Args:
            parent: The parent widget (default: None).
        """
        super().__init__(parent)
        
        self.setAcceptDrops(True)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setSceneRect(0, 0, 800, 600)  # Définir la taille de la scène
        self.installEventFilter(self)  # Installer un filtre d'événement sur l'objet lui-même
        self.setMouseTracking(True)  # Activer le suivi de la souris même sans clic
        self.last_y = 0
        self.connection_manager = ConnectionManager()
        self.temp_connection_start = None  # Point de départ temporaire pour la connexion en cours
        self.temp_connection_end = None  # Point de fin temporaire pour la connexion en cours
        self.used_connection_points = set()  # Garder une trace des points de connexion utilisés

    def dragEnterEvent(self, event):
        """
        Event handler for drag enter event.

        Accepts the proposed action if the event's mime data has text.
        """
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):  
        """
        Event handler for drag move event.

        Accepts the event.
        """
        event.accept()
    
    def dropEvent(self, event):
        """
        Event handler for drop event.

        Args:
            event: The drop event.
        """
        block_type = event.mimeData().text()

        
        point = event.position().toPoint()
        

    
        pos = self.mapToScene(point)
        

        x, y, width, height = pos.x(), pos.y(), 100, 100  
        

        work_area = self  # Pass a reference to the work area

        if block_type == "For":
            
            block = ForBlockItem(x, y, width, height, work_area)
            block.setZValue(0)
            
            
            self.scene.addItem(block)  # Add the block to the scene

            
                        
            
             # Ajouter les points de connexion de block à la scène
            for input_point in block.for_block.input_connection_points:
                input_point.setZValue(2) 
                
                

                
                
            for output_point in block.for_block.output_connection_points:
                output_point.setZValue(2) 
                

                
                

        # Add conditions for other block types here
        elif block_type == "While":
            block = WhileBlockItem(x, y, width, height, work_area)
            self.scene.addItem(block)
        

        block.setPos(pos.x() - width / 2, pos.y() - height / 2)
        event.acceptProposedAction()
        self.scene.update()
        


    def mouseDoubleClickEvent(self, event):
        """
        Event handler for mouse double click event.

        Removes the item at the clicked position from the scene.

        Args:
            event: The mouse double click event.
        """
        # Get the item at the clicked position
        item = self.itemAt(event.pos())
        if item:
            # If there is an item at the clicked position, remove it from the scene
            self.scene.removeItem(item)
            del item  # Optional: delete the item to free memory

    def wheelEvent(self, event):
        """
        Event handler for wheel event.

        Zooms in or out when the wheel is turned.

        Args:
            event: The wheel event.
        """
        factor = 1.15 if event.angleDelta().y() > 0 else 1 / 1.15
        self.scale(factor, factor)
    
    def mousePressEvent(self, event):
        # Récupérer la position de la souris dans la scène
        scene_pos = self.mapToScene(event.pos())

        # Convertir les coordonnées QPointF en coordonnées entières
        scene_pos_int = QPoint(int(scene_pos.x()), int(scene_pos.y()))

        # Récupérer les éléments de la scène à la position donnée
        items = self.items(scene_pos_int)

        # Vérifier si le clic est sur un point de connexion
        for item in items:
            if isinstance(item, QGraphicsEllipseItem) and getattr(item, 'isConnectionPoint', True):

                if self.temp_connection_start is None:
                    # Premier point de connexion sélectionné
                    self.temp_connection_start = item

                elif id(self.temp_connection_start) != id(item) and self.temp_connection_start.pos() != item.pos():
                    # Deuxième point de connexion sélectionné (différent du premier)
                    self.temp_connection_end = item

                    # Vérifier s'il existe déjà une connexion entre ces deux blocs
                    start_block = self.temp_connection_start.parent_block
                    end_block = self.temp_connection_end.parent_block

                    if not self.connection_manager.has_connection(start_block, end_block):
                        # Créer la connexion entre les deux blocs
                        self.create_connection(self.temp_connection_start, self.temp_connection_end)
                    else:
                        print("Connection already exists")

                    # Réinitialiser les points de connexion temporaires
                    self.temp_connection_start = None
                    self.temp_connection_end = None

                break  # Sortir de la boucle après traitement

        else:
            super().mousePressEvent(event)





    def mouseReleaseEvent(self, event):
        print("Mouse release event")

        # Imprimer les connexions existantes
        self.connection_manager.print_connections()
        
        

        super().mouseReleaseEvent(event)





    def create_connection(self, start_point, end_point):
        """
        Create a connection between two connection points.

        Args:
            start_point: The starting connection point.
            end_point: The ending connection point.
        """
        # Vérifier si les points de connexion sont valides
        if not self.is_valid_connection(start_point, end_point):
            print("Connection not allowed - One or both connection points are already used")
            return

        # Ajouter la connexion dans le gestionnaire de connexions
        start_block = start_point.parent_block
        end_block = end_point.parent_block
        if not self.connection_manager.has_connection(start_block, end_block):
            # Créer la ligne de connexion dans la scène
            start_pos = start_point.scenePos()
            end_pos = end_point.scenePos()
            line = QGraphicsLineItem(start_pos.x(), start_pos.y(), end_pos.x(), end_pos.y())
            line.setPen(QPen(Qt.GlobalColor.blue, 2))
            self.scene.addItem(line)

            # Ajouter la connexion dans le gestionnaire de connexions
            self.connection_manager.add_connection(start_block, end_block, start_point)

            # Marquer les points de connexion comme utilisés
            self.used_connection_points.add(start_point)
            self.used_connection_points.add(end_point)
        else:
            print("Connection already exists")

    def is_valid_connection(self, start_point, end_point):
        """
        Check if the connection between two connection points is valid.

        Args:
            start_point: The starting connection point.
            end_point: The ending connection point.

        Returns:
            True if the connection is valid, False otherwise.
        """
        start_block = start_point.parent_block
        end_block = end_point.parent_block

        # Vérifier si les blocs sont différents
        if start_block == end_block:
            return False

        # Vérifier si les points de connexion sont déjà utilisés
        if start_point in self.used_connection_points or end_point in self.used_connection_points:
            return False

        # Vérifier si une connexion entre ces blocs existe déjà dans le gestionnaire de connexions
        if self.connection_manager.has_connection(start_block, end_block):
            return False

        return True

    
    def get_blocks(self):
        blocks = []
        for item in self.scene.items():
            if isinstance(item, ForBlockItem) or isinstance(item, WhileBlockItem):
                blocks.append(item)
        return blocks
    
    def get_connections(self):
        return self.connection_manager.connections
    
    def organize_blocks_for_execution(self):
        blocks = self.get_blocks()
        connections = self.get_connections()

        # Initialiser les listes de blocs sans entrée et sans sortie
        blocks_without_input = []
        blocks_without_output = []

        # Parcourir tous les blocs pour identifier ceux sans entrée et sans sortie
        for block in blocks:
            has_input = False
            has_output = False
            
            # Vérifier les connexions entrantes et sortantes pour chaque bloc
            for connection in connections:
                start_block, end_block, connection_point = connection
                if end_block == block:
                    has_input = True
                if start_block == block:
                    has_output = True
            
            # Ajouter le bloc à la liste correspondante
            if not has_input:
                blocks_without_input.append(block)
            if not has_output:
                blocks_without_output.append(block)

        # Identifier le premier bloc (sans entrée)
        if blocks_without_input:
            first_block = blocks_without_input[0]
            print(f"Premier bloc à exécuter : {first_block}")
        else:
            print("Aucun premier bloc identifié")

        # Identifier le dernier bloc (sans sortie)
        if blocks_without_output:
            last_block = blocks_without_output[-1]  # Utiliser le dernier bloc sans sortie
            print(f"Dernier bloc à exécuter : {last_block}")
        else:
            print("Aucun dernier bloc identifié")
    

            




    

    




class MainWindow(QMainWindow):
    """
    The main window of the application.
    """
    def on_off_clicked(self):
        print("Le bouton 'On/Off' a été cliqué!")

    def up_clicked(self):
        print("Le bouton 'Up' a été cliqué!")

    def down_clicked(self):
        print("Le bouton 'Down' a été cliqué!")
    
    def left_clicked(self):
        print("Le bouton 'Left' a été cliqué!")
    
    def right_clicked(self):
        print("Le bouton 'Right' a été cliqué!")
    
    def turn_left_clicked(self):
        print("Le bouton 'Turn Left' a été cliqué!")

    def turn_right_clicked(self):
        print("Le bouton 'Turn Right' a été cliqué!")

    def __init__(self, parent=None):
        """
        Initializes the MainWindow.

        Args:
            parent: The parent widget (default: None).
        """
        super().__init__(parent)
        
        self.setWindowTitle("Get Jinxed !")
        self.setGeometry(100, 100, 800, 600)
        self.work_area = WorkArea(self)
        self.block_list = BlockList(parent=self.work_area)
        
        

        block_names = ["Connection","For", "While","If","Else","Elif", "Walk", "Dance", "Rotate", "Side Step", "Scan", "Eye Move", "Stop", "Wait"]

        for i in range(len(block_names)):
            item = QListWidgetItem(block_names[i])
            self.block_list.addItem(item)


        button_names = ["On/Off", "Up", "Down", "Left", "Right", "Turn Left", "Turn Right"]

        button_layout = QVBoxLayout()

        for i in range(len(button_names)):
            button = QPushButton(button_names[i])
            button_layout.addWidget(button)
            
            if button_names[i] == "On/Off":
                button.clicked.connect(self.execute_program)
            elif button_names[i] == "Up":
                button.clicked.connect(self.organize_blocks_and_execute)
            elif button_names[i] == "Down":
                button.clicked.connect(self.down_clicked)
            elif button_names[i] == "Left":
                button.clicked.connect(self.left_clicked)
            elif button_names[i] == "Right":
                button.clicked.connect(self.right_clicked)
            elif button_names[i] == "Turn Left":
                button.clicked.connect(self.turn_left_clicked)
            elif button_names[i] == "Turn Right":
                button.clicked.connect(self.turn_right_clicked)
        
         # Create a QGraphicsView
        self.view = QGraphicsView()

        # Set the scene of the QGraphicsView to the scene
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)

        # Now you can add the QGraphicsView to your main widget
        self.setCentralWidget(self.view)

        # Create blocks and add them to the scene
        self.for_block = ForBlockItem(0, 0, 100, 100, None)
        self.scene.addItem(self.for_block) #A peut être retirer pour cause redondance

        self.while_block = WhileBlockItem(200, 0, 100, 100, None)
        self.scene.addItem(self.while_block)#A peut être retirer pour cause redondance
            
        

        main_layout = QGridLayout()  # Main layout
        main_layout.addWidget(self.block_list, 0, 0)  # Add the block list to the left
        main_layout.addWidget(self.work_area, 0, 1)  # Add the work area in the middle
        main_layout.addLayout(button_layout, 0, 2)  # Add the buttons to the right

        central_widget = QWidget()  # Create a central widget
        central_widget.setLayout(main_layout)  # Set the main layout on the central widget
        self.setCentralWidget(central_widget)  # Set the central widget on the window
        self.setWindowIcon(QIcon('hehehe'))  

    def widgets(self):
        return self.findChildren(QWidget)
    
    def execute_program(self):
        # Récupérer la zone de travail
        work_area = self.work_area
        
        # Récupérer tous les blocs dans la zone de travail
        blocks = work_area.get_blocks()
        print(f"Nombre de blocs dans la zone de travail : {len(blocks)}")
        
        # Récupérer toutes les connexions dans la zone de travail
        connections = work_area.get_connections()
        print(f"Nombre de connexions dans la zone de travail : {len(connections)}")

        # Maintenant tu peux utiliser ces blocs et connexions pour exécuter ton programme
        # Par exemple, tu pourrais parcourir les blocs et exécuter les instructions en fonction des connexions
        
        # Exemple d'utilisation (à adapter selon tes besoins) :
        for block in blocks:
            print(f"Bloc à la position ({block.pos().x()}, {block.pos().y()})")
            print(f"Type de bloc : {block.__class__.__name__}")
        
        for connection in connections:
            start_block, end_block, connection_point = connection
            print(f"Connexion de {start_block} à {end_block} au point {connection_point}")


    def organize_blocks_and_execute(self):
        # Récupérer la zone de travail
        work_area = self.work_area
        
        # Organiser les blocs pour l'exécution
        work_area.organize_blocks_for_execution()

        # Maintenant tu peux utiliser ces informations pour créer une liste d'exécution
        # et interpréter les actions à exécuter dans ton programme

    
        
    

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    
    window.show()
    app.exec()
