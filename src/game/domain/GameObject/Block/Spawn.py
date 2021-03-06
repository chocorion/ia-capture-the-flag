from domain.GameObject.Block import Block

class Spawn(Block):
    """
    A block in which bots from a certain team can appear.
    """

    def __init__(self, team, x, y):
        super().__init__(x,y)
        self.transparent = True
        self.team = team

        self.color = (255, 0, 0, 30) if team == 1 else (0, 0, 255, 30)
