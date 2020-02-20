from domain.Player import Player
from domain.Map.RegularMap import RegularMap
from ai.pathFinding.PathFinder import PathFinder
from ai.pathFinding.aStar.Astar import Astar
from ai.pathFinding.aStar.NodeAstar import NodeAstar
from ai.pathFinding.base.Graph import Graph
from domain.Map import Map

from ai.bahavior_tree import *

import math
import random
from domain.GameObject.Block import *

def build_stupid_tree():
    root_node = Sequence()



class myPlayer(Player):
    
    def __init__(self, game_map, rules):
        self._map          = game_map
        self._rules        = rules
        self._pathFinder   = Astar(Graph(self.buildNodeList(), [], None))


        self._bot_data = dict()

    def buildNodeList(self):
        Nodelist = []
        for y in range(self._map["blockHeight"]):
            for x in range(self._map["blockWidth"]):
                    Nodelist.insert(
                        0,
                        NodeAstar(x, y, self._map["blocks"][x][y]))
        return Nodelist
    

    def distance(self,x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    


    def poll(self, pollingData):
        
