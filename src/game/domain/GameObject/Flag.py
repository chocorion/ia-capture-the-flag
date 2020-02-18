from domain.GameObject import GameObject

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
        super().__init__(x, y)
        self.team = team
        self.pickable = True
        print(team,x,y)

        self.color = (255, 0, 0, 200) if team == 1 else (0, 0, 255, 200)