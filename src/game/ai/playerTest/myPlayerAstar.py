from domain.Player import Player
from domain.Map.RegularMap import RegularMap
from ai.pathFinding.PathFinder import PathFinder
from ai.pathFinding.aStar.Astar import Astar
from ai.pathFinding.aStar.NodeAstar import NodeAstar
from ai.pathFinding.base.Graph import Graph
from domain.Map import Map
import math
import random
from domain.GameObject.Block import *
class myPlayer(Player):

    def __init__(self, _map, rules):
        # map and rules are python objects, need to make them JSON
        self._map          = _map
        self._rules        = rules
        self._graph        = Graph(self.buildNodeList(),
                                [],
                                None)
        self._pathFinder   = None
        self._currentPath  = {}
        self._currentIndex = {}
        self._currentTry   = {}
        self._lastPosition = {}
        self._canSend = False

        self._blocked_bots = list()

        #print("Bonjour! Je suis un joueur :))) avec {} bots".format(rules["BotsCount"]))

        """
        This function will be called on each tick, use it to indicate your actions.
    
        Parameters:    
            pollingData :
            {
                "bots" : {
                    "<bot_identifier>" : { "current_position" : ( <x> , <y> , <angle>, <speed> ) },
                    ...
                },
                "events" : {
                    ...
                }
            }
        
        Returns:
            {
                "bots": {
                    "<bot_identifier>" : { "target_position" : ( <x> , <y>, <speed> ), "actions" : <bitwise_actions> },
                    ...
                }
            }
        
        Actions: bitwise enumeration
            1 : Shoot
            2 : Drop Flag
            4 : ... More to come
        
        Example:
            3 -> Shoot + Drop Flag        
        
        """

    def distance(self,x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def getNextPos(self, bot_id, current_position):
        if bot_id in self._currentPath and bot_id in self._currentIndex:
            x, y =  (self._currentPath[bot_id][self._currentIndex[bot_id]][0] * Map.BLOCKSIZE,
                     self._currentPath[bot_id][self._currentIndex[bot_id]][1] * Map.BLOCKSIZE)
            return (x, y)
    
    def initPathFinder(self):
        if not self._pathFinder:
            self._pathFinder = Astar(self._graph)

    def initCurrentIndex(self, bot_id):
        if not bot_id in self._currentIndex:
            self._currentIndex[bot_id] = 0
        if not bot_id in self._lastPosition:
            self._lastPosition[bot_id] = -1, -1
                
    def getPath(self, bot_id, current_position, pos):
        if not bot_id in self._currentPath:
            self._currentPath[bot_id] = self._pathFinder.getPath(current_position, pos)

    def incrementIndex(self, bot_id, current_position):
        if bot_id in self._currentPath and bot_id in self._currentIndex and self._currentPath[bot_id] != None :
            
            posInPath    = self.getNextPos(bot_id, current_position)
            lengthPath   = len(self._currentPath[bot_id])-1
            distancePath = self.distance(current_position[0], current_position[1], posInPath[0], posInPath[1])
           
            if distancePath < 80.0 and self._currentIndex[bot_id] != lengthPath :
                self._currentIndex[bot_id] += 1
            

    def isBlocked(self, current_position, bot_id):
        x, y = int(current_position[0]// Map.BLOCKSIZE), int(current_position[1] // Map.BLOCKSIZE)
        #current_block = self._map["blocks"][x][y]
        ##print(current_block)
        if self._lastPosition[bot_id] == current_position:
            current_position = self._pollingData["bots"][bot_id]["current_position"]
            #print("Je suis bloqué" + str(current_position[2]%180))
            
            angle = current_position[2]

            if angle < -180:
                angle += 360
            elif angle > 180:
                angle -= 360

            #print("[ANGLE] base -> {}, new -> {}".format(current_position[2], angle))

            #print("[DEBUG] {}".format((current_position[2], angle)))

            # Wall right
            if angle > 0 and angle < 45:
                self._currentPath[bot_id].insert(self._currentIndex[bot_id], (x, y + 1))
            elif angle > -45 or angle < 0:
                self._currentPath[bot_id].insert(self._currentIndex[bot_id], (x, y - 1))

            # Wall left
            if angle > 135 and angle < 180:
                self._currentPath[bot_id].insert(self._currentIndex[bot_id], (x, y + 1))
            elif angle <= -180 or angle > -135:
                self._currentPath[bot_id].insert(self._currentIndex[bot_id], (x, y - 1))

            # Wall up
            elif angle > -135 and angle <= -90:
                self._currentPath[bot_id].insert(self._currentIndex[bot_id], (x - 1, y))
            elif angle > -90 and angle <= -45:
                self._currentPath[bot_id].insert(self._currentIndex[bot_id], (x + 1, y))

            # Wall down
            elif angle > 135 and angle <= 90:
                self._currentPath[bot_id].insert(self._currentIndex[bot_id], (x - 1, y))
            elif angle > 90 and angle <= 45:
                self._currentPath[bot_id].insert(self._currentIndex[bot_id], (x + 1, y))
            else:
                return False

            return True
            

            
    
    def pathWithPollingData(self, pollingData, pos = None):
        for bot_id in pollingData["bots"].keys():
            self.initCurrentIndex(bot_id)
            current_position = pollingData["bots"][bot_id]["current_position"]
            #cas de test
            if pos == None :
                pos = (5600, 2500, current_position[2], 0)
            # if (bot_id in self._currentIndex and bot_id in self._currentPath and self._currentPath[bot_id] != None
            #     and self._currentIndex[bot_id] == len(self._currentPath[bot_id])-1):
            #     remove =self._currentPath.pop(bot_id)
            #     del remove
            #     self._currentIndex[bot_id] = 0

            self.getPath(bot_id, current_position, pos)
            if self._currentPath[bot_id] == None:
                continue
            self.incrementIndex(bot_id, current_position)
        self._canSend = True

    def getReturnPoll(self, pollingData):
        returnData = { "bots": { } }

        for bot_id in pollingData["bots"].keys():
            current_position = pollingData["bots"][bot_id]["current_position"]
            lengthPath =  len(self._currentPath[bot_id])-1
            ##print(self._canSend)
            if bot_id in self._currentPath and bot_id in self._currentIndex and self._canSend:
                if self._currentPath[bot_id] != None and self._currentIndex[bot_id] != lengthPath:
                    speed = 100

                    if self.isBlocked(current_position, bot_id):
                        self._blocked_bots.append(bot_id)
                        #print("[DEBUG] {} est blocké".format(bot_id))

                    if bot_id in self._blocked_bots:
                        #print("[DEBUG] {} est dans la liste des blockés".format(bot_id))
                        if self.distance(current_position[0],current_position[1], self._lastPosition[bot_id][0], self._lastPosition[bot_id][1]) > 75:
                            #print("[DEBUG] il se débloque")
                            self._blocked_bots.remove(bot_id)
                            self._lastPosition[bot_id] = current_position
                        else:
                            speed = 5
                    else:
                        self._lastPosition[bot_id] = current_position

                        
                    currentPosInPath = self._currentPath[bot_id][self._currentIndex[bot_id]]
                    returnData["bots"][bot_id] = { "target_position" : 
                    (currentPosInPath[0] * Map.BLOCKSIZE + Map.BLOCKSIZE//2,
                    currentPosInPath[1] * Map.BLOCKSIZE + Map.BLOCKSIZE//2,
                    speed), "actions" : 0 }
                else:
                    returnData["bots"][bot_id] = {"target_position" : (current_position[0], current_position[1], 0),"actions" : 0 }
        return returnData

    def poll(self, pollingData):
        self._pollingData = pollingData
        self.initPathFinder()
        self.pathWithPollingData(pollingData)
        return self.getReturnPoll(pollingData)

    def buildNodeList(self):
        Nodelist = []
        for y in range(self._map["blockHeight"]):
            for x in range(self._map["blockWidth"]):
                    Nodelist.insert(
                        0,
                        NodeAstar(x, y, self._map["blocks"][x][y]))
        return Nodelist