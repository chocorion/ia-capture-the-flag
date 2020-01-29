import pygame
import pygame.gfxdraw
from pygame.locals import *

from model.map import *
from model.blocks import *

from math import (ceil, floor)
import sys

# Faire attention à comment gérer la taille des bots dans le modèle qui peut être différente de celle
# de la vue.

WIDTH = 1800
HEIGHT = 1000

class Game_view:
    def __init__(self, model):

        pygame.init()
        self._window = pygame.display.set_mode((WIDTH, HEIGHT))
        
        self._model = model
        current_map = model.get_map()

        self._cell_size = min(WIDTH//current_map.get_width(), HEIGHT//current_map.get_height())

        self._mult_factor = self._cell_size/model.get_cell_size() # may find a better name latter



    def display(self):
        self._display_map()
        self._display_bots()
        
        pygame.display.flip()


    def _display_map(self):
        pygame.draw.rect(self._window, pygame.Color(255, 255, 255, 255), pygame.Rect(0, 0, WIDTH, HEIGHT))
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

                pygame.draw.rect(self._window, pygame.Color(r, g, b, a), current_rect)


    def _display_bots(self):
        bots = self._model.get_bots()

        for bot in bots:
            (r, g, b, a) = bot.get_color()
            
            bot_radius = int(bot.get_radius() * self._mult_factor)
            (x, y) = bot.get_coord()

            x *= self._mult_factor
            y *= self._mult_factor

            pygame.gfxdraw.aacircle(
                self._window,
                int(x),
                int(y),
                bot_radius,
                pygame.Color(r, g, b)
            )
