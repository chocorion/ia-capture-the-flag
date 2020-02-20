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

        # This does nothing interesting, just a demonstration.

        returnData = { "bots": { } }

        for bot_id in pollingData["bots"].keys():
            current_position = pollingData["bots"][bot_id]["current_position"]
            
            returnData["bots"][bot_id] = { "target_position" : (2000, 1000 , 100), "actions" : 0 }

        return returnData
