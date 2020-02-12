from domain.GameObject import GameObject

class Flag(GameObject):
    
    def __init__(self, team, x, y):
        self.team = team
        self.x = x
        self.y = y