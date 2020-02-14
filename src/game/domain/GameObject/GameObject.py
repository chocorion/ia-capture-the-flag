

# Any entity that has a presence in the map
class GameObject:

    def __init__(self):
        self.x = None # Real x coordinate
        self.y = None # Real y coordinate

    def isIn(self, x, y):
        raise NotImplementedError