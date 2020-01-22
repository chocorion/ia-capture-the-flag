from model.blocks.block import Block

class Empty(Block):
    def __init__(self):
        super().__init__(transparancy=True, solid=False)
        self._color = (255, 255, 255, 255)

    def __str__(self):
        return ' '