#!/usr/bin/env python3

from model import *

DEFAULT_MAP = "model/map/map_files/map_00.txt"

class Game:
    def __init__(self, map_name=DEFAULT_MAP):
        self.game_model = Game_model(map_filename=map_name)

    def game_loop(self):
        pass

if __name__ == '__main__':
    print("Hello !")

    game = Game()
    game.game_loop()

    print("Bye !")
    