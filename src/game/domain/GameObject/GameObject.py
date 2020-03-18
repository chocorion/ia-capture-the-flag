

class GameObject:
    """
    Any entity that has a presence in the map

    Attributes:
        x (int) : Real x coordinate
        y (int) : Real y coordinate
        pickable (bool) : Whether it can be picked up and moved around
        held (bool) : Whether it is held by someone or something
        category (String) : Object category (to call the correct class)

    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pickable = False
        self.held = False
        self.category = "Default"

    def move(self, x, y):
        self.x += x
        self.y += y

    def isIn(self, x, y):
        raise NotImplementedError