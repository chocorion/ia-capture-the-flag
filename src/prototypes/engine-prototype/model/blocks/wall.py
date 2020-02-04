from model.blocks.block import Block

class Wall(Block):
    def __init__(self):
        super().__init__(False, True, (96, 90, 84, 255), 'wall')

    def __str__(self):
        return '#'