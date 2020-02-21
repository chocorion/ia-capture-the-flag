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

    DEBUG_COLLISIONMAP = 0
    DEBUG_CELL_COORDS = 1

    def __init__(self, model):
        """ 
        The constructor for PygameView.

        Stores necessary objects as attributes and computes different values used for displaying.
  
        Parameters: 
           model (Model): The data to represent.
        """
        
        self._model = model
        self._map = self._model.getMap()

        self._cellSize = min(Config.ResolutionWidth()//self._map.blockWidth, Config.ResolutionHeight()//self._map.blockHeight + 1)

        pygame.init()

        self._defaultFontSmall = pygame.font.Font(pygame.font.get_default_font(), 24) 
        self._default_font_big = pygame.font.Font(pygame.font.get_default_font(), 64) 
        self._defaultFontBigOutline = pygame.font.Font(pygame.font.get_default_font(), 64) 

        self._windowRect = (self._map.blockWidth * self._cellSize, self._map.blockHeight * self._cellSize)

        self._window = pygame.display.set_mode(self._windowRect)
        self._surface = pygame.Surface(self._windowRect, pygame.SRCALPHA)

        self._multFactor = self._cellSize/self._map.BLOCKSIZE

        self._refreshMap = True

        self.last_displayed_timer = None
        self.last_displayed_aimed = None

        self.countdownEnd = None

        self.debug = [False]*2


    def get_mult_factor(self):
        """ 
        Getter for multFactor.

        The multiplication factor is used by the controller to determine the location of a block from a real coordinate.
  
        Returns: 
           multFactor (double): Cellsize / Blocksize, computed during init.
        """
        return self._multFactor

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

        if self._refreshMap or self.debug[PygameView.DEBUG_COLLISIONMAP]:
            self._refreshMap = False

            self._displayMap() 
                
        self._displayBots()
        self._displayFlags()
        self._displayCountdown()

        if self.debug[PygameView.DEBUG_COLLISIONMAP]:
            self.displayCollisionMap("RegularBot")

        if self.debug[PygameView.DEBUG_CELL_COORDS]:
            self.displayAimed()

        self._window.blit(self._surface, (0, 0))
        pygame.display.flip()



    def _displayMap(self):
        """ 
        Clears the window and draws all map blocks on screen.
        """
        pygame.draw.rect(self._window, pygame.Color(255, 255, 255, 255), pygame.Rect(0, 0, Config.ResolutionWidth(), Config.ResolutionHeight()))
        
        self._displayTiles(0,0,self._map.blockWidth - 1,self._map.blockHeight - 1)

    def _displayCountdown(self):
        """
        Displays the remaining countdown time in seconds in the middle of the screen.
        """
        if self._model.cooldownremaining > 0:
            self.countdownEnd = False
            toDisplay = ceil(self._model.cooldownremaining / 1000)

            # refresh timer surface only if it changes
            if self.last_displayed_timer != toDisplay: 
                toDisplay = '{}'.format(toDisplay)
                self.lastDisplayedTimerText = self._default_font_big.render(toDisplay, True, (255,0,255,255))

                self.lastDisplayedTimerTextOutline = self._defaultFontBigOutline.render(toDisplay, True, (0,0,0,255))

                # TODO: refactor
                self.lastDisplayedTimerTextRect = self.lastDisplayedTimerText.get_rect()
                self.lastDisplayedTimerTextOutlineRect1 = self.lastDisplayedTimerText.get_rect()
                self.lastDisplayedTimerTextOutlineRect2 = self.lastDisplayedTimerText.get_rect()
                self.lastDisplayedTimerTextOutlineRect3 = self.lastDisplayedTimerText.get_rect()
                self.lastDisplayedTimerTextOutlineRect4 = self.lastDisplayedTimerText.get_rect()
                self.lastDisplayedTimerTextOutlineRect5 = self.lastDisplayedTimerText.get_rect()
                self.lastDisplayedTimerTextOutlineRect6 = self.lastDisplayedTimerText.get_rect()
                self.lastDisplayedTimerTextOutlineRect7 = self.lastDisplayedTimerText.get_rect()
                self.lastDisplayedTimerTextOutlineRect8 = self.lastDisplayedTimerText.get_rect()

                self.lastDisplayedTimerTextRect.center = (self._windowRect[0] // 2, self._windowRect[1] // 2)

                outlineMargin = 5
                self.lastDisplayedTimerTextOutlineRect1.center = (self._windowRect[0] // 2 + outlineMargin, self._windowRect[1] // 2)
                self.lastDisplayedTimerTextOutlineRect2.center = (self._windowRect[0] // 2, self._windowRect[1] // 2 + outlineMargin)
                self.lastDisplayedTimerTextOutlineRect3.center = (self._windowRect[0] // 2 - outlineMargin, self._windowRect[1] // 2)
                self.lastDisplayedTimerTextOutlineRect4.center = (self._windowRect[0] // 2, self._windowRect[1] // 2 - outlineMargin)
                self.lastDisplayedTimerTextOutlineRect5.center = (self._windowRect[0] // 2 + outlineMargin, self._windowRect[1] // 2 + outlineMargin)
                self.lastDisplayedTimerTextOutlineRect6.center = (self._windowRect[0] // 2 + outlineMargin, self._windowRect[1] // 2 - outlineMargin)
                self.lastDisplayedTimerTextOutlineRect7.center = (self._windowRect[0] // 2 - outlineMargin, self._windowRect[1] // 2 + outlineMargin)
                self.lastDisplayedTimerTextOutlineRect8.center = (self._windowRect[0] // 2 - outlineMargin, self._windowRect[1] // 2 - outlineMargin)

            # TODO: refactor
            self._window.blit(self.lastDisplayedTimerTextOutline, self.lastDisplayedTimerTextOutlineRect1)
            self._window.blit(self.lastDisplayedTimerTextOutline, self.lastDisplayedTimerTextOutlineRect2)
            self._window.blit(self.lastDisplayedTimerTextOutline, self.lastDisplayedTimerTextOutlineRect3)
            self._window.blit(self.lastDisplayedTimerTextOutline, self.lastDisplayedTimerTextOutlineRect4)
            self._window.blit(self.lastDisplayedTimerTextOutline, self.lastDisplayedTimerTextOutlineRect5)
            self._window.blit(self.lastDisplayedTimerTextOutline, self.lastDisplayedTimerTextOutlineRect6)
            self._window.blit(self.lastDisplayedTimerTextOutline, self.lastDisplayedTimerTextOutlineRect7)
            self._window.blit(self.lastDisplayedTimerTextOutline, self.lastDisplayedTimerTextOutlineRect8)
            self._window.blit(self.lastDisplayedTimerText, self.lastDisplayedTimerTextRect)
            self._refreshMap = True
        elif not self.countdownEnd:
            self.countdownEnd = True
            self._refreshMap = True
            
    def displayCollisionMap(self, name):
        """
        Displays a collision map.

        Parameters:
            name (string) : The identifier of this collision map. Example: "RegularBot"
        """
        try:

            self._window.blit(self.collisionSurface, (0, 0))
        except:
            collisionMap = self._model.getEngine().collisionsMaps[name]
            divider = self._model.getEngine().collisionsMapsDividers[name]

            self.collisionSurface = pygame.Surface(self._windowRect, pygame.SRCALPHA)

            (x,y) = (0,0)
            for line in collisionMap:
                for dot in line:
                    if dot:

                        currentRect = pygame.Rect(
                            int(x * self._cellSize // divider),
                            int(y * self._cellSize // divider),
                            round(self._cellSize / divider),
                            round(self._cellSize / divider)
                        )
                        
                        (r, g, b, a) = (255,0,0,60)

                        pygame.draw.rect(self.collisionSurface, pygame.Color(r, g, b, a), currentRect)
                    y += 1
                x += 1
                y = 0
            

    def displayAimed(self):
        """
        DEBUG: Displays the coordinates of the currently hovered block.
        """
        # refresh aimed cell only if changed
        toDisplay = (self._model.mouseCoords[0] // self._cellSize,self._model.mouseCoords[1] // self._cellSize)

        if self.last_displayed_aimed != toDisplay: 
            toDisplay = '(x{},y{})'.format(toDisplay[0],toDisplay[1])
            self.last_displayed_aimed_text = self._defaultFontSmall.render(toDisplay, True, (0,0,0,255))
            self._refreshMap = True

        self._window.blit(self.last_displayed_aimed_text, self.last_displayed_aimed_text.get_rect())


    def _displayTiles(self, startX, startY, endX, endY):
        """ 
        Draws map blocks contained in a rectangle selection.
  
        Parameters: 
           startX (int): Top-left block X of the selection, X coordinate in blocks.
           startY (int): Top-left block Y of the selection, Y coordinate in blocks.
           endX (int): Bottom-right block of the selection, X coordinate in blocks.
           endY (int): Bottom-right block of the selection, Y coordinate in blocks.
        """
        for y in range(startY, endY + 1):
            for x in range(startX, endX + 1):
                currentRect = pygame.Rect(
                    x * self._cellSize,
                    y * self._cellSize,
                    self._cellSize,
                    self._cellSize
                )
                
                (r, g, b, a) = self._map.blocks[x][y].color

                pygame.draw.rect(self._window, pygame.Color(r, g, b, a), currentRect)

    def _displayFlags(self):
        """
        Draws flags. 

        Use only on a map that has flags.
        """

        for flag in self._map.flags:
            currentRect = pygame.Rect(
                flag.x * self._multFactor - (self._cellSize - flag.width * self._multFactor)//2,
                flag.y * self._multFactor - (self._cellSize - flag.height * self._multFactor)//2,
                flag.width * self._multFactor,
                flag.height * self._multFactor
            )
                
            (r, g, b, a) = flag.color
            pygame.draw.rect(self._window, pygame.Color(r, g, b, a), currentRect)

    def _displayBots(self):
        """ 
        Draws every bot from the model and updates their adjacent tiles as well.
        """
        bots = self._model.getBots()

        tilesToRefresh = dict()

        for botId in bots.keys():  
            bot = bots[botId]  
            xTile = int(bot.x // self._map.BLOCKSIZE)
            yTile = int(bot.y // self._map.BLOCKSIZE)

            if not xTile in tilesToRefresh.keys():
                tilesToRefresh[xTile] = dict()
            tilesToRefresh[xTile][yTile] = 1

        for xTile in tilesToRefresh.keys():
            for yTile in tilesToRefresh[xTile].keys():

                startX = xTile - 5
                startY = yTile - 5
                endX = xTile + 5
                endY = yTile + 5

                if(startX < 0):
                    startX = 0
                if(startY < 0):
                    startY = 0
                if(endX >= self._map.blockWidth):
                    endX = self._map.blockWidth - 1
                if(endY >= self._map.blockHeight):
                    endY = self._map.blockHeight - 1

                self._displayTiles(startX,startY,endX,endY)

        for botId in bots.keys():  
            bot = bots[botId] 
            (r, g, b, a) = bot.color
            
            botRadius = int(bot.radius * self._multFactor)
            (x, y) = (bot.x, bot.y)

            x *= self._multFactor
            y *= self._multFactor

            self._drawCone(
                x,
                y, 
                pygame.Color(r, g, b, 70),
                bot.viewDistance * 2,
                int(bot.angle - bot.fov),
                int(bot.angle + bot.fov),
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
                    int(x + cos(radians(bot.angle)) * 1.5 * botRadius),
                    int(y + sin(radians(bot.angle)) * 1.5 * botRadius)
                )
            )

    def _drawCone(self, x, y, color, length, angleStart, angleEnd, step = 1):
        """ 
        Draws a cone.
  
        Parameters: 
           x (int): The screen x coordinate.
           y (int): The screen y coordinate.
           color (r,g,b,a): RGBA tuple.
           length (int): The diameter of the circle containing the cone.
           angleStart (int): The angle at which the cone starts within the circle.
           angleEnd (int): The angle at which the cone ends within the circle.
           step (int): The done is made of triangles, a lower step makes a more precise curve.
        """
        angleStart = float(angleStart)
        angleEnd = float (angleEnd)

        angleStep = 0 if step <= 0 else (angleEnd -  angleStart)/step

        oldX = x
        oldY = y

        x = length
        y = length

        points = [(x, y), (x + cos(radians(angleStart)) * length, y + sin(radians(angleStart)) * length)]

        for i in range(step):
            points.append(
                (x + cos(radians(angleStart + angleStep * i)) * length, y + sin(radians(angleStart + angleStep * i)) * length)
            )

        points.append((x + cos(radians(angleEnd)) * length, y + sin(radians(angleEnd)) * length))
        points.append((x, y))

        self.coneSurface = pygame.Surface((length * 2, length * 2), pygame.SRCALPHA)

        pygame.draw.polygon(
            self.coneSurface,
            color,
            points
        )

        self._window.blit(self.coneSurface, (oldX - length, oldY - length))


    def debug_switch(self, debugmode):
        self.debug[debugmode] = not self.debug[debugmode]
        self._refreshMap = True