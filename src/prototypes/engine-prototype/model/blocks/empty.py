from model.blocks.block import Block

class Empty(Block):
    def __init__(self):
        super().__init__(True, False, (240, 240, 240, 255), 'empty')

    def __str__(self):
        return ' '