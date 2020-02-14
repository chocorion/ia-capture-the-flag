from domain.GameObject.Bot import Bot
from service.Physics import Physics

# An entity controlled by a Player
class RegularBot(Bot):

    def __init__(self, player, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.radius = 36 # Default radius of a regular bot
        self.speed = 0
        self.player = player

        self.color = (255, 0, 0, 255) if player == 1 else (0, 0, 255, 255)

        print("New bot in team {} | x: {}, y: {}".format(player,x,y))

    def isIn(self, x, y):
        return Physics.isInCircle(self.x, self.y, x, y, self.radius)
