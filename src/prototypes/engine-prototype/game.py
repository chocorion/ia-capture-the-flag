#!/usr/bin/env python3

from model import *
from view import *

DEFAULT_MAP = "model/map/map_files/map_00.txt"

class Game:
    def __init__(self, map_name=DEFAULT_MAP):
        self._model = Game_model(map_filename=map_name)
        self._view = Game_view(self._model)

        # Ugly, we need the view to get cell size
        self._model.generate_bots(5)

    def game_loop(self):
        while True:
            self._view.display()

if __name__ == '__main__':
    print("Hello !")

    game = Game()
    game.game_loop()

    print("Bye !")
    