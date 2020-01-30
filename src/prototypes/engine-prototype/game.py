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

        self._model = Game_model(map_filename=map_name)
        self._view = Game_view(self._model)


        # For latter -> Match class

        self._model.set_ai(1, Basic_AI(1, NUMBER_OF_BOTS))
        self._model.set_ai(2, Basic_AI(2, NUMBER_OF_BOTS))



    def game_loop(self):
        prev_time = time.time()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            self._model.tick()
            self._view.display()
            
            curr_time = time.time()
            diff = curr_time - prev_time
            delay = max(1.0/TARGET_FPS - diff, 0)
            time.sleep(delay)
            fps = 1.0/(delay + diff)
            prev_time = curr_time
            print("FPS -> {:4s}".format(str(round(fps, 2))), end='\r')


if __name__ == '__main__':
    print("Hello !")

    game = Game()
    game.game_loop()

    print("Bye !")
    