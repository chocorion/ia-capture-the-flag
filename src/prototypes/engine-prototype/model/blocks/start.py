from model.blocks.block import Block

class Start(Block):
    def __init__(self):
        super().__init__(True, False, (149, 163, 164, 255), 'start')

    def __str__(self):
        return 'S'