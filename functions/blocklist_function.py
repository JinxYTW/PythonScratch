from functions.marty_function import MartyFunction
from ui.work_area import WorkArea
from blocks.for_block_widget import ForBlockWidget
from blocks.walk_block_widget import WalkBlockWidget
from blocks.connect_block_widget import ConnectBlockWidget  
from blocks.dance_block_widget import DanceBlockWidget
from blocks.rotate_block_widget import RotateBlockWidget
from blocks.side_step_block_widget import SideStepBlockWidget
from blocks.wait_block_widget import WaitBlockWidget
from models.interpreter import ForBlock, WalkBlock,ConnectBlock, DanceBlock, RotateBlock, SideStepBlock, WaitBlock
from models.ip_manager import IPManager

class BlocklistFunction:
    def __init__(self, work_area):
        self.work_area = work_area
        self.marty_ip = IPManager.get_instance().get_ip_address1()

    def execute_program(self):
        work_area = self.work_area
        blocks = work_area.get_widgets()
        print(f"Nombre de blocs dans la zone de travail : {len(blocks)}")
        connections = work_area.get_connections()
        print(f"Nombre de connexions dans la zone de travail : {len(connections)}")

    def organize_blocks_for_execution(self):
        blocks = self.work_area.get_widgets()
        print(blocks)
        connections = self.work_area.get_connections()
        print(connections)
        next_blocks = {block: {'loop_exit': [], 'body_code': []} for block in blocks}

        for start_block, end_block, connection_point in connections:
            connection_type = self.work_area.connection_manager.get_connection_type(connection_point)
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

        # Generate the code from the ordered blocks
        code = """
marty_function = MartyFunction("{marty_ip}")
marty_function.connect()
""".format(marty_ip=self.marty_ip)

        for block_info in ordered_blocks:
            block_widget = block_info[0]
            if isinstance(block_widget, ForBlockWidget):
                var = block_widget.get_variable()
                range_start = block_widget.get_range_start()
                range_end = block_widget.get_range_end()
                body_blocks = block_info[1]
                body_code = [self.convert_block_to_interpreter(b) for b in body_blocks]
                code += ForBlock(var, range_start, range_end, body_code).to_python_code()
            elif isinstance(block_widget, WalkBlockWidget):
                code += "marty_function.walk(steps=2, direction='auto', turn=0, step_length=35, step_time=1500)\n"
            elif isinstance(block_widget, ConnectBlockWidget):
                code += self.connect_marty_code()
            elif isinstance(block_widget, DanceBlockWidget):
                code += "marty_function.dance()\n"
            elif isinstance(block_widget, RotateBlockWidget):
                angle = block_widget.get_angle()
                code += f"marty_function.turn(turn_amount={angle})\n"
            elif isinstance(block_widget, SideStepBlockWidget):
                direction = block_widget.get_direction()
                code += f"marty_function.side_step(direction='{direction}')\n"
            elif isinstance(block_widget, WaitBlockWidget):
                seconds = block_widget.get_duration()
                code += f"marty_function.wait(seconds={seconds})\n"


        print(code)
        try:
            exec(code)
        except Exception as e:
            print(f"Error: {e}")

    def convert_block_to_interpreter(self, block_info):
        block_widget = block_info[0]
        if isinstance(block_widget, ForBlockWidget):
            var = block_widget.get_variable()
            range_start = block_widget.get_range_start()
            range_end = block_widget.get_range_end()
            body_blocks = block_info[1]
            body_code = [self.convert_block_to_interpreter(b) for b in body_blocks]
            return ForBlock(var, range_start, range_end, body_code)
        elif isinstance(block_widget, WalkBlockWidget):
            return WalkBlock(2)
        elif isinstance(block_widget, ConnectBlockWidget):
            return self.connect_marty_code()
        elif isinstance(block_widget, DanceBlockWidget):
            return DanceBlock()
        elif isinstance(block_widget, RotateBlockWidget):
            angle = block_widget.get_angle()
            return RotateBlock(angle)
        elif isinstance(block_widget, SideStepBlockWidget):
            direction = block_widget.get_direction() 
            return SideStepBlock(direction)
        elif isinstance(block_widget, WaitBlockWidget):
            seconds = block_widget.get_duration()  
            return WaitBlock(seconds)
        






    def connect_marty_code(self):
        return """
marty_function = MartyFunction("{marty_ip}")
marty_function.connect()
""".format(marty_ip=self.marty_ip)
