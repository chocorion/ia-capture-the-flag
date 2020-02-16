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
        speed (int) : Current speed of the bot.
        fov (int) : Field of View of the bot.
        view_distance (int) : Distance to which the bot can see.
        color (rgba) : Color of the bot (Needs to be moved in View somehow)

        max_speed (int) : The maximum speed this bot can reach.

    """

    def __init__(self, player, x, y):
        self.x = None
        self.y = None
        self.angle = None
        self.player = None
        self.speed = None
        
        self.fov = None
        self.view_distance = None

        self.color = None
        raise NotImplementedError

    def move(self, x, y):
        self.x += x
        self.y += y

    def rotate(self, angle):
        self.angle += angle