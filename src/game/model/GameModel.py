from model.Model import Model
from model.PhysicsEngine import PhysicsEngine
from model.PlayerProcess import PlayerProcess
from model.ArgBuilder.JSONBuilder import JSONBuilder
from model.ArgBuilder.DictBuilder import DictBuilder
from service.Ruleset import Ruleset
from service.Physics import Physics
from service.Config import Config
from service.TimeManager import TimeManager
from domain.Map import *
from domain.GameObject.Bot import *
from domain.Player import Player
from copy import deepcopy

import sys
class GameModel(Model):
    """
    Implements the Game Model.

    Attributes:
        map (Map) : The game map.
        ruleset (Ruleset) : The set of rules for this game.
        players (list(Player)) : The players that will be polled each tick.
        teams (dict) : Contains player informations to be sent to them.

        cooldownremaining (int) : time in milliseconds since end of start cooldown.
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

        self._engine.createCollisionMap("RegularBot", 36)

        self._argBuilder = DictBuilder()

        self._players = dict()

        self._playerProcesses = dict()

        self._turn = 0

        self._stopwatch = TimeManager()
        
        self.cooldownremaining = self._ruleset["StartCountdownSeconds"] * 1000

        #### Implementation Simu ####
        try:
            self._players["1"] = Player1(mapData, self._ruleset, team=1)
        except:
            print("Player 1 can't be evaluated because it failed to initialize")

        try:
            self._players["2"] = Player2(mapData, self._ruleset, team=2)
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

                (x, y) = self._map.GetRandomPositionInSpawn(team, 36)
                self._teams[team_id]["bots"][bot_id] = RegularBot(team, x, y)

            
            self._playerProcesses[team_id] = PlayerProcess(self, team_id, self._players[team_id])
            self._playerProcesses[team_id].start()

        self._last_flag_position = [
            (-1, -1),
            (-1, -1)
        ]

    def getengine(self):
        return self._engine

    def tick(self, deltaTime):
        """ 
        Update and handle the game data. Poll each player and process their actions.
  
        Parameters: 
           deltaTime (int): The time in milliseconds since the last call to this function.
        """

        self._engine.tick(deltaTime)
        self.deltaTime = deltaTime


        if self._turn >= 0 and self._turn != 1 :
            # Called before the start of the countdown and each turn after (not including) the first turn
            self.handlePlayerPolling()
            self.updateLastFlagPosition()

        if self._turn > 0:
            # Call each turn to handle physics and player response
            self.handleNormalTurn()

        # In this condition, we wemove ThinkTimeMs because it is already slept during player polling
        elif self._stopwatch.PeekDeltaTimeMs() > int(self._ruleset["StartCountdownSeconds"]) * 1000 - int(self._ruleset["ThinkTimeMs"]):
            # Call once to finish countdown
            self.handleFirstTurn()

        else:
            # Call each time during countdown after the first player polling
            self.handleStartingCountdown()

        self.checkItemsPickup()

    def handlePlayerPolling(self):
        """
        Creates and starts each Player Process which will process the player's polling function.
        """

        # This timer will run for the whole game
        # Setting the turn to -1 will make us able to know we are in the initial countdown phase
        if self._turn == 0:
            self._stopwatch.StartTimer()
            self._turn = -1

        # The data is reset each time to make sure we don't perform outdated player actions
        self.teams_data = {
            "1" : None,
            "2" : None,
        }

        # Send polling data to each player and get their response
        for team_id in self._players.keys():
            player = self._players[team_id]

            # Start to build the pollindData
            self._argBuilder.begin_argument()

            for i in range(2):
                old_flag_x, old_flag_y = self._last_flag_position[i]
                
                flag_x = self._map.flags[i].x
                flag_y = self._map.flags[i].y


                if flag_x != old_flag_x or flag_y != old_flag_y:
                    self._argBuilder.add_flag(self._map.flags[i].team, (flag_x, flag_y))

            for bot_id in self._teams[team_id]["bots"].keys():
                self._argBuilder.add_bot(self._teams[team_id]["bots"][bot_id], bot_id)

            self._argBuilder.end_argument()

            pollingData = self._argBuilder.get_result()

            self._playerProcesses[team_id].setData(pollingData)
            
        # Start each player's computation and sleep while they should be processing
        # After we are done sleeping, two things can occur:
        #   1 - If we are in countdown phase : Players will be able to compute for the duration of the countdown
        #   2 - Else : Players will be immediatly checked and killed. If they did not finish, their (individual) turn is invalid; not affecting other players.
        for playerProcess in self._playerProcesses.values():
            playerProcess.execute()

        # The entire computation of a player must be done during this sleep (if not in countdown phase)
        TimeManager.Sleep(int(self._ruleset["ThinkTimeMs"]))

    def handleNormalTurn(self):
        """
        This stops players computing and processes their response
        """

        # This occurs right after sleeping during ThinkTimeMs milliseconds
        for playerProcess in self._playerProcesses.values():
            playerProcess.check()
                
        self._turn += 1

        # Interpret players orders
        for team_id in self.teams_data.keys():
            if(self.teams_data[team_id] == None):
                print("Did not get a response from player {}".format(team_id))
                self._team_fails[team_id] += 1
                continue

            # try:
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
                (new_x,new_y) = self._engine.checkCollision("RegularBot",bot.x,bot.y,real_x,real_y,target_x,target_y)

                bot.move(new_x - bot.x, new_y - bot.y)

                # bitwise comparison for actions
                actions = bin(data["bots"][bot_id]["actions"])

                if actions[0]: # SHOOT
                    pass
                if actions[1]: # DROP_FLAG
                    pass
            # except:
            #     print("Invalid response from player {} : {}".format(team_id,sys.exc_info()[0]))
            #     self._team_fails[team_id] += 1

        for team_id in self._team_fails.keys():
            if self._team_fails[team_id] >= Config.InvalidResponsesKick():
                print("Player {} is disqualified for failing to provide consistent responses.".format(team_id))
                self.kick(team_id)
                self._team_fails[team_id] = -1

    def handleFirstTurn(self):
        """
        Handles the end of the countdown and sets the turn to 1. This causes the turn to be handled without asking for new data, since it is collected during countdown.
        """
        self._turn = 1
        self.cooldownremaining = 0

        for playerProcess in self._playerProcesses.values():
            playerProcess.check()

    def handleStartingCountdown(self):
        """
        Handles the countdown phase by always checking for a response without giving new data.
        """
        self.cooldownremaining = int(self._ruleset["StartCountdownSeconds"]) * 1000 - int(self._ruleset["ThinkTimeMs"]) - self._stopwatch.PeekDeltaTimeMs()

        for playerProcess in self._playerProcesses.values():
            playerProcess.check()

    def checkItemsPickup(self):
        """
        Checks all bots for a surrounding item to pick.
        """
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

    def updateLastFlagPosition(self):
        for i in range(2):
            self._last_flag_position[i] = (self._map.flags[i].x, self._map.flags[i].y)