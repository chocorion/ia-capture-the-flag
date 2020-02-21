from domain.Player import Player
from domain.Map.RegularMap import RegularMap

from ai.pathFinding.PathFinder import PathFinder
from ai.pathFinding.aStar.Astar import Astar
from ai.pathFinding.aStar.NodeAstar import NodeAstar
from ai.pathFinding.base.Graph import Graph

from domain.Map import Map

from ai.behaviorTree import *

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

class myPlayer(Player):
    
    def debug(self, botId, message):
        if int(botId.split("_")[1]) == 0:
            print("[LITTLE_PLAYER] " + message)


    def __init__(self, gameMap, rules, team):
        self._team         = team
        self._map          = RegularMap(gameMap)
        self._rules        = rules
        self._pathFinder   = Astar(Graph(self.buildNodeList(), [], None))

        self._init = True


        self._botData = {"bots": dict()}


    def buildNodeList(self):
        Nodelist = []
        for y in range(self._map.blockHeight):
            for x in range(self._map.blockWidth):
                    Nodelist.insert(
                        0,
                        NodeAstar(x, y, self._map.blocks[x][y]))
        return Nodelist
    
    def _build_response(self):
        response = {"bots": dict()}

        for botId in self._botData["bots"].keys():
            dest = self._botData["bots"][botId]["destination"]

            response["bots"][botId] = {
                "targetPosition": (
                    dest[0] * Map.BLOCKSIZE + Map.BLOCKSIZE//2,
                    dest[1] * Map.BLOCKSIZE + Map.BLOCKSIZE//2,
                    100
                ),
                "actions": 0
            }

        return response

    def _updateData(self, pollingData):
        for botId in pollingData["bots"].keys():
            self._botData["bots"][botId]["currentPosition"] = pollingData["bots"][botId]["currentPosition"]

    def poll(self, pollingData):
        if self._init:
            
            for botId in pollingData["bots"]:
                self._botData["bots"][botId] = pollingData["bots"][botId]
                self._botData["bots"][botId]["behavior"] = self.buildStupidBotBehavior(botId)

            for flag in pollingData["events"]["flags"]:
                if flag["team"] != self._team:
                    self._botData["enemy_flag"] = flag["position"]
            
            self._init = False

        self._updateData(pollingData)

        for botId in self._botData["bots"].keys():
            result = self._botData["bots"][botId]["behavior"].tick(0)

        return self._build_response()


    ###########################################################
    # Bot behavior part
    #######################

    def botFunFindPathToFlag(self, botId):
        def f(dt):
            path = self._pathFinder.getPath(
                (
                    self._botData["bots"][botId]["currentPosition"][0],
                    self._botData["bots"][botId]["currentPosition"][1]
                ),
                self._botData["enemy_flag"] # temporary
            )
            self._botData["bots"][botId]["path"]        = path
            self._botData["bots"][botId]["pathLength"] = len(path)
            self._botData["bots"][botId]["pathIndex"]   = 0

            return NodeTree.SUCCESS

        return f


    def botFunFollowCurrentPath(self, botId):
        def f(dt):
            currentIndex = self._botData["bots"][botId]["pathIndex"]
            path         = self._botData["bots"][botId]["path"]
            botPosition  = self._botData["bots"][botId]["currentPosition"]

            if currentIndex == self._botData["bots"][botId]["pathLength"] - 1:
                return NodeTree.SUCCESS

            
            if distance(path[currentIndex][0] * Map.BLOCKSIZE + Map.BLOCKSIZE//2, path[currentIndex][1] * Map.BLOCKSIZE + Map.BLOCKSIZE//2, botPosition[0], botPosition[1]) <= 80:
                self._botData["bots"][botId]["destination"] = path[currentIndex + 1]
                self._botData["bots"][botId]["pathIndex"] += 1

                return NodeTree.RUNNING

            self._botData["bots"][botId]["destination"] = path[currentIndex]
            return NodeTree.RUNNING
            
        return f

    def botFunFindPathToHome(self, botId):
        def f(dt):
            randomHomePos = self._map.GetRandomPositionInSpawn(self._team, margin = 20)
            
            path = self._pathFinder.getPath(
                (
                    self._botData["bots"][botId]["currentPosition"][0],
                    self._botData["bots"][botId]["currentPosition"][1]
                ),
                randomHomePos
            )

            self._botData["bots"][botId]["path"]        = path
            self._botData["bots"][botId]["pathLength"]  = len(path)
            self._botData["bots"][botId]["pathIndex"]   = 0

            return NodeTree.SUCCESS

        return f



    def buildStupidBotBehavior(self, botId):
        root_node = Sequence()

        root_node.appendNode(Leaf(self.botFunFindPathToFlag(botId)))
        root_node.appendNode(Leaf(self.botFunFollowCurrentPath(botId)))
        root_node.appendNode(Leaf(self.botFunFindPathToHome(botId)))
        root_node.appendNode(Leaf(self.botFunFollowCurrentPath(botId)))

        return root_node
