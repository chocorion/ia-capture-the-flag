from domain.GameObject import GameObject
from math import sqrt

# An entity controlled by a Player
class Bot(GameObject):

    def __init__(self, x, y, radius):
        self.x = None
        self.y = None
        self.angle = None
        raise NotImplementedError