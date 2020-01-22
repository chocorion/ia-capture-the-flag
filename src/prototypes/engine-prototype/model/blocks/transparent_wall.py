from model.blocks.block import Block

class Transparent_wall(Block):
    def __init__(self):
        super().__init__(transparancy=True, solid=True)
        self._color = (61, 61, 61, 255)

    def __str__(self):
        return '-'