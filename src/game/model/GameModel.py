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

import sys, math
class GameModel(Model):
    """
    Implements the Game Model.

    Attributes:
        map (Map) : The game map.
        ruleset (Ruleset) : The set of rules for this game.
        players (list(Player)) : The players that will be polled each tick.
        teams (dict) : Contains player informations to be sent to them.

        countdownremaining (int) : time in milliseconds since end of start countdownremaining.
    """

    def __init__(self, Player1, Player2, map_file = './maps/map_00.txt'):
        """
        Initialize game data.
  
        Parameters: 
           Player1 (Player): The player in control of the Red team.
           Player2 (Player): The player in control of the Blue team.
        """
        mapData = RegularMap.loadMapData(map_file)

        # Generate an empty map and send it to the players
        # The bots starting positions will be sent at the first polling
        self._map = RegularMap(mapData)

        self._ruleset = Ruleset.GetRuleset()

        self._engine = PhysicsEngine(self._ruleset, self._map)

        self._engine.createCollisionMap("RegularBot", 36)

        self._argBuilder = DictBuilder()

        self._players = dict()

        self._playerProcesses = dict()

        self.turn = 0

        self.stopwatch = TimeManager()
        
        self.countdownremaining = self._ruleset["StartCountdownSeconds"] * 1000

        self.game_over = False

        self.winner = None

        self.mouse_coords = (0,0)

        self.shoots = [] # all shoots to display, reset each turn.

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
        self._teamFails = dict()
        self._teamMissedTicks = dict()

        for team in range(1,3): # 2 Players
            teamId = str(team)

            self._teamFails[teamId] = 0 # Keep track of each failure to respond from players
            self._teamMissedTicks[teamId] = 0

            self._teams[teamId] = { "bots": {} }

            for i in range(0,int(self._ruleset["BotsCount"])):
                botId = teamId + "_" + str(i) # Bot identifier is <team>_<number>

                (x, y) = self._map.GetRandomPositionInSpawn(team, 36)
                self._teams[teamId]["bots"][botId] = RegularBot(team, x, y)

            
            self._playerProcesses[teamId] = PlayerProcess(self, teamId, self._players[teamId])
            self._playerProcesses[teamId].start()

        self._lastFlagPosition = [
            (-1, -1),
            (-1, -1)
        ]

    def getEngine(self):
        return self._engine

    def tick(self, deltaTime):
        """ 
        Update and handle the game data. Poll each player and process their actions.
  
        Parameters: 
           deltaTime (int): The time in milliseconds since the last call to this function.
        """

        self._engine.tick(deltaTime)
        self.deltaTime = deltaTime

        if self.game_over:
            return

        if self.turn >= 0 and self.turn != 1 :
            # Called before the start of the countdown and each turn after (not including) the first turn
            self.handlePlayerPolling()
            self.updateLastFlagPosition()

        if self.turn > 0:
            # Call each turn to handle physics and player response
            self.handleNormalTurn()

        # In this condition, we wemove ThinkTimeMs because it is already slept during player polling
        elif self.stopwatch.PeekDeltaTimeMs() > int(self._ruleset["StartCountdownSeconds"]) * 1000 - int(self._ruleset["ThinkTimeMs"]):
            # Call once to finish countdown
            self.handleFirstTurn()

        else:
            # Call each time during countdown after the first player polling
            self.handleStartingCountdown()

        self.checkItemsPickup()

        flagInDepot = self._map.FlagInDepot()

        if flagInDepot != 0:
            self.game_over = True
            self.countdownremaining = 0
            self.winner = flagInDepot

            print("WE HAVE WINNER ")

    def handlePlayerPolling(self):
        """
        Creates and starts each Player Process which will process the player's polling function.
        """

        # This timer will run for the whole game
        # Setting the turn to -1 will make us able to know we are in the initial countdown phase
        if self.turn == 0:
            self.stopwatch.StartTimer()
            self.turn = -1

        # The data is reset each time to make sure we don't perform outdated player actions
        self.teamsData = {
            "1" : None,
            "2" : None,
        }

        # Send polling data to each player and get their response
        for teamId in self._players.keys():
            player = self._players[teamId]

            # Start to build the pollindData
            self._argBuilder.beginArgument()

            for i in range(2):
                oldFlagX, oldFlagY = self._lastFlagPosition[i]
                
                flagX = self._map.flags[i].x
                flagY = self._map.flags[i].y


                if flagX != oldFlagX or flagY != oldFlagY:
                    self._argBuilder.addFlag(self._map.flags[i].team, (flagX, flagY))

            for botId in self._teams[teamId]["bots"].keys():
                self._argBuilder.addBot(self._teams[teamId]["bots"][botId], botId)

            self._argBuilder.addMissedTicks(self._teamMissedTicks[teamId])
            self._argBuilder.endArgument()

            pollingData = self._argBuilder.getResult()

            self._playerProcesses[teamId].setData(pollingData)
            
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
                
        self.turn += 1

        # reset shoots
        self.shoots = []

        # Interpret players orders
        for teamId in self.teamsData.keys():
            if(self.teamsData[teamId] == None):
                print("Did not get a response from player {}".format(teamId))
                self._teamFails[teamId] += 1
                self._teamMissedTicks[teamId] += 1
                continue
            elif self.teamsData[teamId] == {}:
                # Empty response, player pass turn
                continue
            else:
                self._teamMissedTicks[teamId] = 0

            # try:
            data = self.teamsData[teamId]
            for botId in data["bots"].keys():
                bot = self._teams[teamId]["bots"][botId]

                # Needed for shoot
                bot_old_x = bot.x
                bot_old_y = bot.y
                bot_old_angle = bot.angle

                # Unpack target
                targetX = data["bots"][botId]["targetPosition"][0]
                targetY = data["bots"][botId]["targetPosition"][1]
                targetSpeed = data["bots"][botId]["targetPosition"][2]
                
                # Perform checks                    
                bot.angle = self._engine.checkAngle(bot, targetX, targetY)
                bot.speed = self._engine.checkSpeed(bot, targetSpeed)

                bot.speed = bot.speed * self._engine.getDeltaTimeModifier()

                # Apply movement
                (realX, realY) = Physics.applyMovement(bot.x, bot.y, bot.angle, bot.speed)
                (newX,newY) = self._engine.checkCollision("RegularBot",bot.x,bot.y,realX,realY,targetX,targetY)

                bot.move(newX - bot.x, newY - bot.y)

                # bitwise comparison for actions
                actions = bin(data["bots"][botId]["actions"])

                if actions[0]: # SHOOT
                    # bot's cooldown ?

                    targetX = bot_old_x + math.cos(math.radians(bot_old_angle)) * 10000 # Default shoot length, param it later
                    targetY = bot_old_y + math.sin(math.radians(bot_old_angle)) * 10000 
                    

                    # First opti : only check bots in front of the bot
                    (shootedBot, (end_x, end_y)) = self._engine.getShootedBot(
                        bot_old_x,
                        bot_old_y,
                        targetX,
                        targetY,
                        self.getBots(1 if int(teamId) == 2 else 2)
                    )
                    # print("Shoot from ({}:{}) to ({}:{})".format(bot_old_x, bot_old_y, end_x, end_y))

                    self.shoots.append(((bot_old_x, bot_old_y), (end_x, end_y), bot.player))

                    if shootedBot != None:
                        print("{} shoot !".format(shootedBot))
                if actions[1]: # DROP_FLAG
                    pass
            # except:
            #     print("Invalid response from player {} : {}".format(teamId,sys.exc_info()[0]))
            #     self._teamFails[teamId] += 1

        for teamId in self._teamFails.keys():
            if self._teamFails[teamId] >= Config.InvalidResponsesKick():
                print("Player {} is disqualified for failing to provide consistent responses.".format(teamId))
                self.kick(teamId)
                self._teamFails[teamId] = -1

    def handleFirstTurn(self):
        """
        Handles the end of the countdown and sets the turn to 1. This causes the turn to be handled without asking for new data, since it is collected during countdown.
        """
        self.turn = 1
        self.countdownremaining = 0

        for playerProcess in self._playerProcesses.values():
            playerProcess.check()

    def handleStartingCountdown(self):
        """
        Handles the countdown phase by always checking for a response without giving new data.
        """
        self.countdownremaining = int(self._ruleset["StartCountdownSeconds"]) * 1000 - int(self._ruleset["ThinkTimeMs"]) - self.stopwatch.PeekDeltaTimeMs()

        for playerProcess in self._playerProcesses.values():
            playerProcess.check()

    def checkItemsPickup(self):
        """
        Checks all bots for a surrounding item to pick.
        """
        allBots = self.getBots()

        for botId in allBots.keys():
            bot = allBots[botId]
            for flag in self._map.flags:
                if not flag.held and Physics.rectIntersectsCircle(flag.x,flag.y,flag.width,flag.height,bot.x,bot.y,bot.radius + 20):
                    bot.pickUp(flag)


    # (needed by the View) No point in having it private, should change in the future
    def getMap(self):
        return self._map

    def getBots(self, team = None):
        """ 
        Get bots from one or both teams
  
        Returns:
            bots (list) : The list of requested bots
        """
        if team == None:
            return self.getAllBots()
            
        return self._teams[str(team)]["bots"]

    def getAllBots(self):
        """ 
        Get bots from both teams
  
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

    def kick(self, teamId):
        """
        Kick a player from the game.
        """
        del self._players[teamId]

    def updateLastFlagPosition(self):
        """
        Updates the last position of each flag
        """
        for i in range(2):
            self._lastFlagPosition[i] = (self._map.flags[i].x, self._map.flags[i].y)
            # TODO: If the flag is inside a base, switch to endscreen

    def stop(self):
        """
        Ends the game and terminates child processes
        """
        for playerProcess in self._playerProcesses.values():
            playerProcess.kill()

    def getShoots(self):
        return self.shoots