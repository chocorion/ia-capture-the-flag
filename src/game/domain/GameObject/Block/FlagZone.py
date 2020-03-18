from domain.GameObject.Block import Block

class FlagZone(Block):
    """
    Zone in wich flag will spawn.
    """

    def __init__(self, team, x, y):
        super().__init__(x, y)
        self.team = team
        self.transparent = True

        self.color = (200, 100, 100, 30) if team == 1 else (100, 100, 200, 30)
