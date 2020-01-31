#!/usr/bin/env python3

from model import *
from view import *
from ai import *

import time, sys
import pygame # tmp, for quit

TARGET_FPS = 60
NUMBER_OF_BOTS = 5 # Warning Same cst in other parts of the code

DEFAULT_MAP = "model/map/map_files/map_00.txt"

class Game:
    def __init__(self, map_name=DEFAULT_MAP):

        self._clock = pygame.time.Clock()
        self._fps = TARGET_FPS

        self._model = Game_model(map_filename=map_name)
        self._view = Game_view(self._model)


        # For latter -> Match class

        self._model.set_ai(1, Basic_AI(1, NUMBER_OF_BOTS))
        self._model.set_ai(2, Basic_AI(2, NUMBER_OF_BOTS))



    def game_loop(self):

        while True:
            # self._show_fps()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            dt = self._clock.tick(self._fps)

            self._model.tick(dt)
            self._view.tick(dt)

    def _show_fps(self):
        print("{:6s}".format(str((self._clock.get_fps()))), end="\r")
            


if __name__ == '__main__':
    print("Hello !")

    game = Game()
    game.game_loop()

    print("Bye !")
    