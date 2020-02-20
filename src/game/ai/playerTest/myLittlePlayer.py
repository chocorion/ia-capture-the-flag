from domain.Player import Player
from domain.Map.RegularMap import RegularMap

from ai.pathFinding.PathFinder import PathFinder
from ai.pathFinding.aStar.Astar import Astar
from ai.pathFinding.aStar.NodeAstar import NodeAstar
from ai.pathFinding.base.Graph import Graph

from domain.Map import Map

from ai.behavior_tree import *

import math
import random
from domain.GameObject.Block import *

NodeResultToString = {
    NodeTree.RUNNING: "RUNNING",
    NodeTree.SUCCESS: "SUCCESS",
    NodeTree.FAILURE: "FAILURE"
}

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def points_distance(p1, p2):
    return distance(p1[0], p1[1], p2[0], p2[1])

class myPlayer(Player):
    
    def __init__(self, game_map, rules, team):
        self._team         = team
        self._map          = game_map
        self._rules        = rules
        self._pathFinder   = Astar(Graph(self.buildNodeList(), [], None))

        self._init = True


        self._bot_data = {"bots": dict()}


    def buildNodeList(self):
        Nodelist = []
        for y in range(self._map["blockHeight"]):
            for x in range(self._map["blockWidth"]):
                    Nodelist.insert(
                        0,
                        NodeAstar(x, y, self._map["blocks"][x][y]))
        return Nodelist
    
    def build_response(self):
        response = {"bots": dict()}

        for bot_id in self._bot_data["bots"].keys():
            dest = self._bot_data["bots"][bot_id]["destination"]

            response["bots"][bot_id] = {
                "target_position": (dest[0], dest[1], 100),
                "actions": 0
            }

        return response

    def poll(self, pollingData):
        if self._init:
            
            for bot_id in pollingData["bots"]:
                self._bot_data["bots"][bot_id] = pollingData["bots"][bot_id]
                self._bot_data["bots"][bot_id]["behavior"] = self.build_stupid_bot_behavior(bot_id)

            for flag in pollingData["events"]["flags"]:
                if flag["team"] != self._team:
                    self._bot_data["enemy_flag"] = flag["position"]
            
            self._init = False

        for bot_id in self._bot_data["bots"].keys():
            result = self._bot_data["bots"][bot_id]["behavior"].tick(0)
            print("bot_id {} -> {}".format(bot_id, NodeResultToString[result]))

        return self.build_response()


    ###########################################################
    # Bot behavior part
    #######################

    def bot_fun_find_path_to_flag(self, bot_id):
        def f(dt):
            path = self._pathFinder.getPath(
                (
                    self._bot_data["bots"][bot_id]["current_position"][0],
                    self._bot_data["bots"][bot_id]["current_position"][1]
                ),
                self._bot_data["enemy_flag"]
            )

            self._bot_data["bots"][bot_id]["path"]        = path
            self._bot_data["bots"][bot_id]["path_length"] = len(path)
            self._bot_data["bots"][bot_id]["path_index"]  = 0

            return NodeTree.SUCCESS

        return f


    def bot_fun_follow_current_path(self, bot_id):
        def f(dt):
            current_index   = self._bot_data["bots"][bot_id]["path_index"]
            path            = self._bot_data["bots"][bot_id]["path"]
            bot_position    = self._bot_data["bots"][bot_id]["current_position"]


            if current_index == self._bot_data["bots"][bot_id]["path_length"]:
                return NodeTree.SUCCESS


            if points_distance(path[current_index], (bot_position[0], bot_position[1])) < 10:
                self._bot_data["bots"][bot_id]["destination"] = path[current_index + 1]
                self._bot_data["bots"][bot_id]["path_index"] += 1

                return NodeTree.RUNNING

            self._bot_data["bots"][bot_id]["destination"] = path[current_index]
            return NodeTree.RUNNING
            
        return f


    def build_stupid_bot_behavior(self, bot_id):
        root_node = Sequence()

        first_leaf = Leaf(self.bot_fun_find_path_to_flag(bot_id))
        second_leaf = Leaf(self.bot_fun_follow_current_path(bot_id))

        root_node.append_node(first_leaf)
        root_node.append_node(second_leaf)

        return root_node
