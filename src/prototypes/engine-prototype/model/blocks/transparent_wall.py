from model.blocks.block import Block

class Transparent_wall(Block):
    def __init__(self):
        super().__init__(transparancy=True, solid=True)

    def __str__(self):
        return '-'