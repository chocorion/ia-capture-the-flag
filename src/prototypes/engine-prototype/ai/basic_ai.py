from ai.ai_interface import AI
from ai.bot import Bot

from random import randrange

test_dest = [
    (40 * 50,     40 * 50,    100),
    (40 * 50,     40 * 50,    70),
    (40 * 50,     40 * 50,   70),
    (40 * 50,     40 * 50,   700),
    (40 * 50,     40 * 50,     100)
]

class Basic_AI(AI):
    def __init__(self, team, number_of_bots):
        super().__init__(team, number_of_bots)

        self._bots = [Bot() for i in range(number_of_bots)]


    def tick(self, datas):
        # return [
        #     (randrange(0, 1000), randrange(0, 1000), randrange(100))  for i in range(super().get_number_of_bots())
        # ]

        return test_dest