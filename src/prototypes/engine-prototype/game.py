#!/usr/bin/env python3

from model import *
from view import *
from controller import *
from ai import *

import time, sys
import pygame # tmp, for quit

from ruleset import ruleset

TARGET_FPS = 60

class Game:
    def __init__(self, map_name=None):
        if map_name == None:
            map_name = ruleset["DEFAULT_MAP"]

        self._clock = pygame.time.Clock()
        self._fps = TARGET_FPS

        self._model = Game_model(map_filename=map_name)
        self._view = Game_view(self._model)
        self._controller = Game_controller(self._model, self._view)


        # For latter -> Match class
        # Must give a copy of the map !!!
        self.register(Basic_AI)
        self.register(Basic_AI)



    def game_loop(self):

        # Initp pygame clock
        dt = self._clock.tick(self._fps)

        while True:
            # self._show_fps()

            dt = self._clock.tick(self._fps)

            self._controller.tick(dt)
            self._model.tick(dt)
            self._view.tick(dt)

    def register(self, player):
        
        self._model.set_ai(player)

        return self._model._map


    def _show_fps(self):
        print("{:6s}".format(str((self._clock.get_fps()))), end="\r")
            


if __name__ == '__main__':
    print("Hello !")

    game = Game()
    game.game_loop()

    print("Bye !")
    