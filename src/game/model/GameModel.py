from model.Model import Model
from domain.Map import *

# Implements Model to be used by the Game Engine
class GameModel(Model):

    def __init__(self):
        mapData = RegularMap.loadMapData('./maps/map_00.txt')
        self._map = RegularMap(mapData)

        self._players = list()

        

    def tick(self, deltaTime):
        pass

    def register(self, player):
        pass