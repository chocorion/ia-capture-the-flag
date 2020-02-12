from Bot import Bot
from service.Physics import Physics

# An entity controlled by a Player
class RegularBot(Bot):

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.angle = 0
        self.radius = radius

    def isIn(self, x, y):
        return Physics.isInCircle(self.x, self.y, x, y, self.radius)
