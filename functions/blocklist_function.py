from ui.work_area import WorkArea

class BlocklistFunction:
    def __init__(self,work_area):
        
        self.work_area = work_area

    
    
    def execute_program(self):
        work_area = self.work_area
        blocks = work_area.get_widgets()
        print(f"Nombre de blocs dans la zone de travail : {len(blocks)}")
        connections = work_area.get_connections()
        print(f"Nombre de connexions dans la zone de travail : {len(connections)}")