
# This class may interact with the game
class Player:

    # Position in bitwise comparison
    SHOOT = 0
    DROP_FLAG = 1

    def __init__(self, map, rules):
        raise NotImplementedError

    # Poll the player for its new actions
    #
    # return : 
    #   {
    #       "bots": {
    #           "bot_identifier" : { "target_position" : ( x , y , speed ), "actions" : bitwise_actions },
    #           ...
    #       }
    #   }
    #
    #   Actions: 
    #       1 -> Shoot
    #       2 -> Drop Flag
    #       4 -> ...
    #       8 -> ...
    #
    #   Example:
    #       3 -> Shoot + Drop Flag
    #
    def poll(self, pollingData):
        raise NotImplementedError
