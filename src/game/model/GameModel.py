from model.Model import Model
from service.Ruleset import Ruleset
from service.Physics import Physics
from domain.Map import *
from domain.GameObject.Bot import *
from domain.Player import Player
from copy import deepcopy

# Implements Model to be used by the Game Engine
class GameModel(Model):
    """
    Implements the Game Model.

    Attributes:
        map (Map) : The game map.
        ruleset (Ruleset) : The set of rules for this game.
        players (list(Player)) : The players that will be polled each tick.
        teams (dict) : Contains player informations to be sent to them.
    """

    def __init__(self, Player1, Player2):
        """
        Initialize game data.
  
        Parameters: 
           Player1 (Player): The player in control of the Red team.
           Player2 (Player): The player in control of the Blue team.
        """
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

        self._teams = dict()

        for team in range(1,3): # 2 Players
            team_id = str(team)

            self._teams[team_id] = { "bots": {} }

            for i in range(0,int(self._ruleset["BotsCount"])):
                bot_id = team_id + "_" + str(i) # Bot identifier is <team>_<number>

                (x, y) = self._map.GetRandomPositionInSpawn(team)
                self._teams[team_id]["bots"][bot_id] = RegularBot(team, x, y)


        

    def tick(self, deltaTime):
        """ 
        Update and handle the game data. Poll each player and process their actions.
  
        Parameters: 
           deltaTime (int): The time in milliseconds since the last call to this function.
        """

        teams_data = dict()
        team = 1
        # Send polling data to each player and get their response
        for player in self._players:
            team_id = str(team)

            pollingData = { "bots" : {}, "events": {}}

            for bot_id in self._teams[team_id]["bots"].keys():
                bot = self._teams[team_id]["bots"][bot_id]
                pollingData["bots"][bot_id] = { "current_position" : (bot.x, bot.y, bot.angle, bot.speed) }

            # Async call ?

            teams_data[team_id] = player.poll(pollingData)
            team += 1
            
        # if async, wait for both players response

        for team_id in teams_data.keys():
            data = teams_data[team_id]
            for bot_id in data["bots"].keys():
                bot = self._teams[team_id]["bots"][bot_id]

                # WARNING: Need to verify that the movement is correct
                target_x = data["bots"][bot_id]["target_position"][0]
                target_y = data["bots"][bot_id]["target_position"][1]
                target_speed = data["bots"][bot_id]["target_position"][2]

                # Check angle
                new_angle = Physics.getAngle( bot.x, bot.y, target_x, target_y)

                delta_angle = new_angle - bot.angle

                if delta_angle > 180:
                    delta_angle = delta_angle - 360

                elif delta_angle < -180:
                    delta_angle = 360 + delta_angle
                
                max_angle = float(self._ruleset["RotationMultiplier"]) * bot.max_rotate

                if abs(delta_angle) > max_angle :
                    delta_angle = max_angle if delta_angle > 0 else -max_angle
                    
                bot.angle = bot.angle + delta_angle

                # Check speed
                max_speed = float(self._ruleset["SpeedMultiplier"]) * bot.max_speed

                if target_speed > max_speed:
                    target_speed = max_speed

                bot.speed = target_speed

                # Apply movement
                (x,y) = Physics.applyMovement(bot.x, bot.y, bot.angle, bot.speed)
                bot.x = x
                bot.y = y


                # bitwise comparison for actions
                actions = bin(data["bots"][bot_id]["actions"])

                if actions[0]: # SHOOT
                    pass
                if actions[1]: # DROP_FLAG
                    pass

    # (needed by the View) No point in having it private, should change in the future
    def getMap(self):
        return self._map

    def getBots(self):
        """ 
        Update and handle the game data. Poll each player and process their actions.
  
        Returns:
            bots (list) : The list of all Bots in the game.
        """
        bots = self._teams["1"]["bots"].copy()
        bots.update(self._teams["2"]["bots"])
        return bots

    def register(self, player):
        """
        Only used if we make it a server

        Add a new player to the game and provide it with necessary data.

        Returns:
            data : Contains all the data a player can have at it's init.
        """
        self._players.append(player)