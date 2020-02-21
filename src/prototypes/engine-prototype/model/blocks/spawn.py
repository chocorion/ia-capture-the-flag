from model.blocks.block import Block

class Spawn(Block):
    def __init__(self, teamNumber):
        super().__init__(transparancy=True, solid=False)
        self._teamNumber = teamNumber

        self._color = (228, 85, 61, 30) if teamNumber == 1 else (125, 174, 159, 30)
        self._name = 'spawn'

    def get_team(self):
        return self._teamNumber

    def __str__(self):
        return str(self._teamNumber)