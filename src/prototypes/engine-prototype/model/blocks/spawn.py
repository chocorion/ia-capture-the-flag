from model.blocks.block import Block

class Spawn(Block):
    def __init__(self, team_number):
        super().__init__(transparancy=True, solid=False)
        self._team_number = team_number

        self._color = (228, 85, 61, 30) if team_number == 1 else (125, 174, 159, 30)
        self._name = 'spawn'

    def get_team(self):
        return self._team_number

    def __str__(self):
        return str(self._team_number)