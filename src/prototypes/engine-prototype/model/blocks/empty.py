from model.blocks.block import Block

class Empty(Block):
    def __init__(self):
        super().__init__(True, False, (255, 255, 255, 255), 'empty')

    def __str__(self):
        return ' '