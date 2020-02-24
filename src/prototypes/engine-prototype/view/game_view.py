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

        self._cellSize = min(WIDTH//current_map.get_width(), HEIGHT//current_map.get_height())

        self._multFactor = self._cellSize/model.get_cellSize() # may find a better name latter

        self._displayMap()


    def getMultFactor(self):
        return self._multFactor

    def tick(self, dt):
        self._display()

    def _display(self):
        #self._displayMap() # a desactiver si opti 
        self._displayBots()
        
        self._window.blit(self._surface, (0, 0))
        pygame.display.flip()
        self._surface.fill((0, 0, 0, 0))



    def _displayMap(self):
        pygame.draw.rect(self._window, pygame.Color(255, 255, 255, 255), pygame.Rect(0, 0, WIDTH, HEIGHT))

        current_map = self._model.get_map()
        
        self._displayTiles(0,0,current_map.get_width() - 1,current_map.get_height() - 1)


    def _displayTiles(self, startX, startY, endX, endY):
        current_map = self._model.get_map() # Store it as attribute ?

        for y in range(startY, endY + 1):
            for x in range(startX, endX + 1):
                currentRect = pygame.Rect(
                    x * self._cellSize,
                    y * self._cellSize,
                    self._cellSize,
                    self._cellSize
                )

                (r, g, b, a) = current_map.get_tile(x, y).getColor()

                pygame.draw.rect(self._window, pygame.Color(r, g, b, a), currentRect)


    def _displayBots(self):
        bots = self._model.get_bots()
        current_map = self._model.get_map()

        tilesToRefresh = dict()

        for bot in bots:
            (x, y) = bot.get_coord()

            xTile = int(x // self._model.get_cellSize())
            yTile = int(y // self._model.get_cellSize())

            if not xTile in tilesToRefresh.keys():
                tilesToRefresh[xTile] = dict()
            tilesToRefresh[xTile][yTile] = 1

        for xTile in tilesToRefresh.keys():
            for yTile in tilesToRefresh[xTile].keys():

                startX = xTile - 4
                startY = yTile - 4
                endX = xTile + 4
                endY = yTile + 4

                if(startX < 0):
                    startX = 0
                if(startY < 0):
                    startY = 0
                if(endX >= current_map._width):
                    endX = current_map._width - 1
                if(endY >= current_map._height):
                    endY = current_map._height - 1

                self._displayTiles(startX,startY,endX,endY)

        for bot in bots:
            (r, g, b, a) = bot.getColor()
            
            botRadius = int(bot.get_radius() * self._multFactor)
            (x, y) = bot.get_coord()

            x *= self._multFactor
            y *= self._multFactor

            self._drawCone(
                x,
                y, 
                pygame.Color(r, g, b, 70),
                10 * botRadius,
                int(bot.get_angle() - 20),
                int(bot.get_angle() + 20),
                10
            )

            pygame.gfxdraw.aacircle(
                self._window,
                int(x),
                int(y),
                botRadius,
                pygame.Color(r, g, b)
            )

            pygame.draw.line(
                self._window,
                pygame.Color(r, g, b),
                (int(x), int(y)),
                (
                    int(x + cos(radians(bot.get_angle())) * 1.5 * botRadius),
                    int(y + sin(radians(bot.get_angle())) * 1.5 * botRadius)
                )
            )

    def _drawCone(self, x, y, color, length, angleStart, angleEnd, step = 1):
        angleStart = float(angleStart)
        angleEnd = float (angleEnd)

        angleStep = 0 if step <= 0 else (angleEnd -  angleStart)/step

        points = [(x, y), (x + cos(radians(angleStart)) * length, y + sin(radians(angleStart)) * length)]

        for i in range(step):
            points.append(
                (x + cos(radians(angleStart + angleStep * i)) * length, y + sin(radians(angleStart + angleStep * i)) * length)
            )

        points.append((x + cos(radians(angleEnd)) * length, y + sin(radians(angleEnd)) * length))
        points.append((x, y))

        pygame.draw.polygon(
            self._surface,
            color,
            points
        )


