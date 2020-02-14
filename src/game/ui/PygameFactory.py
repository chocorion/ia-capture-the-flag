from ui.UiFactory import UiFactory

from ui.PygameController import PygameController
from ui.PygameView import PygameView

class PygameFactory(UiFactory):
    class __PygameFactory(UiFactory):
        def __init__(self, model):
            super().__init__()
            self.controller = PygameController()
            self.view = PygameView(model)

        def getController(self):
            return self.controller

        def getView(self):
            return self.view

    Instance = None

    def __new__(self, model):
        if not PygameFactory.Instance:
            PygameFactory.Instance = PygameFactory.__PygameFactory(model)

        return PygameFactory.Instance

    
    def getController(self):
        return PygameFactory.Instance.getController()
        
    def getView(self):
        return PygameFactory.Instance.getView()