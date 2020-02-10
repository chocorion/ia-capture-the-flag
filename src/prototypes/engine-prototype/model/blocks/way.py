from model.blocks.block import Block

class Way(Block):
    def __init__(self):
        super().__init__(True, False, (183, 209, 218, 255), 'way')

    def __str__(self):
        return 'W'