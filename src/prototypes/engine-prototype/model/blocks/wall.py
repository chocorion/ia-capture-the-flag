from model.blocks.block import Block

class Wall(Block):
    def __init__(self):
        super().__init__(transparancy=False, solid=True)
        self._color = (43, 41, 41, 255)

    def __str__(self):
        return '#'