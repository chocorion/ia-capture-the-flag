from domain.GameObject import GameObject
from domain.Map import Map

class Flag(GameObject):
    """
    A flag that belongs to a team and can be moved by bots.

    Attributes:
        x (int) : Real x coordinate
        y (int) : Real y coordinate
        team (int) : Team number
        color (rgba) : Color of the flag (Needs to be moved in View somehow)

    """
    
    def __init__(self, team, x, y):
        self.width = Map.BLOCKSIZE // 2
        self.height = Map.BLOCKSIZE // 2

        super().__init__(x + self.width, y +  + self.height)
        self.team = team
        self.pickable = True

        self.color = (255, 0, 0, 200) if team == 1 else (0, 0, 255, 200)