from PyQt6.QtWidgets import QGraphicsWidget
from functions.marty_function import MartyFunction

class ForBlock:
    def __init__(self, var, range_start, range_end, body_block):
        self.var = var
        self.range_start = range_start
        self.range_end = range_end
        self.body_block = body_block
        self.inputs = None  # Liste pour stocker les blocs connectés en entrée
        self.output = None  # Bloc connecté en sortie
    
    def add_input(self, block):
        self.inputs = block
    
    def set_output(self, block):
        self.output = block
    
    def to_python_code(self):
        body_code = ""
        for block in self.body_block:
            body_code += "    " + block.to_python_code()
        return f"for {self.var} in range({self.range_start}, {self.range_end}):\n{body_code}"




class WalkBlock:
    def __init__(self, distance):
        self.distance = distance
        self.inputs = None  # Liste pour stocker les blocs connectés en entrée
        self.output = None  # Bloc connecté en sortie

    def add_input(self, block):
        self.input = block

    def set_output(self, block):
        self.output = block

    def to_python_code(self):
        # Générer le code Python pour faire avancer Marty de 2 pas droit devant lui
        return f"MartyFunction.walk(steps={self.distance}, direction='auto', turn=0, step_length=35, step_time=1500)\n"

class DanceBlock:
    def __init__(self):
        pass
        self.inputs = None  # Liste pour stocker les blocs connectés en entrée
        self.output = None  # Bloc connecté en sortie
    
    def add_input(self, block):
        self.input = block
    
    def set_output(self, block):
        self.output = block

    def to_python_code(self):
        return f"MartyFunction.dance()\n"

class RotateBlock:
    def __init__(self, angle):
        self.angle = angle

    def to_python_code(self):
        return f"MartyFunction.turn(turn_amount={self.angle})\n"
    
class SideStepBlock:
    def __init__(self, distance):
        self.distance = distance

    def to_python_code(self):
        return f"MartyFunction.side_step(direction='left', steps={self.distance}, step_length=35, step_time=1000)\n"
    


class EyeMoveBlock:
    def __init__(self,direction):
        self.direction = direction
        self.inputs = None  # Liste pour stocker les blocs connectés en entrée
        self.output = None  # Bloc connecté en sortie
    
    def add_input(self, block):
        self.input = block
    
    def set_output(self, block):
        self.output = block

    def to_python_code(self):
        return f"eye_move({self.direction})\n"


    
class ConnectBlock:
    def __init__(self, robot_ip):
        self.robot_ip = robot_ip
        self.inputs = []  # Liste pour stocker les blocs connectés en entrée
        self.output = None  # Bloc connecté en sortie
    
    def add_input(self, block):
        self.inputs.append(block)
    
    def set_output(self, block):
        self.output = block

    def to_python_code(self):
        return f"marty = MartyFunction('{self.robot_ip}')\n"
    
class WaitBlock:
    def __init__(self, seconds):
        self.seconds = seconds
        self.inputs = None  # Liste pour stocker les blocs connectés en entrée
        self.output = None  # Bloc connecté en sortie
    
    def add_input(self, block):
        self.input = block
    
    def set_output(self, block):
        self.output = block

    def to_python_code(self):
        return f"MartyFunction.wait(seconds={self.seconds})\n"

        


 ####################################################################       
""""
blocks = [
    ForBlock("i",0,10,[WalkBlock(10),RotateBlock(90)]),
    
    WalkBlock(10),
    RotateBlock(90),
    SideStepBlock(10),
    
    EyeMoveBlock("left"),
    
]

code = ""
for block in blocks:
    code += block.to_python_code()

# Exécutez le code
try:
    exec(code)
except Exception as e:
    print(f"Error: {e}")

print(code)
"""
####################################################################

