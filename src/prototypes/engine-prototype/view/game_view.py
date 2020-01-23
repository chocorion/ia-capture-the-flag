import pygame
from pygame.locals import *

from model.map import *
from model.blocks import *

from math import (ceil, floor)
import sys

# Faire attention à comment gérer la taille des bots dans le modèle qui peut être différente de celle
# de la vue.

WIDTH = 1200
HEIGHT = 800

# Ugly
CELL_SIZE = 0
BOT_RADIUS = 0

class Game_view:
    def __init__(self, model):
        global CELL_SIZE

        pygame.init()
        self._window = pygame.display.set_mode((WIDTH, HEIGHT))
        
        self._model = model
        current_map = model.get_map()

        self._cell_size = min(WIDTH//current_map.get_width(), HEIGHT//current_map.get_height())
        self._bot_radius = ceil(self._cell_size/3)

        CELL_SIZE = self._cell_size
        BOT_RADIUS = self._bot_radius


    def display(self):
        self._display_map()
        self._display_bots()
        
        pygame.display.flip()

    def _display_map(self):
        current_map = self._model.get_map()

        for y in range(current_map.get_height()):
            for x in range(current_map.get_width()):
                current_rect = pygame.Rect(
                    x * self._cell_size,
                    y * self._cell_size,
                    self._cell_size,
                    self._cell_size
                )

                (r, g, b, a) = current_map.get_tile(x, y).get_color()

                pygame.draw.rect(self._window, pygame.Color(r, g, b), current_rect)


    def _display_bots(self):
        bots = self._model.get_bots()

        for bot in bots:
            (r, g, b, a) = bot.get_color()

            print(bot.get_coord_int())
            print(self._bot_radius)
            
            pygame.draw.circle(
                self._window,
                pygame.Color(r, g, b),
                bot.get_coord_int(),
                self._bot_radius
            )

    @staticmethod
    def get_cell_size():
        return CELL_SIZE

    @staticmethod
    def get_bot_radius():
        return BOT_RADIUS
            
