from domain.GameObject.Block import Block

class WallTransparent(Block):
    """
    A block that can never be crossed but you can see through.
    """

    def __init__(self):
        self.solid = True
        self.transparent = True

        self.color = (153,153,153,255)
