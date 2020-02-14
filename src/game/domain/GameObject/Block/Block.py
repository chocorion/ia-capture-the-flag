from domain.GameObject import GameObject

# A map tile
class Block(GameObject):

    def __init__(self):

        self.solid = None           # Wether another entity must collide with this
        self.transparent = None     # Wether light can travel through this

        self.color = None

        raise NotImplementedError