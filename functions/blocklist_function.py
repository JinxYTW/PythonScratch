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


    def organize_blocks_for_execution(self):
        blocks = self.work_area.get_widgets()
        print(blocks)
        connections = self.work_area.get_connections()
        print (connections)
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