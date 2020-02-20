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



def find_path_to_flag(dt, bot_id, pathFinder, bot_data):
    pathFinder.getPath((bot_data[bot_id]["current_position"]["x"], bot_data[bot_id]["current_position"]["y"]), bot_data["enemy_flag"])



def build_stupid_behavior(bot_id, bot_data, pathFinder):
    root_node = Sequence()




class myPlayer(Player):
    
    def __init__(self, game_map, rules, team):
        self._team         = team
        self._map          = game_map
        self._rules        = rules
        self._pathFinder   = Astar(Graph(self.buildNodeList(), [], None))

        self._init = True


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
        if self._init:
            for bot_id in pollingData["bots"]:
                self._bot_data[bot_id] = pollingData["bots"][bot_id]
                self._bot_data[bot_id]["behavior"] = build_stupid_behavior(bot_id, self._bot_data, self._pathFinder)

            for flag in pollingData["events"]["flags"]:
                if flag["team"] != 
            self._init = False
        
