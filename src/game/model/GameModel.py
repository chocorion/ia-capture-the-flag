from model.Model import Model
from model.PhysicsEngine import PhysicsEngine
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

from multiprocessing import Process, Pipe
import sys

class PlayerProcess():
    def __init__(self, model, team_id, player, pollingData):
        """
        Creates a new process to run a player's tick.

        Arguments:
            model (Model) : Access to the model of the game
            team_id (string) : The team to operate
            player (Player) : The player to call
            pollingData (any) : Data formatted by the used ArgBuilder
        """

        self._target = self.run

        self._parent_conn, child_conn = Pipe()

        self._model = model
        self._team_id = team_id

        self._stopwatch = TimeManager()

        self._args = (child_conn, model, team_id, player, pollingData)

        self._process = Process(target=self._target, args=self._args)

    def run(self, pipe_out, model, team_id, player, pollingData):
        model.teams_data[team_id] = None
        pipe_out.send(player.poll(pollingData))
        pipe_out.close()

    def check(self):
        if self._parent_conn.poll(0):
            result = self._parent_conn.recv()

            #print("Result obtained in {} ms".format(self._stopwatch.DeltaTimeMs()))

            if result != None:
                self._model.teams_data[self._team_id] = result

    def start(self):
        self._stopwatch.StartTimer()
        self._process.start()

    def join(self, timeout):
        self._process.join(timeout)

    def kill(self):
        #print("Killed after timing out in {} ms".format(self._stopwatch.DeltaTimeMs()))
        self._process.kill()

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

        self._argBuilder = DictBuilder()

        self._players = dict()

        self._threads = list()

        self._turn = 0

        self._stopwatch = TimeManager()

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


        if self._turn >= 0 and self._turn != 1 :
            # Called before the start of the countdown and each turn after the first one
            self.handlePlayerPolling()

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
        # The processes are destroyed each time.
        # Should be improvable to preserve the processes and only restart them instead of creating
        self._threads = list()

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

            for bot in self._teams[team_id]["bots"].values():
                self._argBuilder.add_bot(bot)

            self._argBuilder.end_argument()

            pollingData = self._argBuilder.get_result()
            
            # This part could be improved by conserving Process inside PlayerProcess object
            try:
                self._threads.append(PlayerProcess(self, team_id, player, pollingData))
            except:
                print("WARNING: Could not start polling thread for team {} ! Their actions will not be applied.".format(team_id))
            
        # Start each player's computation and sleep while they should be processing
        # After we are done sleeping, two things can occur:
        #   1 - If we are in countdown phase : Players will be able to compute for the duration of the countdown
        #   2 - Else : Players will be immediatly checked and killed. If they did not finish, their (individual) turn is invalid; not affecting other players.
        for thread in self._threads:
            thread.start()

        # The entire computation of a player must be done during this sleep (if not in countdown phase)
        TimeManager.Sleep(int(self._ruleset["ThinkTimeMs"]))

    def handleNormalTurn(self):
        """
        This stops players computing and processes their response
        """

        # This occurs right after sleeping during ThinkTimeMs milliseconds
        for thread in self._threads:
            thread.check()
            thread.kill()
                
        self._turn += 1

        # Interpret players orders
        for team_id in self.teams_data.keys():
            if(self.teams_data[team_id] == None):
                print("Did not get a response from player {}".format(team_id))
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

    def handleFirstTurn(self):
        """
        TODO
        """
        self._turn = 1
        for thread in self._threads:
            thread.check()
        for team_id in self.teams_data.keys():
            if(self.teams_data[team_id] == None):
                print(team_id + " not ready")

    def handleStartingCountdown(self):
        """
        TODO
        """
        print("Game starting in {}s ...".format(int(self._ruleset["StartCountdownSeconds"]) * 1000 - int(self._ruleset["ThinkTimeMs"]) - self._stopwatch.PeekDeltaTimeMs()))

        for thread in self._threads:
            thread.check()
        for team_id in self.teams_data.keys():
            if(self.teams_data[team_id] == None):
                print(team_id + " not ready")

    def checkItemsPickup(self):
        """
        TODO
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