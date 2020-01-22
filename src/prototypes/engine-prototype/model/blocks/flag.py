from model.blocks.block import Block

class Flag(Block):
    def __init__(self):
        super().__init__(transparancy=True, solid=False)

    def __str__(self):
        return 'F'