from ui.Controller import Controller
from ui.PygameView import PygameView

import pygame, sys

from pygame.locals import *

# Implements Controller
class PygameController(Controller):

    def __init__(self, model, view):
        self._model = model
        self._view =  view

    def tick(self, deltaTime):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # terminate player processes
                sys.exit()
        
            elif event.type == pygame.MOUSEMOTION:
                self._model.mouse_coords = pygame.mouse.get_pos()
                (x,y) = (self._model.mouse_coords[0],self._model.mouse_coords[1])
                self.current_mousex = int(x//self._view.get_mult_factor())
                self.current_mousey = int(y//self._view.get_mult_factor())

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self._view.debug_switch(PygameView.DEBUG_COLLISIONMAP)
                if event.key == pygame.K_z:
                    self._view.debug_switch(PygameView.DEBUG_CELL_COORDS)
                # if event.key == pygame.K_e:
                #     self._view.debug_switch(PygameView.DEBUG_VERTICES)
                # if event.key == pygame.K_r:
                #     self._view.debug_switch(PygameView.DEBUG_CORNERS)