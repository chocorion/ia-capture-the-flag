from domain.GameObject.Block import Block

class Empty(Block):
    """
    Just an empty block. Used as a regular floor.
    """

    def __init__(self, x, y):
        super().__init__(x, y)
        self.transparent = True

        self.color = (240,240,240,255)
