class WorkAreaFunction:
    def __init__(self,work_area):
        
        self.work_area = work_area

    
    
    def execute_program(self):
        work_area = self.work_area
        blocks = work_area.get_widgets()
        print(f"Nombre de blocs dans la zone de travail : {len(blocks)}")
        connections = work_area.get_connections()
        print(f"Nombre de connexions dans la zone de travail : {len(connections)}")

    def organize_blocks_and_execute(self):
        work_area = self.work_area
        work_area.organize_blocks_for_execution()

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