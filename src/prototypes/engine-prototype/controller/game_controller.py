import pygame, sys

from pygame.locals import *

class Game_controller:
    def __init__(self, model, view):
        self._model = model
        self._view = view

    def tick(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (x, y) = pygame.mouse.get_pos()
                x = int(x//self._view.get_mult_factor())
                y = int(y//self._view.get_mult_factor())


                if pygame.mouse.get_pressed()[0]:
                    self._model.mark_start_cell(x, y)
                    self._model.set_ai_destination(x, y)

                elif pygame.mouse.get_pressed()[2]:
                    self._model.mark_end_cell(x, y)
