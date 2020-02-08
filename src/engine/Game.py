from ui.PygameFactory import PygameFactory
from service.TimeManager import TimeManager
from service.Config import Config

from time import sleep

class Game:
    def __init__(self):
        Config.Initialize()
        uiFactory = PygameFactory()

        self.View       = uiFactory.getView()
        self.Controller = uiFactory.getController()


    def gameLoop(self):
        print("Game starting")
        
        running = True

        runningStopwatch = TimeManager()
        runningStopwatch.StartTimer()

        while running:

            deltaTime = runningStopwatch.NextFrame()
                
            runningStopwatch.Mark()

            self.Controller.tick(deltaTime)
            self.View.tick(deltaTime)

            # running = False # Game over

        runningStopwatch.StopTimer()

        print("Game closing")
        pass