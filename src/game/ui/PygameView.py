from ui.View import View
from service.Config import Config

import pygame
import pygame.gfxdraw
from pygame.locals import *

from math import (ceil, floor, radians, cos, sin)

# Implements View using pygame
class PygameView(View):
    """
    Implements the Game View using the Pygame library.

    Attributes:
        model (Model)   : The data to represent.
        map (Map)       : The Map object from Model, for easier access.
    """

    def __init__(self, model):
        """ 
        The constructor for PygameView.

        Stores necessary objects as attributes and computes different values used for displaying.
  
        Parameters: 
           model (Model): The data to represent.
        """
        
        self._model = model
        self._map = self._model.getMap()

        self._cell_size = min(Config.ResolutionWidth()//self._map.blockWidth, Config.ResolutionHeight()//self._map.blockHeight + 1)

        pygame.init()
        self._window = pygame.display.set_mode((self._map.blockWidth * self._cell_size, self._map.blockHeight * self._cell_size))
        self._surface = pygame.Surface((self._map.blockWidth * self._cell_size, self._map.blockHeight * self._cell_size), pygame.SRCALPHA)

        self._mult_factor = self._cell_size/self._map.BLOCKSIZE

        self._display_map()


    def get_mult_factor(self):
        """ 
        Getter for mult_factor.

        The multiplication factor is used by the controller to determine the location of a block from a real coordinate.
  
        Returns: 
           mult_factor (double): Cellsize / Blocksize, computed during init.
        """
        return self._mult_factor

    def tick(self, deltaTime):
        """ 
        Called each tick to refresh the View.
  
        Parameters: 
           deltaTime (int): The time in milliseconds since the last call to this function.
        """
        self._display()

    def _display(self):
        """ 
        Updates the window with the current representation of the game.
        """
        self._surface.fill((0, 0, 0, 0))
        #self._display_map() # a desactiver si opti 
        self._display_bots()
        self._display_flags()
        
        self._window.blit(self._surface, (0, 0))
        pygame.display.flip()



    def _display_map(self):
        """ 
        Clears the window and draws all map blocks on screen.
        """
        pygame.draw.rect(self._window, pygame.Color(255, 255, 255, 255), pygame.Rect(0, 0, Config.ResolutionWidth(), Config.ResolutionHeight()))
        
        self._display_tiles(0,0,self._map.blockWidth - 1,self._map.blockHeight - 1)


    def _display_tiles(self, start_x, start_y, end_x, end_y):
        """ 
        Draws map blocks contained in a rectangle selection.
  
        Parameters: 
           start_x (int): Top-left block X of the selection, X coordinate in blocks.
           start_y (int): Top-left block Y of the selection, Y coordinate in blocks.
           end_x (int): Bottom-right block of the selection, X coordinate in blocks.
           end_y (int): Bottom-right block of the selection, Y coordinate in blocks.
        """
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

    def _display_flags(self):
        """
        Draws flags. 

        Use only on a map that has flags.
        """

        for flag in self._map.flags:
            current_rect = pygame.Rect(
                flag.x * self._mult_factor - (self._cell_size - flag.width * self._mult_factor)//2,
                flag.y * self._mult_factor - (self._cell_size - flag.height * self._mult_factor)//2,
                flag.width * self._mult_factor,
                flag.height * self._mult_factor
            )
                
            (r, g, b, a) = flag.color
            pygame.draw.rect(self._window, pygame.Color(r, g, b, a), current_rect)

    def _display_bots(self):
        """ 
        Draws every bot from the model and updates their adjacent tiles as well.
        """
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

                start_x = x_tile - 5
                start_y = y_tile - 5
                end_x = x_tile + 5
                end_y = y_tile + 5

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
                bot.view_distance * 2,
                int(bot.angle - bot.fov),
                int(bot.angle + bot.fov),
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
        """ 
        Draws a cone.
  
        Parameters: 
           x (int): The screen x coordinate.
           y (int): The screen y coordinate.
           color (r,g,b,a): RGBA tuple.
           length (int): The diameter of the circle containing the cone.
           angle_start (int): The angle at which the cone starts within the circle.
           angle_end (int): The angle at which the cone ends within the circle.
           step (int): The done is made of triangles, a lower step makes a more precise curve.
        """
        angle_start = float(angle_start)
        angle_end = float (angle_end)

        angle_step = 0 if step <= 0 else (angle_end -  angle_start)/step

        old_x = x
        old_y = y

        x = length
        y = length

        points = [(x, y), (x + cos(radians(angle_start)) * length, y + sin(radians(angle_start)) * length)]

        for i in range(step):
            points.append(
                (x + cos(radians(angle_start + angle_step * i)) * length, y + sin(radians(angle_start + angle_step * i)) * length)
            )

        points.append((x + cos(radians(angle_end)) * length, y + sin(radians(angle_end)) * length))
        points.append((x, y))

        self.cone_surface = pygame.Surface((length * 2, length * 2), pygame.SRCALPHA)

        pygame.draw.polygon(
            self.cone_surface,
            color,
            points
        )

        self._window.blit(self.cone_surface, (old_x - length, old_y - length))

