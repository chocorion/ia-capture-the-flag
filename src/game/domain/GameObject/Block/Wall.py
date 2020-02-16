from domain.GameObject.Block import Block

class Wall(Block):
    """
    A block that can never be crossed.
    """

    def __init__(self):
        self.solid = True
        self.transparent = False

        self.color = (96,90,84,255)
