
from service.TimeManager import TimeManager
from multiprocessing import Process, Queue
import sys

class PlayerProcess():
    """
    Handles the process of a player

    Attributes:
        process (Process) : The process in which player polling will be ran
        target (function) : The function that will be executed in the Process
        args (tuple) : Arguments sent to the process at execution

        data (any) : The data to be sent to the Process
        
        dataQueue (Queue) : The queue used to send data to the process
        resultQueue (Queue) : The queue used to get the result from the process

        model (Model) : The game model, containing teamsData in which we place the response
        teamId (string) : The team identifier, for placing the result in the correct teamsData

        stopwatch (TimeManager) : Used to monitor process response time
    """

    def __init__(self, model, teamId, player):
        """
        Creates a new process to run a player's tick.

        Arguments:
            model (Model) : Access to the model of the game
            teamId (string) : The team to operate
            player (Player) : The player to call
        """

        self._target = runPlayerProcess

        self._data = None
        self._dataQueue = Queue()
        self._resultQueue = Queue()

        self._model = model
        self._teamId = teamId

        self._stopwatch = TimeManager()

        self._args = (self._dataQueue, self._resultQueue, player)

        self._process = Process(target=self._target, args=self._args)

        self.lastResponseTime = None

    def setData(self, pollingData):
        """
        Changes what data will be put in the queue for the next call to execute.

        Arguments:
            pollingData (any) : Correctly formatted data that can be read by a Player
        """
        self._data = pollingData

    def execute(self):
        """
        Places the data in the queue, which will usually trigger the process's next loop.

        Use setData to change what will be read by the player.
        """
        self._stopwatch.StartTimer()
        self._dataQueue.put(self._data)

    def check(self):
        """
        Checks if the player has sent a response, and places it in teamsData[team]

        If no response is given, None is placed.
        """
        try: 
            result = self._resultQueue.get(False)
            self.lastResponseTime = self._stopwatch.DeltaTimeMs()
            
        except:
            if self._model.teamsData[self._teamId] == None:
                result = None
            else:
                result = self._model.teamsData[self._teamId]

        self._model.teamsData[self._teamId] = result

    def start(self):
        """
        Starts the process hosting the player. Should only be called once in a game.
        """
        self._process.start()

    def join(self, timeout = None):
        """
        Waits until process termination.
        """
        self._process.join(timeout)

    def kill(self):
        """
        Kills the process hosting the player. Should only be called once the game is over.
        """
        self._process.kill()

def runPlayerProcess(dataQueue, resultQueue, player):
        while True:
            pollingData = dataQueue.get()
            resultQueue.put(player.poll(pollingData))