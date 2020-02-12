from model.Model import Model
from service.Ruleset import Ruleset
from domain.Map import *
from copy import deepcopy

# Implements Model to be used by the Game Engine
class GameModel(Model):

    def __init__(self, Player1, Player2):
        mapData = RegularMap.loadMapData('./maps/map_00.txt')
        self._map = RegularMap(mapData)

        self._ruleset = Ruleset.GetRuleset()

        self._players = list()

        #### Implementation Simu ####
        try:
            self._players.append(Player1(deepcopy(mapData), deepcopy(self._ruleset)))
        except:
            print("Player 1 can't be evaluated because it failed to initialize")

        try:
            self._players.append(Player2(deepcopy(mapData), deepcopy(self._ruleset)))
        except:
            print("Player 2 can't be evaluated because it failed to initialize")
        ####
        

    def tick(self, deltaTime):
        pass

    def register(self, player):
        pass