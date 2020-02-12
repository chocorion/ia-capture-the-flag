from model.Model import Model
from domain.Map import *

# Implements Model to be used by the Game Engine
class GameModel(Model):

    def __init__(self):
        mapData = RegularMap.loadMapData('./maps/map_00.txt')
        self.map = RegularMap(mapData)

    def tick(self, deltaTime):
        pass

    def register(self, player):
        pass