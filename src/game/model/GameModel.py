from model.Model import Model
from service.Ruleset import Ruleset
from domain.Map import *
from domain.GameObject.Bot import *
from domain.Player import Player
from copy import deepcopy

# Implements Model to be used by the Game Engine
class GameModel(Model):

    def __init__(self, Player1, Player2):
        mapData = RegularMap.loadMapData('./maps/map_00.txt')

        # Generate an empty map and send it to the players
        # The bots starting positions will be sent at the first polling
        self._map = RegularMap(mapData)

        self._ruleset = Ruleset.GetRuleset()

        self._players = list()

        #### Implementation Simu ####
        try:
            self._players.append(Player1(deepcopy(mapData), deepcopy(self._ruleset)))
        except:
            print("Player 1 can't be evaluated because it failed to initialize")

        try:
            self._players.append(Player2(deepcopy(mapData), deepcopy(self._ruleset)))
        except:
            print("Player 2 can't be evaluated because it failed to initialize")
        ####

        self._teams = dict() # This will contain informations about players, structured so that we can send those easily to them

        for team in range(1,3): # 2 Players
            team_id = str(team)

            self._teams[team_id] = { "bots": {} }

            for i in range(0,int(self._ruleset["BotsCount"])):
                bot_id = team_id + "_" + str(i) # Bot identifier is <team>_<number>

                (x, y) = self._map.GetRandomPositionInSpawn(team)
                self._teams[team_id]["bots"][bot_id] = RegularBot(team, x, y)


        

    def tick(self, deltaTime):

        teams_data = dict()
        team = 1
        # Send polling data to each player and get their response
        for player in self._players:
            team_id = str(team)
            # Async call ?
            teams_data[team_id] = player.poll({ "bots" : self._teams[team_id]["bots"], "events": {}})
            team += 1
            
        # if async, wait for both players response

        for team_id in teams_data.keys():
            data = teams_data[team_id]
            for bot_id in data["bots"].keys():

                # WARNING: Need to verify that the movement is correct
                self._teams[team_id]["bots"][bot_id].x = data["bots"][bot_id]["target_position"][0]
                self._teams[team_id]["bots"][bot_id].y = data["bots"][bot_id]["target_position"][1]
                self._teams[team_id]["bots"][bot_id].angle = data["bots"][bot_id]["target_position"][2]

                # bitwise comparison for actions
                actions = bin(data["bots"][bot_id]["actions"])

                if actions[Player.SHOOT]:
                    pass
                if actions[Player.DROP_FLAG]:
                    pass

    # (needed by the View) No point in having it private, should change in the future
    def getMap(self):
        return self._map

    def getBots(self):
        bots = self._teams["1"]["bots"].copy()
        bots.update(self._teams["2"]["bots"])
        return bots

    # Only used if we make it a server
    def register(self, player):
        self._players.append(player)
        # return formatted map and ruleset