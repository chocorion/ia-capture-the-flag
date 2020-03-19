from ui.Controller import Controller
from ui.CLIView import CLIView

class CLIController(Controller):

    def __init__(self, model, view):
        self._model = model
        self._model.mouseCoords = (0,0)
        self._view =  view

    def tick(self, deltaTime):
        pass