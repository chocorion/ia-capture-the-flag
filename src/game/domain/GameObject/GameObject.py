

class GameObject:
    """
    Any entity that has a presence in the map

    Attributes:
        x (int) : Real x coordinate
        y (int) : Real y coordinate

    """

    def __init__(self):
        raise NotImplementedError

    def isIn(self, x, y):
        raise NotImplementedError