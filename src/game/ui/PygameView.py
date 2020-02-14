from ui.View import View
from service.Config import Config

import pygame
import pygame.gfxdraw
from pygame.locals import *

from math import (ceil, floor, radians, cos, sin)

# Implements View using pygame
class PygameView(View):

    def __init__(self, model):

        pygame.init()
        self._window = pygame.display.set_mode((Config.ResolutionWidth(), Config.ResolutionHeight()))
        self._surface = pygame.Surface((Config.ResolutionWidth(), Config.ResolutionHeight()), pygame.SRCALPHA)
        
        self._model = model
        self._map = self._model.getMap()

        self._cell_size = min(Config.ResolutionWidth()//self._map.blockWidth, Config.ResolutionHeight()//self._map.blockHeight)

        self._mult_factor = self._cell_size/self._map.BLOCKSIZE

        self._display_map()


    def get_mult_factor(self):
        return self._mult_factor

    def tick(self, deltaTime):
        self._display()
        pass

    def _display(self):
        self._surface.fill((0, 0, 0, 0))
        #self._display_map() # a desactiver si opti 
        self._display_bots()
        
        self._window.blit(self._surface, (0, 0))
        pygame.display.flip()



    def _display_map(self):
        pygame.draw.rect(self._window, pygame.Color(255, 255, 255, 255), pygame.Rect(0, 0, Config.ResolutionWidth(), Config.ResolutionHeight()))
        
        self._display_tiles(0,0,self._map.blockWidth - 1,self._map.blockHeight - 1)


    def _display_tiles(self, start_x, start_y, end_x, end_y):
        for y in range(start_y, end_y + 1):
            for x in range(start_x, end_x + 1):
                current_rect = pygame.Rect(
                    x * self._cell_size,
                    y * self._cell_size,
                    self._cell_size,
                    self._cell_size
                )
                
                (r, g, b, a) = self._map.blocks[x][y].color

                pygame.draw.rect(self._window, pygame.Color(r, g, b, a), current_rect)


    def _display_bots(self):
        bots = self._model.getBots()

        tiles_to_refresh = dict()

        for bot_id in bots.keys():  
            bot = bots[bot_id]  
            x_tile = int(bot.x // self._map.BLOCKSIZE)
            y_tile = int(bot.y // self._map.BLOCKSIZE)

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
                if(end_x >= self._map.blockWidth):
                    end_x = self._map.blockWidth - 1
                if(end_y >= self._map.blockHeight):
                    end_y = self._map.blockHeight - 1

                self._display_tiles(start_x,start_y,end_x,end_y)

        for bot_id in bots.keys():  
            bot = bots[bot_id] 
            (r, g, b, a) = bot.color
            
            bot_radius = int(bot.radius * self._mult_factor)
            (x, y) = (bot.x, bot.y)

            x *= self._mult_factor
            y *= self._mult_factor

            self._draw_cone(
                x,
                y, 
                pygame.Color(r, g, b, 70),
                10 * bot_radius,
                int(bot.angle - 20),
                int(bot.angle + 20),
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
                    int(x + cos(radians(bot.angle)) * 1.5 * bot_radius),
                    int(y + sin(radians(bot.angle)) * 1.5 * bot_radius)
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

