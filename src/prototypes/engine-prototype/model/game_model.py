from model.map import *
from model.blocks import *

class Game_model:
    def __init__(self, map_filename):
        self._map = Map(filename=map_filename)


    def get_map(self):
        return self._map