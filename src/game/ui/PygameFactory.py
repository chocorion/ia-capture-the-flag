from ui.UiFactory import UiFactory

from ui.PygameController import PygameController
from ui.PygameView import PygameView

class PygameFactory(UiFactory):
    class __PygameFactory(UiFactory):
        def __init__(self):
            super().__init__()
            self.controller = PygameController()
            self.view = PygameView()

        def getController(self):
            return self.controller

        def getView(self):
            return self.view

    Instance = None

    def __new__(self):
        if not PygameFactory.Instance:
            PygameFactory.Instance = PygameFactory.__PygameFactory()

        return PygameFactory.Instance

    
    def getController(self):
        return PygameFactory.Instance.getController()
        
    def getView(self):
        return PygameFactory.Instance.getView()