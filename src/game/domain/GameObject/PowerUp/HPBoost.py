from domain.GameObject.GameObject import GameObject
from domain.GameObject.Effect import Effect

class HPBoost(Effect):
    """
    Heals a bot
    """

    def __init__(self, x, y):
        super().__init__(x, y)
        self.duration = 0
        self.boost = 50
        
    def apply(self, bot):
        if not self.used:
            newHP = bot.health + self.boost
            bot.health = bot.maxHealth if newHP >= bot.maxHealth else newHP
            self.used = True
        
    def wearOut(self, bot):
        pass