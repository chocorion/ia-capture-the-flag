from model.blocks.block import Block

class Wall(Block):
    def __init__(self):
        super().__init__(transparancy=False, solid=True)

    def __str__(self):
        return '#'