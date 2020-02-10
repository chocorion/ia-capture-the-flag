from model.blocks.block import Block

class End(Block):
    def __init__(self):
        super().__init__(True, False, (105, 114, 104, 255), 'end')

    def __str__(self):
        return 'E'