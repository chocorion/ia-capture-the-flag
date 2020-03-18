from domain.GameObject.Block import Block

class Depot(Block):
    """
    Zone in wich IA must bring flag to win.
    """

    def __init__(self, team, x, y):
        super().__init__(x, y)
        self.team = team
        self.transparent = True

        self.color = (120, 80, 80, 30) if team == 1 else (80, 80, 120, 30)
