from domain.GameObject.GameObject import GameObject
from domain.Map import Map

class Effect(GameObject):
    """
    Applies an effect on a bot during a period of time
    """

    def __init__(self, x, y):
        super().__init__(x * Map.BLOCKSIZE, y * Map.BLOCKSIZE)
        self.duration = 0
        self.category = "Effect"
        
    def apply(self, bot):
        """
        Redefine to apply your effect
        """
        pass
        
    def wearOut(self, bot):
        """
        Redefine to undo your effect
        """
        pass