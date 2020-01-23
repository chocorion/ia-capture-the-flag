from model.map import *
from model.blocks import *
from model.game_objects import *

from random import randrange
import sys

DEFAULT_BOOT_PER_SQUAD = 5
class Game_model:
    def __init__(self, map_filename):
        self._map = Map(filename=map_filename)
        self._generate_bots(DEFAULT_BOOT_PER_SQUAD)


    def _generate_bots(self, bots_per_squad):
        self._bots = [[], []]
        print(self._map.get_spawn_zones())
        sys.exit(0)
        for i in range(bots_per_squad):
            self._bots[0].append(Bot(team=1, x=randrange(0, 800), y=randrange(0, 800)))
            self._bots[1].append(Bot(team=2, x=randrange(0, 800), y=randrange(0, 800)))


    def get_map(self):
        return self._map

    
    def get_bots(self):
        return self._bots[0] + self._bots[1]