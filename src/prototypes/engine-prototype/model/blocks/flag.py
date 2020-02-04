from model.blocks.block import Block

class Flag(Block):
    def __init__(self):
        super().__init__(True, False, (142, 182, 101, 255), 'flag')

    def __str__(self):
        return 'F'