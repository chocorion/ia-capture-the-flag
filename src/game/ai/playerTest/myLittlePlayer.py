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


def convertPath(path):
    newPath = list()

    for currentIndex in range(len(path)):
        newPath.append((
            path[currentIndex][0] * Map.BLOCKSIZE + Map.BLOCKSIZE//2,
            path[currentIndex][1] * Map.BLOCKSIZE + Map.BLOCKSIZE//2
        ))

    return newPath


class myPlayer(Player):
    
    def debug(self, botId, message):
        """
        This function display message only for the bot with id 0, whatever
        the team is.

        Parameters:
            botId (String): id of a bot.
            message (String): message to display
        """

        if int(botId.split("_")[1]) == 0 and int(botId.split("_")[0]) == 1:
            print("[LITTLE_PLAYER]({})".format(botId) + message)


    def __init__(self, gameMap, rules, team):
        self._team         = team
        self._map          = RegularMap(gameMap)
        self._rules        = rules
        self._pathFinder   = Astar(Graph(self.buildNodeList(), [], None))

        self._init = True


        self._botData = {"bots": dict()}


    def buildNodeList(self):
        """
        Build the node list for pathfinding.

        Return:
            NodeList (list): node list for pathfinding.
        """

        Nodelist = []
        for y in range(self._map.blockHeight):
            for x in range(self._map.blockWidth):
                    Nodelist.insert(
                        0,
                        NodeAstar(x, y, self._map.blocks[x][y]))
        return Nodelist
    

    def _build_response(self):
        """
        Build response for the engine.

        Return:
            response (dict): Contain, for each bot :
                {
                    targetPosition: (
                        x,
                        y,
                        speed
                    ),
                    action: action_id
                }
        """

        response = {"bots": dict()}

        for botId in self._botData["bots"].keys():
            dest = self._botData["bots"][botId]["destination"]

            shoot = random.randint(0, 1000)%29 == 0


            response["bots"][botId] = {
                "targetPosition": (
                    dest[0],
                    dest[1],
                    100
                ),
                "actions": 1 if shoot else 0
            }

        return response


    def _updateData(self, pollingData):
        for botId in pollingData["bots"].keys():
            self._botData["bots"][botId]["currentPosition"] = pollingData["bots"][botId]["currentPosition"]


    def poll(self, pollingData):
        """
        Override the Player poll method.
        """

        if self._init:
            for botId in pollingData["bots"]:
                self._botData["bots"][botId] = pollingData["bots"][botId]
                self._botData["bots"][botId]["behavior"] = self.buildStupidBotBehavior(botId)

            for flag in pollingData["events"]["flags"]:
                if flag["team"] != self._team:
                    self._botData["enemy_flag"] = flag["position"]
            
            self._init = False

        if pollingData["missedTicks"] != 0:
            # print("Return empty answer")
            return {}

        self._updateData(pollingData)

        for botId in self._botData["bots"].keys():
            result = self._botData["bots"][botId]["behavior"].tick(0)

        return self._build_response()


    ##################################################
    # Bot behavior part
    #######################

    def botFunFindPathToDepot(self, botId):
        """
        Create function to find path from bot position to team depot

        Parameters:
            botId (String): Id of the bot

        Return:
            f (function()) : Function that take in parameters dt, the delta time used by NodeTree.tick().
        """
        def f(dt):
            randomDepotPos = self._map.GetRandomPositionInDepot(self._team, margin = 20)

            
            path = self._pathFinder.getPath(
                (
                    int(self._botData["bots"][botId]["currentPosition"][0]),
                    int(self._botData["bots"][botId]["currentPosition"][1])
                ),
                randomDepotPos
            )


            self._botData["bots"][botId]["path"]        = convertPath(path)
            self._botData["bots"][botId]["pathLength"]  = len(path)
            self._botData["bots"][botId]["pathIndex"]   = 0


            return NodeTree.SUCCESS

        return f


    def botFunFindPathToFlag(self, botId):
        """
        Create function to find path from bot position to enemy flag

        Parameters:
            botId (String): Id of the bot

        Return:
            f (function()) : Function that take in parameters dt, the delta time used by NodeTree.tick().
        """
        def f(dt):
            path = self._pathFinder.getPath(
                (
                    self._botData["bots"][botId]["currentPosition"][0],
                    self._botData["bots"][botId]["currentPosition"][1]
                ),
                self._botData["enemy_flag"] # temporary
            )


            self._botData["bots"][botId]["path"]        = convertPath(path)
            self._botData["bots"][botId]["pathLength"]  = len(path)
            self._botData["bots"][botId]["pathIndex"]   = 0

            return NodeTree.SUCCESS

        return f


    def botFunFollowCurrentPath(self, botId):
        """
        Create function to follow current path of the given bot.

        Parameters:
            botId (String): Id of the bot

        Return:
            f (function()) : Function that take in parameters dt, the delta time used by NodeTree.tick().
        """
        
        def f(dt):
            currentIndex = self._botData["bots"][botId]["pathIndex"]
            path         = self._botData["bots"][botId]["path"]
            botPosition  = self._botData["bots"][botId]["currentPosition"]

            if currentIndex == self._botData["bots"][botId]["pathLength"] - 1:
                return NodeTree.SUCCESS

            checkpoint_x = path[currentIndex][0]
            checkpoint_y = path[currentIndex][1]

            margin = 35
            if currentIndex == self._botData["bots"][botId]["pathLength"] - 2:
                margin = 10

            if distance(checkpoint_x, checkpoint_y, botPosition[0], botPosition[1]) <= margin:
                self._botData["bots"][botId]["destination"] = path[currentIndex + 1]
                self._botData["bots"][botId]["pathIndex"] += 1

                return NodeTree.RUNNING

            self._botData["bots"][botId]["destination"] = path[currentIndex]
            return NodeTree.RUNNING
            
        return f


    def buildStupidBotBehavior(self, botId):
        """
        Function that build simple behavior.

        Parameters:
            botId (String): id of the bot.

        Return:
            root_node (NodeTree): The simple behavior tree build.
        """
        root_node = Sequence()

        root_node.appendNode(Leaf(self.botFunFindPathToFlag(botId)))
        root_node.appendNode(Leaf(self.botFunFollowCurrentPath(botId)))
        root_node.appendNode(Leaf(self.botFunFindPathToDepot(botId)))
        root_node.appendNode(Leaf(self.botFunFollowCurrentPath(botId)))

        return root_node
