
class Player:
    """
    Implement this to create your AI.

    This class interacts with the game by returning it's targets and actions during the poll function.
    You are free to do whatever you want as long as you respond !

    Actions available to the player are described in the enumeration in class variables.
    """


    SHOOT = 1
    """
    Bots can fire a weapon and damage the health of other bots. There is a cooldown of X milliseconds.
    """
    DROP_FLAG = 2
    """
    If they are holding a flag, bots can drop it next to their current location for other to pick it up.
    """

    def __init__(self, map, rules, team):
        raise NotImplementedError


    def poll(self, pollingData):
        """
        This function will be called on each tick, use it to indicate your actions.
    
        Parameters:    
            pollingData :
            {
                "bots" : {
                    "<botIdentifier>" : { 
                        "attributes"        : ( <life> , <flag> , <shootCooldown> ),
                        "currentPosition"  : ( <x> , <y> , <angle>, <speed> ),
                    },
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
        raise NotImplementedError
