from domain.GameObject import GameObject
from math import sqrt

# An entity controlled by a Player
class Bot(GameObject):

    def __init__(self, player, x, y):
        self.x = None
        self.y = None
        self.angle = None
        self.player = None

        self.color = None
        raise NotImplementedError

    def move(self, x, y):
        self.x += x
        self.y += y

    def rotate(self, angle):
        self.angle += angle