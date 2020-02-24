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
            _currentPath: Dict storing path for each botId
                {
                    "<botIdentifier>" : list of point corresponding to path
                }
            _currentIndex: Dict storing index of the current path for each botId
                {
                    "<botIdentifier>" : int : index of the current path (ex: 10 is 10th point of path)
                }
            _lastPosition: Dict storing last position of the bot botId
                {
                    "<botIdentifier>" : (int, int): last position
                }
            _canSend: Tell if we can send the next action.
            _blockedBots: List of the blocked bots : botId is add to list if the bot is blocked
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
        self._blockedBots = list()

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
            botId: The ID of the requested bot (ex: '1_0')
    """

    def initCurrentIndex(self, botId):
        if not botId in self._currentIndex:
            self._currentIndex[botId] = 0
        if not botId in self._lastPosition:
            self._lastPosition[botId] = -1, -1

    """ 
        Get the next position of the current path for the bot.
        If there is no currentPath do nothing.

        Parameters:
            botId: The ID of the requested bot (ex: '1_0')
        
        Returns:
            (x, y) : The next coordinates
    """

    def getNextPos(self, botId):
        if botId in self._currentPath and botId in self._currentIndex:
            x, y =  (self._currentPath[botId][self._currentIndex[botId]][0] * Map.BLOCKSIZE + Map.BLOCKSIZE//2,
                     self._currentPath[botId][self._currentIndex[botId]][1] * Map.BLOCKSIZE + Map.BLOCKSIZE//2)
            return (x, y)

    """
        If not already computed, get a path for the bot from the current position to the pos selected.
        Store it at self._currentPath[botId].
        
        Parameters:
            botId: The ID of the requested bot (ex: '1_0')
            currentPosition:The start position for the path
            pos: The goal position for the path        
    """

    def getPath(self, botId, currentPosition, pos):
        if not botId in self._currentPath:
            self._currentPath[botId] = self._pathFinder.getPath(currentPosition, pos)

    """
        Increments the index of the bot if the old index (i.e position) has been reached.
        The index and the path must exist for the given botId.
        
        Parameters:
            botId: The ID of the requested bot (ex: '1_0')
            currentPosition: The current position of the requested bot      
    """

    def incrementIndex(self, botId, currentPosition):
        radiusBot = 36
        if botId in self._currentPath and botId in self._currentIndex and self._currentPath[botId] != None :
            
            posInPath    = self.getNextPos(botId)
            lengthPath   = len(self._currentPath[botId]) -1
            distancePath = self._distance(currentPosition, posInPath)
            distanceOld  = self._distance(currentPosition,self._lastPosition[botId])

            if distanceOld - distancePath > -radiusBot and self._currentIndex[botId] != lengthPath :
                self._currentIndex[botId] += 1
            

    """
        Check if the bot is blocked next to a wall.
        If so, set a new position if path in order to get the correct angle to avoid the wall.
        
        Parameters:
            currentPosition: The current position of the requested bot      
            botId: The ID of the requested bot (ex: '1_0')
        
        Returns:
            boolean: True if blocked else false
    """

    def isBlocked(self, currentPosition, botId):
        x, y = int(currentPosition[0] // Map.BLOCKSIZE), int(currentPosition[1] // Map.BLOCKSIZE)
        if self._lastPosition[botId] == currentPosition:
            currentPosition = self._pollingData["bots"][botId]["currentPosition"]
            
            angle = currentPosition[2]

            if angle  < -180:
                angle += 360
            elif angle > 180:
                angle -= 360

            posX, posY = currentPosition[0], currentPosition[1]
            # Bloqué à gauche
            if posX % Map.BLOCKSIZE < 3 and self._map["blocks"][x - 1][y].solid:
                if angle < 0: #negative
                    self._currentPath[botId].insert(self._currentIndex[botId], (x, y - 1))
                else:
                    self._currentPath[botId].insert(self._currentIndex[botId], (x, y + 1))


            # Bloqué à droite
            elif posX % Map.BLOCKSIZE > Map.BLOCKSIZE - 3 and self._map["blocks"][x + 1][y].solid:
                if angle < 0:
                    self._currentPath[botId].insert(self._currentIndex[botId], (x, y - 1))
                else:
                    self._currentPath[botId].insert(self._currentIndex[botId], (x, y + 1))

            # Bloqué en haut
            elif posY % Map.BLOCKSIZE < 3 and self._map["blocks"][x][y - 1].solid:
                if angle < -90:
                    self._currentPath[botId].insert(self._currentIndex[botId], (x - 1, y))
                else:
                    self._currentPath[botId].insert(self._currentIndex[botId], (x + 1, y))
    
            # Bloqué en bas
            elif posY % Map.BLOCKSIZE > Map.BLOCKSIZE - 3 and self._map["blocks"][x][y + 1].solid:
                if angle < 90:
                    self._currentPath[botId].insert(self._currentIndex[botId], (x - 1, y))
                else:
                    self._currentPath[botId].insert(self._currentIndex[botId], (x + 1, y))

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
        for botId in self._pollingData["bots"].keys():
            self.initCurrentIndex(botId)
            currentPosition = self._pollingData["bots"][botId]["currentPosition"]
            tmpX, tmpY     = int(currentPosition[0]), int(currentPosition[1])
            currentPosition = (tmpX, tmpY, currentPosition[2], currentPosition[3])
            
            #Test case random pos
            if pos == None :
                pos = (5600, 2500, currentPosition[2], 0)

            self.getPath(botId, currentPosition, pos)
            
            if self._currentPath[botId] == None:
                continue
            self.incrementIndex(botId, currentPosition)

        self._canSend = True

    """
        Define the next action needed to be done and format it in the way the engine need to.
        Returns:
            The computed data to send to the engine.
            {
                "bots": {
                    "<botIdentifier>" : { "targetPosition" : ( <x> , <y>, <speed> ), "actions" : <bitwiseActions> },
                    ...
                }
            }
    """

    def getReturnPoll(self):
        returnData  = { "bots": { } }
        maxDistance = 0.0

        for botId in self._pollingData["bots"].keys():
            currentPosition = self._pollingData["bots"][botId]["currentPosition"]
            lengthPath       =  len(self._currentPath[botId]) -1

            if botId in self._currentPath and botId in self._currentIndex and self._canSend:

                if self._currentPath[botId] != None and self._currentIndex[botId] != lengthPath:
                    speed = 100

                    if self.isBlocked(currentPosition, botId):
                        if not botId in self._blockedBots:
                            self._blockedBots.append(botId)
                        

                    if botId in self._blockedBots:
                        
                        if self._distance(currentPosition, self._lastPosition[botId]) > maxDistance:
                            
                            self._blockedBots.remove(botId)
                            self._lastPosition[botId] = currentPosition
                        else:
                            speed = 5
                    else:
                        self._lastPosition[botId] = currentPosition

                        
                    currentPosInPath = self._currentPath[botId][self._currentIndex[botId]]
                    xInPath          = currentPosInPath[0] * Map.BLOCKSIZE + Map.BLOCKSIZE//2
                    yInPath          = currentPosInPath[1] * Map.BLOCKSIZE + Map.BLOCKSIZE//2
                    
                    returnData["bots"][botId] = { "targetPosition" : (xInPath, yInPath, speed), "actions" : 0 }
                else:
                    if botId in self._currentPath and botId in self._currentIndex and self._currentIndex[botId] == lengthPath:

                        currentPosInPath = self._currentPath[botId][self._currentIndex[botId]]
                        xInPath          = currentPosInPath[0] * Map.BLOCKSIZE + Map.BLOCKSIZE//2
                        yInPath          = currentPosInPath[1] * Map.BLOCKSIZE + Map.BLOCKSIZE//2

                        if self.distance(xInPath, yInPath, currentPosition[0], currentPosition[1]) > 10:
                            returnData["bots"][botId] = {"targetPosition" : (xInPath, yInPath, 100),"actions" : 0 }
                    else:
                        returnData["bots"][botId] = {"targetPosition" : (currentPosition[0], currentPosition[1], 0),"actions" : 0 }
        return returnData


    """
    This function will be called on each tick, use it to indicate your actions.

    Parameters:    
        pollingData :
        {
            "bots" : {
                "<botIdentifier>" : { "currentPosition" : ( <x> , <y> , <angle>, <speed> ) },
                ...
            },
            "events" : {
                ...
                "flags": {
                    "team" : <teamNumber>
                    "position" : (<x>, <y>)
                }
            }
        }
    
    Returns:
        {
            "bots": {
                "<botIdentifier>" : { "targetPosition" : ( <x> , <y>, <speed> ), "actions" : <bitwiseActions> },
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
        self.initPathFinder()
        self.pathWithPollingData()
        return self.getReturnPoll()
