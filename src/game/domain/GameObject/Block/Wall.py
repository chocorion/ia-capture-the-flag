from domain.GameObject.Block import Block

# An uncrossable block
class Wall(Block):

        def __init__(self):
            self.solid = True
            self.transparent = False

            self.color = (96,90,84,255)
