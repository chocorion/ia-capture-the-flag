from domain.GameObject import GameObject

class Flag(GameObject):
    
    def __init__(self, team, x, y):
        self.team = team
        self.x = x
        self.y = y

        self.color = (255, 0, 0, 30) if team == 1 else (0, 0, 255, 30)