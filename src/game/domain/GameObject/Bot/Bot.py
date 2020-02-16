from domain.GameObject import GameObject
from math import sqrt

class Bot(GameObject):
    """
    An entity controlled by a Player

    Attributes:
        x (int) : Real x coordinate
        y (int) : Real y coordinate
        player (int) : Player/Team number
        angle (int) : Angle the bot is facing in degrees.
        color (rgba) : Color of the bot (Needs to be moved in View somehow)

    """

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