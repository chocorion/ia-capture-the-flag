from model.blocks.block import Block

class Flag(Block):
    def __init__(self):
        super().__init__(transparancy=True, solid=False)
        self._color = (142, 182, 101, 255)

    def __str__(self):
        return 'F'