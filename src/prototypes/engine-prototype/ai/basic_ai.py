from ai.ai_interface import AI
from ai.bot import Bot
from ai.astar import *

from random import randrange
import math

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def build_graph(game_map):
    nodeGraph = []
    for x in range(game_map.get_width()):
        for y in range(game_map.get_height()):
            insertNode(x, y, str(game_map.get_tile(x,y)), nodeGraph)

    return nodeGraph

class Basic_AI(AI):
    def __init__(self, team, number_of_bots, game_map):
        super().__init__(team, number_of_bots, game_map)

        game_map = super().get_map()

        self._bots = [Bot(game_map) for i in range(number_of_bots)]

        for bot_index in range(len(self._bots)):
            self._bot_set_random_dest(bot_index)
            self._bots[bot_index].save_pos() 

        self._node_graph = build_graph(super().get_map())


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
            (x, y, angle, dest) = datas[bot_index]
            self._bots[bot_index].update(x, y, angle)

            # print(dest)

            (last_pos_x, last_pos_y) = self._bots[bot_index].get_saved_pos()


            if dest != None:
                (dest_x, dest_y) = dest
                (bot_dest_x, bot_dest_y) = self._bots[bot_index].get_dest()

                if dest_x != bot_dest_x or dest_y != bot_dest_y:
                    print("\tBot {} -> dest set to {}:{}".format(bot_index, dest_x, dest_y))
                    self._bots[bot_index].set_dest(dest_x, dest_y, self._node_graph)

                elif distance(x, y, dest_x, dest_y) < 30:
                    print("Bot reach destination ! Now random dest.")
                    self._bot_set_random_dest(bot_index)



            self._bots[bot_index].save_pos()
            (bot_dest_x, bot_dest_y) = self._bots[bot_index].get_next_dest()

            result.append((bot_dest_x, bot_dest_y, 100))

        return result