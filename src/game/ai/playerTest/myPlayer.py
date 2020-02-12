from domain.Player import Player

class myPlayer(Player):

    def __init__(self, map, rules):
        print("Bonjour! Je suis un joueur :))) avec {} bots".format(rules["BotsCount"]))

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
        return { "bots": { } } # :(((
