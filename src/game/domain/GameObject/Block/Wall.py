from domain.GameObject.Block import Block

# An uncrossable block
class Wall(Block):

        def __init__(self):
            self.solid = True
            self.transparent = False
