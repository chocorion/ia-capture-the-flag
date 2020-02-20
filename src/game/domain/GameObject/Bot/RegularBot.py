from domain.GameObject.Bot import Bot
from service.Physics import Physics

class RegularBot(Bot):
    """
    Just a regular Bot.
    """

    def __init__(self, player, x, y):
        super().__init__(player, x, y)

        self.health = 100
        
        self.angle = 0
        self.radius = 36 # Default radius of a regular bot
        self.speed = 0
        
        self.max_speed = 15 # Default max speed
        self.max_rotate = 18 # Default max rotation in degrees
        
        self.fov = 50 # Default FOV
        self.view_distance = 35 # Default view distance


        self.color = (255, 0, 0, 255) if player == 1 else (0, 0, 255, 255)

        print("New bot in team {} | x: {}, y: {}".format(player,x,y))

    def isIn(self, x, y):
        return Physics.isInCircle(self.x, self.y, x, y, self.radius)