from domain.Player import Player

class myPlayer(Player):

    def __init__(self, map, rules):
        # map and rules are python objects, need to make them JSON
        print("Bonjour! Je suis un joueur :))) avec {} bots".format(rules["BotsCount"]))

    # Poll the player for its new actions
    #
    # pollingData :
    #   {
    #       "bots" : {
    #           "<bot_identifier>" : { "current_position" : ( <x> , <y> , <angle>, <speed> ) },
    #           ...
    #       },
    #       "events" : {
    #           ...
    #       }
    #   }
    #
    #
    # return : 
    #   {
    #       "bots": {
    #           "<bot_identifier>" : { "target_position" : ( <x> , <y>, <angle> , <speed> ), "actions" : <bitwise_actions> },
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

        returnData = { "bots": { } }

        for bot_id in pollingData["bots"].keys():
            current_position = pollingData["bots"][bot_id]["current_position"]
            
            returnData["bots"][bot_id] = { "target_position" : (current_position[0] + 10, current_position[1] + 10, 0, 0), "actions" : 0 }

        return returnData
