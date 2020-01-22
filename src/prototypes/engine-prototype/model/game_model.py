from model.map import *
from model.blocks import *

class Game_model:
    def __init__(self, map_filename):
        self._map = Map(filename=map_filename)

        print(self._map)