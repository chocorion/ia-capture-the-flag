from model.blocks.block import Block

class Transparent_wall(Block):
    def __init__(self):
        super().__init__(True, True,(151, 151, 151, 255),'transparent_wall')

    def __str__(self):
        return '-'