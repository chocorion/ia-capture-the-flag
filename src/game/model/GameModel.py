from model.Model import Model
from model.PhysicsEngine import PhysicsEngine
from service.Ruleset import Ruleset
from service.Physics import Physics
from service.Config import Config
from domain.Map import *
from domain.GameObject.Bot import *
from domain.Player import Player
from copy import deepcopy

import threading
import sys

class PollThread(threading.Thread):
    def __init__(self, model, team_id, player, pollingData):
        super(PollThread, self).__init__()
        self._stop_event = threading.Event()
        self.model = model
        self.team_id = team_id
        self.player = player
        self.pollingData = pollingData

    def run(self):
        self.model.teams_data[self.team_id] = None
        result = self.player.poll(self.pollingData)
        self.model.teams_data[self.team_id] = result

    def stop(self):
        self._stop_event.set()

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

        self._engine = PhysicsEngine(self._ruleset, self._map)

        self._players = dict()

        #### Implementation Simu ####
        try:
            self._players["1"] = Player1(deepcopy(mapData), deepcopy(self._ruleset))
        except:
            print("Player 1 can't be evaluated because it failed to initialize")

        try:
            self._players["2"] = Player2(deepcopy(mapData), deepcopy(self._ruleset))
        except:
            print("Player 2 can't be evaluated because it failed to initialize")
        ####

        self._teams = dict()
        self._team_fails = dict()

        for team in range(1,3): # 2 Players
            team_id = str(team)

            self._team_fails[team_id] = 0 # Keep track of each failure to respond from players

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

        self._engine.tick(deltaTime)
        self.deltaTime = deltaTime

        self.teams_data = dict()
        team = 1

        threads = list()

        # Send polling data to each player and get their response
        for team_id in self._players.keys():
            player = self._players[team_id]

            pollingData = { "bots" : {}, "events": {}}

            for bot_id in self._teams[team_id]["bots"].keys():
                bot = self._teams[team_id]["bots"][bot_id]
                pollingData["bots"][bot_id] = { "current_position" : (bot.x, bot.y, bot.angle, bot.speed) }

            #try:
            threads.append(PollThread(self, team_id, player, pollingData))
            #except:
            #    print("WARNING: Could not start polling thread for team {} ! Their actions will not be applied.".format(team_id))

            team += 1
            
        for thread in threads:
            thread.start()
            
        for thread in threads:
            thread.join(0.016)

        for thread in threads:
            thread.stop()
                
        # Interpret players orders
        for team_id in self.teams_data.keys():
            if(self.teams_data[team_id] == None):
                print("Invalid response from player !!!")
                self._team_fails[team_id] += 1
                continue

            try:
                data = self.teams_data[team_id]
                for bot_id in data["bots"].keys():
                    bot = self._teams[team_id]["bots"][bot_id]

                    # Unpack target
                    target_x = data["bots"][bot_id]["target_position"][0]
                    target_y = data["bots"][bot_id]["target_position"][1]
                    target_speed = data["bots"][bot_id]["target_position"][2]
                    
                    # Perform checks                    
                    bot.angle = self._engine.checkAngle(bot, target_x, target_y)
                    bot.speed = self._engine.checkSpeed(bot, target_speed)

                    bot.speed = bot.speed * self._engine.getDeltaTimeModifier()

                    # Apply movement
                    (real_x, real_y) = Physics.applyMovement(bot.x, bot.y, bot.angle, bot.speed)
                    (new_x,new_y) = self._engine.checkCollision(bot.x,bot.y,real_x,real_y)

                    bot.move(new_x - bot.x, new_y - bot.y)

                    # bitwise comparison for actions
                    actions = bin(data["bots"][bot_id]["actions"])

                    if actions[0]: # SHOOT
                        pass
                    if actions[1]: # DROP_FLAG
                        pass
            except:
                print("Invalid response from player {} : {}".format(team_id,sys.exc_info()[0]))
                self._team_fails[team_id] += 1

        for team_id in self._team_fails.keys():
            if self._team_fails[team_id] >= Config.InvalidResponsesKick():
                print("Player {} is disqualified for failing to provide consistent responses.".format(team_id))
                self.kick(team_id)
                self._team_fails[team_id] = -1

        # Check if bots can pick items on the ground
        allBots = self.getBots()

        for bot_id in allBots.keys():
            bot = allBots[bot_id]
            for flag in self._map.flags:
                if not flag.held and Physics.rectIntersectsCircle(flag.x,flag.y,flag.width,flag.height,bot.x,bot.y,bot.radius):
                    bot.pickUp(flag)


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
        Only used if we make it a server.

        Add a new player to the game and provide it with necessary data.

        Returns:
            data : Contains all the data a player can have at it's init.
        """
       
        pass

    def kick(self, team_id):
        """
        Kick a player from the game.
        """
        del self._players[team_id]