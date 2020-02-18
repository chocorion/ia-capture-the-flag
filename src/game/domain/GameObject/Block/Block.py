from domain.GameObject import GameObject

class Block(GameObject):
    """
    A block. Can be part of a Map.

    Attributes:
        solid (bool) : Whether or not collisions apply to this block.
        transparent (bool) : Whether or not vision collisions apply to this block.

        color (rgba) : Color of the block (Needs to be moved in View somehow)
    """

    def __init__(self, x, y):
        super().__init__(x, y)
        self.solid = False
        self.transparent = False

        self.color = None