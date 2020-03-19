from ui.UiFactory import UiFactory

from ui.CLIController import CLIController
from ui.CLIView import CLIView

class CLIFactory(UiFactory):
    class __CLIFactory(UiFactory):
        def __init__(self, model):
            super().__init__()
            self.view = CLIView(model)
            self.controller = CLIController(model, self.view)

        def getController(self):
            return self.controller

        def getView(self):
            return self.view

    Instance = None

    def __new__(self, model):
        if not CLIFactory.Instance:
            CLIFactory.Instance = CLIFactory.__CLIFactory(model)

        return CLIFactory.Instance

    
    def getController(self):
        return CLIFactory.Instance.getController()
        
    def getView(self):
        return CLIFactory.Instance.getView()