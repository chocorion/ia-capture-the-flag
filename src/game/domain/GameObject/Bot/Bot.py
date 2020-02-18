from domain.GameObject import GameObject
from math import sqrt

class Bot(GameObject):
    """
    An entity controlled by a Player

    Attributes:

        heldItems (list(GameObject)) : The items held by this bot
        angle (int) : Angle the bot is facing in degrees.
        speed (int) : Current speed of the bot.

        player (int) : Player/Team number
        
        max_speed (int) : The maximum speed this bot can reach.
        max_rotate (int) : Max rotation in degrees
        fov (int) : Field of View of the bot.
        view_distance (int) : Distance to which the bot can see.

        color (rgba) : Color of the bot (Needs to be moved in View somehow)

    """

    def __init__(self, player, x, y):
        super().__init__(x, y)
        self.pickable = False
        self.heldItems = list()

        ### Redefine these to create a custom bot
        self.angle = None
        self.player = None
        self.speed = None
        
        self.max_speed = None
        self.max_rotate = None
        
        self.fov = None
        self.view_distance = None

        self.color = None
        ###

    def pickUp(self, gameObject):
        if not gameObject.held:
            gameObject.held = True
            gameObject.x = self.x
            gameObject.y = self.y
            self.heldItems.append(gameObject)

    def drop(self, gameObject):
        self.heldItems.remove(gameObject)
        gameObject.held = False

    def move(self, x, y):
        super().move(x,y)

        for item in self.heldItems:
            item.move(x,y)

    def rotate(self, angle):
        self.angle += angle