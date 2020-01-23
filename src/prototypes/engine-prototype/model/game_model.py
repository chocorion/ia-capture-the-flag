from model.map import *
from model.blocks import *
from model.game_objects import *
from view import *

from random import (randrange, uniform)
import sys

DEFAULT_BOOT_PER_SQUAD = 5
class Game_model:
    def __init__(self, map_filename):
        self._map = Map(filename=map_filename)
        # self._generate_bots(DEFAULT_BOOT_PER_SQUAD)


    def generate_bots(self, bots_per_squad):
        self._bots = [[], []]
        spawn_zones = self._map.get_spawn_zones()

        [x1, y1, w1, h1] = spawn_zones[1]
        [x2, y2, w2, h2] = spawn_zones[2]      

        cell_size = Game_view.get_cell_size()
        bot_radius = Game_view.get_bot_radius()

        # round(random.uniform(1,2), N)

        for i in range(bots_per_squad):
            self._bots[0].append(Bot(team=1, x=randrange(x1, x1 + w1) * cell_size + bot_radius, y=randrange(y1, y1 + h1) * cell_size + bot_radius))
            self._bots[1].append(Bot(team=2, x=randrange(x2, x2 + w2) * cell_size + bot_radius, y=randrange(y2, y2 + h2) * cell_size + bot_radius))



    def get_map(self):
        return self._map

    
    def get_bots(self):
        return self._bots[0] + self._bots[1]