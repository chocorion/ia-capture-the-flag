from domain.Player import Player

class myPlayer(Player):
    """
    This is an example AI.

    Your AI must also be named 'myPlayer' and implement 'Player'.
    """

    def __init__(self, map, rules, team):
        # map and rules are python objects, need to make them JSON
        print("Bonjour! Je suis un joueur :))) avec {} bots".format(rules["BotsCount"]))

    def poll(self, pollingData):
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

        # This does nothing interesting, just a demonstration.

        returnData = { "bots": { } }

        for botId in pollingData["bots"].keys():
            currentPosition = pollingData["bots"][botId]["currentPosition"]
            
            returnData["bots"][botId] = { "targetPosition" : (2000, 1000 , 100), "actions" : 0 }

        return returnData
