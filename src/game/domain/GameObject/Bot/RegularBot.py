from domain.GameObject.Bot import Bot
from service.Physics import Physics

class RegularBot(Bot):
    """
    Just a regular Bot.
    """

    def __init__(self, player, x, y):
        super().__init__(player, x, y)

        self.maxHealth = 100
        self.health = self.maxHealth
        
        self.angle = 0
        self.radius = 36 # Default radius of a regular bot
        self.speed = 0
        self.reach = self.radius + 30
        
        self._maxSpeed = 15 # Default max speed
        self.speedmultiplier = 1 # Default speed multiplier
        self.maxRotate = 18 # Default max rotation in degrees
        
        self.fov = 50 # Default FOV
        self.viewDistance = 400 # Default view distance

        # self.hitbox = Physics.createCirclePolygon(6)

        self.color = (255, 0, 0, 255) if player == 1 else (0, 0, 255, 255)

    def isIn(self, x, y):
        return Physics.isInCircle(self.x, self.y, x, y, self.radius)

    def getMaxSpeed(self):
        return self._maxSpeed * self.speedmultiplier