import pygame
import pygame.gfxdraw
from pygame.locals import *

from model.map import *
from model.blocks import *

from math import (ceil, floor, radians, cos, sin)
import sys

# Faire attention à comment gérer la taille des bots dans le modèle qui peut être différente de celle
# de la vue.

WIDTH = 1800
HEIGHT = 1000

class Game_view:
    def __init__(self, model):

        pygame.init()
        self._window = pygame.display.set_mode((WIDTH, HEIGHT))
        self._surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        self._model = model
        current_map = model.get_map()

        self._cell_size = min(WIDTH//current_map.get_width(), HEIGHT//current_map.get_height())

        self._mult_factor = self._cell_size/model.get_cell_size() # may find a better name latter

        self._display_map()


    def tick(self, dt):
        self._display()

    def _display(self):
        # self._display_map()
        self._display_bots()
        
        self._window.blit(self._surface, (0, 0))
        pygame.display.flip()
        self._surface.fill((0, 0, 0, 0))



    def _display_map(self):
        pygame.draw.rect(self._window, pygame.Color(255, 255, 255, 255), pygame.Rect(0, 0, WIDTH, HEIGHT))

        current_map = self._model.get_map()
        
        self._display_tiles(0,0,current_map.get_width() - 1,current_map.get_height() - 1)


    def _display_tiles(self, start_x, start_y, end_x, end_y):
        current_map = self._model.get_map() # Store it as attribute ?

        for y in range(start_y, end_y + 1):
            for x in range(start_x, end_x + 1):
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
        current_map = self._model.get_map()

        tiles_to_refresh = dict()

        for bot in bots:
            (x, y) = bot.get_coord()

            x_tile = int(x // self._model.get_cell_size())
            y_tile = int(y // self._model.get_cell_size())

            if not x_tile in tiles_to_refresh.keys():
                tiles_to_refresh[x_tile] = dict()
            tiles_to_refresh[x_tile][y_tile] = 1

        for x_tile in tiles_to_refresh.keys():
            for y_tile in tiles_to_refresh[x_tile].keys():

                start_x = x_tile - 4
                start_y = y_tile - 4
                end_x = x_tile + 4
                end_y = y_tile + 4

                if(start_x < 0):
                    start_x = 0
                if(start_y < 0):
                    start_y = 0
                if(end_x >= current_map._width):
                    end_x = current_map._width - 1
                if(end_y >= current_map._height):
                    end_y = current_map._height - 1

                self._display_tiles(start_x,start_y,end_x,end_y)

        for bot in bots:
            (r, g, b, a) = bot.get_color()
            
            bot_radius = int(bot.get_radius() * self._mult_factor)
            (x, y) = bot.get_coord()

            x *= self._mult_factor
            y *= self._mult_factor

            self._draw_cone(
                x,
                y, 
                pygame.Color(r, g, b, 70),
                10 * bot_radius,
                int(bot.get_angle() - 20),
                int(bot.get_angle() + 20),
                10
            )

            pygame.gfxdraw.aacircle(
                self._window,
                int(x),
                int(y),
                bot_radius,
                pygame.Color(r, g, b)
            )

            pygame.draw.line(
                self._window,
                pygame.Color(r, g, b),
                (int(x), int(y)),
                (
                    int(x + cos(radians(bot.get_angle())) * 1.5 * bot_radius),
                    int(y + sin(radians(bot.get_angle())) * 1.5 * bot_radius)
                )
            )

    def _draw_cone(self, x, y, color, length, angle_start, angle_end, step = 1):
        angle_start = float(angle_start)
        angle_end = float (angle_end)

        angle_step = 0 if step <= 0 else (angle_end -  angle_start)/step

        points = [(x, y), (x + cos(radians(angle_start)) * length, y + sin(radians(angle_start)) * length)]

        for i in range(step):
            points.append(
                (x + cos(radians(angle_start + angle_step * i)) * length, y + sin(radians(angle_start + angle_step * i)) * length)
            )

        points.append((x + cos(radians(angle_end)) * length, y + sin(radians(angle_end)) * length))
        points.append((x, y))

        pygame.draw.polygon(
            self._surface,
            color,
            points
        )


