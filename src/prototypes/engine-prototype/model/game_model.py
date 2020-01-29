from model.map import *
from model.blocks import *
from model.game_objects import *
from view import *

from random import (randrange, uniform)
import sys


DEFAULT_BOOT_PER_SQUAD = 5


class Game_model:

    def __init__(self, map_filename):
        # Model need an inner representation of the game
        self._cell_size = 100
        self._default_bot_radius = 40

        self._map = Map(filename=map_filename)
        self._generate_bots(bots_per_squad=DEFAULT_BOOT_PER_SQUAD)

    def _generate_bots(self, bots_per_squad):
        self._bots = [[], []]
        spawn_zones = self._map.get_spawn_zones()

        [x1, y1, w1, h1] = spawn_zones[1]
        [x2, y2, w2, h2] = spawn_zones[2]      

        infos = (
            [1] + spawn_zones[1],
            [2] + spawn_zones[2]
        )

        margin = self._default_bot_radius/self._cell_size
        print(margin)


        for i in range(bots_per_squad):
            for (team, x, y, w, h) in infos:
                self._bots[team - 1].append(
                    Bot(
                        team=team,
                        x = round(uniform(x + margin, x + w - margin), 2) * self._cell_size,
                        y = round(uniform(y + margin, y + h - margin), 2) * self._cell_size,
                        radius=self._default_bot_radius
                    )
                )


    def get_map(self):
        return self._map

    
    def get_bots(self):
        return self._bots[0] + self._bots[1]

    def get_cell_size(self):
        return self._cell_size