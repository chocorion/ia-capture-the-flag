from ai.ai_interface import AI
from ai.bot import Bot

from random import randrange
import math

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

class Basic_AI(AI):
    def __init__(self, team, number_of_bots, game_map):
        super().__init__(team, number_of_bots, game_map)

        self._bots = [Bot() for i in range(number_of_bots)]

        for bot_index in range(len(self._bots)):
            self._bot_set_random_dest(bot_index)
            self._bots[bot_index].save_pos()




    def _bot_set_random_dest(self, bot_index):
        map_cell_size = super().get_map().get_cell_size()
        map_width  = super().get_map().get_width()
        map_height = super().get_map().get_height()


        self._bots[bot_index].set_dest(
            randrange(map_cell_size, map_width * map_cell_size),
            randrange(map_cell_size, map_height * map_cell_size)
        )


    def tick(self, datas):
        result = []

        for bot_index in range(len(self._bots)):
            (x, y, angle) = datas[bot_index]
            self._bots[bot_index].update(x, y, angle)

            (last_pos_x, last_pos_y) = self._bots[bot_index].get_saved_pos()
            (dest_x, dest_y) = self._bots[bot_index].get_dest()

            if distance(x, y, last_pos_x, last_pos_y) < 3:
                self._bot_set_random_dest(bot_index)

            elif distance(x, y, dest_x, dest_y) < 30:
                self._bot_set_random_dest(bot_index)
            

            self._bots[bot_index].save_pos()
            (dest_x, dest_y) = self._bots[bot_index].get_dest()

            result.append((dest_x, dest_y, 100))

        return result