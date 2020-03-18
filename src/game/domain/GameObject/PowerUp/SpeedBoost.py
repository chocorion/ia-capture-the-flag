from domain.GameObject.GameObject import GameObject
from domain.GameObject.Effect import Effect

class SpeedBoost(Effect):
    """
    Applies a speed boost to a bot
    """

    def __init__(self, x, y):
        super().__init__(x, y)
        self.pickable = False
        self.used = False
        self.duration = 3000
        self.multiplier = 1.5
        
    def apply(self, bot):
        if not self.used:
            bot.speedmultiplier = bot.speedmultiplier + (self.multiplier - 1)
            self.used = True
        
    def wearOut(self, bot):
        bot.speedmultiplier = bot.speedmultiplier - (self.multiplier - 1)