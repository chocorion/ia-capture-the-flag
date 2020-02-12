from domain.GameObject.Block import Block

# An uncrossable block you can see through
class WallTransparent(Block):

        def __init__(self):
            self.solid = True
            self.transparent = True
