#! /usr/bin/env python3

from ui.PygameFactory import PygameFactory
from model import *
from service.TimeManager import TimeManager
from service.Config import Config

from time import sleep

class Game:
    def __init__(self):
        Config.Initialize()
        uiFactory = PygameFactory()

        self.View       = uiFactory.getView()
        self.Controller = uiFactory.getController()
        self.Model      = GameModel()


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

# Make this an executable file
if __name__ == "__main__":
    game = Game()
    game.gameLoop() 