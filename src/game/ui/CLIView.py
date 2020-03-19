from ui.View import View
from service.Config import Config

from math import (ceil, floor, radians, cos, sin)

class CLIView(View):
    """
    Implements the Game View using a command line interface.

    Attributes:
        model (Model)   : The data to represent.
        map (Map)       : The Map object from Model, for easier access.
    """

    def __init__(self, model):
        """ 
  
        Parameters: 
           model (Model): The data to represent.
        """
        
        self._model = model
        self._map = self._model.getMap()

        self.last_displayed_timer = None

        self.countdownEnd = False
        self.gameOverEnd = False

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
        
        if self._model.countdownremaining > 0:
            self._displayCountdown()
        elif not self.countdownEnd:
            self.countdownEnd = True
            print("Go!")
        if not self.gameOverEnd and self._model.winner != None:
            self._displayGameOver()
            self.gameOverEnd = True

    def _displayGameOver(self):
        """
        Displays the winner in the middle of the screen.
        """
        print("Red wins !" if self._model.winner == 1 else "Blue wins !")

    def _displayCountdown(self):
        """
        Displays the remaining countdown time in seconds in the middle of the screen.
        """
        toDisplay = "Starting in "+str(ceil(self._model.countdownremaining / 1000))

        if toDisplay != self.last_displayed_timer:
            self.last_displayed_timer = toDisplay
            print(toDisplay)