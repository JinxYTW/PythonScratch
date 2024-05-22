from PyQt6.QtWidgets import  QLabel, QLineEdit,QGraphicsWidget, QGraphicsProxyWidget, QGraphicsLinearLayout,QGraphicsGridLayout
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsEllipseItem

from blocks.connection_point import ConnectionPoint

class ForBlockWidget(QGraphicsWidget):
    def __init__(self):
        super().__init__()

        

        # Create a layout for organizing the internal widgets
        layout = QGraphicsGridLayout()
        self.setLayout(layout)
        self.input_connection_points = []
        self.output_connection_points = []

        # Ajouter des étiquettes et des zones d'édition pour la variable, index début et index fin
        variable_label = QLabel("FOR:")
        index_start_label = QLabel("Index début:")
        index_end_label = QLabel("Index fin:")

       
        variable_label.setStyleSheet(
            "font-size: 8px; color: ; border: none; padding-right: 5px; background-color: transparent;"
        )  

        
        

        variable_label_proxy = QGraphicsProxyWidget()
        variable_label_proxy.setWidget(variable_label)

       # Add widgets for editing parameters
        self.variable_edit = QLineEdit("i")  # Make this an instance attribute
        self.variable_edit.setFixedWidth(30)
        self.range_start_edit = QLineEdit("0")  # Make this an instance attribute
        self.range_start_edit.setFixedWidth(30)
        self.range_end_edit = QLineEdit("10")  # Make this an instance attribute
        self.range_end_edit.setFixedWidth(30)

        variable_edit_proxy = QGraphicsProxyWidget()
        variable_edit_proxy.setWidget(self.variable_edit)

        range_start_edit_proxy = QGraphicsProxyWidget()
        range_start_edit_proxy.setWidget(self.range_start_edit)

        range_end_edit_proxy = QGraphicsProxyWidget()
        range_end_edit_proxy.setWidget(self.range_end_edit)

        layout.addItem(variable_label_proxy,0,0)
        layout.addItem(variable_edit_proxy,0,1)
        layout.addItem(range_start_edit_proxy,1,1)
        layout.addItem(range_end_edit_proxy,2,1)

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

        self.output_connection_points.append(input_point)

        # Ajouter le point de connexion de sortie à la scène
        
        self.scene().addItem(input_point) #A peut être retirer cause redondance
            
        

    def add_output_connection_points(self):
        
        

        
        output_point1 = ConnectionPoint(self)
        output_point1.setPos(180,25)
        

        output_point1.setRect(-5, -5, 10, 10)

        output_point2 = ConnectionPoint(self)
        output_point2.setPos(180, 75)
        
        output_point2.setRect(-5, -5, 10, 10)


        self.input_connection_points.extend([output_point1, output_point2])

        # Ajouter les points de connexion à la scène
        
        for point in [output_point1, output_point2]: #A peut être retirer cause redondance
            
            self.scene().addItem(point)
        
        

    def paint(self, painter, option, widget):
        
        """
        Override the paint method to draw connection points.
        """
        if not self.input_connection_points:
            self.add_input_connection_points()
        if not self.output_connection_points:
            self.add_output_connection_points()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Call the base class paint method to draw the layout
        super().paint(painter, option, widget)

        # Draw ellipses for input connection points
        painter.setBrush(Qt.GlobalColor.black)
        for ellipse in self.input_connection_points:
            painter.drawEllipse(ellipse.rect())

        # Draw ellipse for output connection point
        painter.setBrush(Qt.GlobalColor.red)
        painter.drawEllipse(self.output_connection_points[0].rect())

    def get_variable(self):
        return self.variable_edit.text()
    
    def get_range_start(self):
        return self.range_start_edit.text()
    
    def get_range_end(self):
        return self.range_end_edit.text()

