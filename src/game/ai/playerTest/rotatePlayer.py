from domain.Player import Player

import math

class myPlayer(Player):
    """
    Rotates
    """

    def __init__(self, map, rules, team):
        pass

    def poll(self, pollingData):

        returnData = { "bots": { } }

        for botId in pollingData["bots"].keys():
            currentPosition = pollingData["bots"][botId]["currentPosition"]
            
            target = (currentPosition[0] + math.cos(math.radians((currentPosition[2] + 5))) * 100, currentPosition[1] + math.sin(math.radians((currentPosition[2] + 5))) * 100 , 0)
            
            returnData["bots"][botId] = { "targetPosition" : target, "actions" : 1 }

        return returnData
