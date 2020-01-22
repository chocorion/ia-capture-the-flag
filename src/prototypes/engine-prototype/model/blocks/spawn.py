from model.blocks.block import Block

class Spawn(Block):
    def __init__(self, team_number):
        super().__init__(transparancy=True, solid=False)
        self._team_number = team_number

        self._color = (228, 85, 61, 255) if team_number == 1 else (125, 174, 159, 255)

    def __str__(self):
        return str(self._team_number)