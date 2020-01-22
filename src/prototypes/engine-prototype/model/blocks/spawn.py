from model.blocks.block import Block

class Spawn(Block):
    def __init__(self, team_number):
        super().__init__(transparancy=True, solid=False)
        self._team_number = team_number

    def __str__(self):
        return str(self._team_number)