import sys
import os
import io

import unittest

PACKAGE_PARENT = '../game'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from domain.Player import Player
from model.GameModel import GameModel
from service.Config import Config
from service.Ruleset import Ruleset
from service.TimeManager import TimeManager

class myPlayer(Player):

    def __init__(self, map, rules, team):
        pass

    def poll(self, pollingData):
        pass

class TestGameModel(unittest.TestCase):

    def __init__(self, methodName):
        super().__init__(methodName)

    # Need to run this first to init the Model we test
    def test__init(self):
        Config.Initialize()
        Ruleset.Initialize()
        
        TestGameModel.Model = GameModel(myPlayer, myPlayer, 'game/maps/test_map.txt')

        # Override the model stopwatch to test reaction to time
        def getTimeMs(self):
            return self.overriden_time
        
        TimeManager.GetTimeMs = getTimeMs
        TimeManager.overriden_time = 0

        TestGameModel.Model.stopwatch = TimeManager()

        assert(TestGameModel.Model.turn == 0)

    def test_start(self):
        TimeManager.overriden_time = 1000
        TestGameModel.Model.tick(1000)

        assert(TestGameModel.Model.turn == -1)

        TimeManager.overriden_time = 5000
        TestGameModel.Model.tick(4000)

        assert(TestGameModel.Model.turn == 1)

        TimeManager.overriden_time = 5000

        # suppress stdout because 1ms tick will print errors from players
        # they do not have to respond, it doesn't change anything.
        save_stdout = sys.stdout
        sys.stdout = io.StringIO()
        TestGameModel.Model.tick(1)
        sys.stdout = save_stdout

        assert(TestGameModel.Model.turn == 2)

    # Need to run this a the end to stop player Processes (or it hangs)
    def testend(self):
        TestGameModel.Model.stop()

        assert(True)