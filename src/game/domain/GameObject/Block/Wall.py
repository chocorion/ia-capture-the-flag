from domain.GameObject.Block import Block

class Wall(Block):
    """
    A block that can never be crossed.
    """

    def __init__(self, x, y):
        super().__init__(x, y)
        self.solid = True

        self.color = (96,90,84,255)
