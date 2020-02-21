
class Player:
    """
    Implement this to create your AI.

    This class interacts with the game by returning it's targets and actions during the poll function.
    You are free to do whatever you want as long as you respond !
    """

    # Value in bitwise comparison
    SHOOT = 1
    DROP_FLAG = 2

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
