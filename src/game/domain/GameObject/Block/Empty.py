from domain.GameObject.Block import Block

# Floor you can walk on and see through
class Empty(Block):

        def __init__(self):
            self.solid = False
            self.transparent = True

            self.color = (240,240,240,255)
