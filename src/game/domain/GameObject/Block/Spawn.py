from domain.GameObject.Block import Block

# A block in which bots from a certain team can appear
class Spawn(Block):

        def __init__(self, team):
            self.solid = False
            self.transparent = True
            self.team = team
