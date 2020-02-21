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

    """
        Implements a player for the CTF.

        Attributes:
            _map: The current map object of the game.
            _rules: The current rules (object) apply to the game.
            _graph: Representation in a graph of the map.
            _pathFinder: Object to get a path for some start and goal position.
            _currentPath: Dict storing path for each bot_id
                {
                    "<bot_identifier>" : list of point corresponding to path
                }
            _currentIndex: Dict storing index of the current path for each bot_id
                {
                    "<bot_identifier>" : int : index of the current path (ex: 10 is 10th point of path)
                }
            _lastPosition: Dict storing last position of the bot bot_id
                {
                    "<bot_identifier>" : (int, int): last position
                }
            _canSend: Tell if we can send the next action.
            _blocked_bots: List of the blocked bots : bot_id is add to list if the bot is blocked
    """
    
    def __init__(self, _map, rules, team):
        # vvvvvvvvvvv
        RegularMap(_map) # <----- use this for the map
        # ^^^^^^^^^^^

        # map and rules are python objects, need to make them JSON
        self._map          = _map
        self._rules        = rules
        self._graph        = Graph(self.buildNodeList(), [], None)
        self._pathFinder   = None
        self._currentPath  = {}
        self._currentIndex = {}
        self._lastPosition = {}
        self._canSend      = False
        self._blocked_bots = list()

        self._team = team
        #print("Bonjour! Je suis un joueur :))) avec {} bots".format(rules["BotsCount"]))

    """
        Build a list of NodeAstar representing each block of the map

        A nodeAstar is represented by (x, y, cellContent)
        For exemple: NodeAstar(1, 1, WallObject)

        Returns:
            The NodeList representing each block ofthe map
    """

    def buildNodeList(self):
        Nodelist = []
        for y in range(self._map["blockHeight"]):
            for x in range(self._map["blockWidth"]):
                    Nodelist.insert(
                        0,
                        NodeAstar(x, y, self._map["blocks"][x][y]))
        return Nodelist
    
    """ Returns the distance beetween coordinates """

    def distance(self,x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    """ Returns the distance beetween two points """

    def _distance(self, point1, point2):
        return math.sqrt((point2[0] - point1[0] )**2 + (point2[1] - point1[1])**2)

    """If a pathFinder don't exist then create it else do nothing"""

    def initPathFinder(self):
        if not self._pathFinder:
            self._pathFinder = Astar(self._graph)

    """
        Initialize the current index (in order to be able to know on which position of the path we are)
        of the bot.
        Initialize the lastPosition of the bot to (-1, -1). (none encountered yet)

        Parameters:
            bot_id: The ID of the requested bot (ex: '1_0')
    """

    def initCurrentIndex(self, bot_id):
        if not bot_id in self._currentIndex:
            self._currentIndex[bot_id] = 0
        if not bot_id in self._lastPosition:
            self._lastPosition[bot_id] = -1, -1

    """ 
        Get the next position of the current path for the bot.
        If there is no currentPath do nothing.

        Parameters:
            bot_id: The ID of the requested bot (ex: '1_0')
        
        Returns:
            (x, y) : The next coordinates
    """

    def getNextPos(self, bot_id):
        if bot_id in self._currentPath and bot_id in self._currentIndex:
            x, y =  (self._currentPath[bot_id][self._currentIndex[bot_id]][0] * Map.BLOCKSIZE + Map.BLOCKSIZE//2,
                     self._currentPath[bot_id][self._currentIndex[bot_id]][1] * Map.BLOCKSIZE + Map.BLOCKSIZE//2)
            return (x, y)

    """
        If not already computed, get a path for the bot from the current position to the pos selected.
        Store it at self._currentPath[bot_id].
        
        Parameters:
            bot_id: The ID of the requested bot (ex: '1_0')
            current_position:The start position for the path
            pos: The goal position for the path        
    """

    def getPath(self, bot_id, current_position, pos):
        if not bot_id in self._currentPath:
            self._currentPath[bot_id] = self._pathFinder.getPath(current_position, pos)

    """
        Increments the index of the bot if the old index (i.e position) has been reached.
        The index and the path must exist for the given bot_id.
        
        Parameters:
            bot_id: The ID of the requested bot (ex: '1_0')
            current_position: The current position of the requested bot      
    """

    def incrementIndex(self, bot_id, current_position):
        rayonBot = 36
        if bot_id in self._currentPath and bot_id in self._currentIndex and self._currentPath[bot_id] != None :
            
            posInPath    = self.getNextPos(bot_id)
            lengthPath   = len(self._currentPath[bot_id]) -1
            distancePath = self._distance(current_position, posInPath)
            distanceOld  = self._distance(current_position,self._lastPosition[bot_id])
            if distanceOld - distancePath > -rayonBot and self._currentIndex[bot_id] != lengthPath :
                self._currentIndex[bot_id] += 1
            

    """
        Check if the bot is blocked next to a wall.
        If so, set a new position if path in order to get the correct angle to avoid the wall.
        
        Parameters:
            current_position: The current position of the requested bot      
            bot_id: The ID of the requested bot (ex: '1_0')
        
        Returns:
            boolean: True if blocked else false
    """

    def isBlocked(self, current_position, bot_id):
        x, y = int(current_position[0] // Map.BLOCKSIZE), int(current_position[1] // Map.BLOCKSIZE)
        if self._lastPosition[bot_id] == current_position:
            current_position = self._pollingData["bots"][bot_id]["current_position"]
            
            angle = current_position[2]

            if angle  < -180:
                angle += 360
            elif angle > 180:
                angle -= 360

            pos_x, pos_y = current_position[0], current_position[1]
            # Bloqué à gauche
            if pos_x % Map.BLOCKSIZE < 3 and self._map["blocks"][x - 1][y].solid:
                if angle < 0: #negative
                    self._currentPath[bot_id].insert(self._currentIndex[bot_id], (x, y - 1))
                else:
                    self._currentPath[bot_id].insert(self._currentIndex[bot_id], (x, y + 1))


            # Bloqué à droite
            elif pos_x % Map.BLOCKSIZE > Map.BLOCKSIZE - 3 and self._map["blocks"][x + 1][y].solid:
                if angle < 0:
                    self._currentPath[bot_id].insert(self._currentIndex[bot_id], (x, y - 1))
                else:
                    self._currentPath[bot_id].insert(self._currentIndex[bot_id], (x, y + 1))

            # Bloqué en haut
            elif pos_y % Map.BLOCKSIZE < 3 and self._map["blocks"][x][y - 1].solid:
                if angle < -90:
                    self._currentPath[bot_id].insert(self._currentIndex[bot_id], (x - 1, y))
                else:
                    self._currentPath[bot_id].insert(self._currentIndex[bot_id], (x + 1, y))
    
            # Bloqué en bas
            elif pos_y % Map.BLOCKSIZE > Map.BLOCKSIZE - 3 and self._map["blocks"][x][y + 1].solid:
                if angle < 90:
                    self._currentPath[bot_id].insert(self._currentIndex[bot_id], (x - 1, y))
                else:
                    self._currentPath[bot_id].insert(self._currentIndex[bot_id], (x + 1, y))

            else:
                return False

            return True
        else:
            return False
            

    """
        Procede the get a path to the pos if needed,
        And increment index if needed (see incrementIndex).

        Parameters:
            pos: The goal position for the path   
    """

    def pathWithPollingData(self, pos = None):
        for bot_id in self._pollingData["bots"].keys():
            self.initCurrentIndex(bot_id)
            current_position = self._pollingData["bots"][bot_id]["current_position"]
            tmp_x, tmp_y = int(current_position[0]), int(current_position[1])
            current_position = (tmp_x, tmp_y, current_position[2], current_position[3])
            #cas de test random pos
            if pos == None :
                pos = (5600, 2500, current_position[2], 0)

            # would be to remove the path if done: not implemented
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

    """
        Define the next action needed to be done and format it in the way the engine need to.
        Returns:
            The computed data to send to the engine.
            {
                "bots": {
                    "<bot_identifier>" : { "target_position" : ( <x> , <y>, <speed> ), "actions" : <bitwise_actions> },
                    ...
                }
            }
    """

    def getReturnPoll(self):
        returnData  = { "bots": { } }
        maxDistance = 0.0

        for bot_id in self._pollingData["bots"].keys():
            current_position = self._pollingData["bots"][bot_id]["current_position"]
            lengthPath       =  len(self._currentPath[bot_id]) -1

            if bot_id in self._currentPath and bot_id in self._currentIndex and self._canSend:

                if self._currentPath[bot_id] != None and self._currentIndex[bot_id] != lengthPath:
                    speed = 100

                    if self.isBlocked(current_position, bot_id):
                        if not bot_id in self._blocked_bots:
                            self._blocked_bots.append(bot_id)
                        #print("[DEBUG] {} est blocké".format(bot_id))

                    if bot_id in self._blocked_bots:
                        #print("[DEBUG] {} est dans la liste des blockés".format(bot_id))
                        if self._distance(current_position, self._lastPosition[bot_id]) > maxDistance:
                            #print("[DEBUG] il se débloque")
                            self._blocked_bots.remove(bot_id)
                            self._lastPosition[bot_id] = current_position
                        else:
                            speed = 5
                    else:
                        self._lastPosition[bot_id] = current_position

                        
                    currentPosInPath = self._currentPath[bot_id][self._currentIndex[bot_id]]
                    xInPath          = currentPosInPath[0] * Map.BLOCKSIZE + Map.BLOCKSIZE//2
                    yInPath          = currentPosInPath[1] * Map.BLOCKSIZE + Map.BLOCKSIZE//2
                    
                    returnData["bots"][bot_id] = { "target_position" : (xInPath, yInPath, speed), "actions" : 0 }
                else:
                    if bot_id in self._currentPath and bot_id in self._currentIndex and self._currentIndex[bot_id] == lengthPath:
                        currentPosInPath = self._currentPath[bot_id][self._currentIndex[bot_id]]
                        xInPath          = currentPosInPath[0] * Map.BLOCKSIZE + Map.BLOCKSIZE//2
                        yInPath          = currentPosInPath[1] * Map.BLOCKSIZE + Map.BLOCKSIZE//2
                        if self.distance(xInPath, yInPath, current_position[0], current_position[1]) > 10:
                            returnData["bots"][bot_id] = {"target_position" : (xInPath, yInPath, 100),"actions" : 0 }
                    else:
                        returnData["bots"][bot_id] = {"target_position" : (current_position[0], current_position[1], 0),"actions" : 0 }
            #print(current_position)
        return returnData


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
                "flags": {
                    "team" : <team_number>
                    "position" : (<x>, <y>)
                }
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
    def poll(self, pollingData):
        self._pollingData = pollingData

        # if "flags" in pollingData["events"].keys():
        #     print("Flag position update !")

        #     for flag in pollingData["events"]["flags"]:
        #         print("\t{} -> {}:{}".format(flag["team"], flag["position"][0], flag["position"][1]))

        self.initPathFinder()
        self.pathWithPollingData()
        return self.getReturnPoll()
