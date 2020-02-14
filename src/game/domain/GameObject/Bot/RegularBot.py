from domain.GameObject.Bot import Bot
from service.Physics import Physics

# An entity controlled by a Player
class RegularBot(Bot):

    def __init__(self, player, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.radius = 10 # Default radius of a regular bot
        self.player = player

        print("New bot in team {} | x: {}, y: {}".format(player,x,y))

    def isIn(self, x, y):
        return Physics.isInCircle(self.x, self.y, x, y, self.radius)
