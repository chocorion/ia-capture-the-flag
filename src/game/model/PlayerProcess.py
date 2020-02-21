
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
        
        data_queue (Queue) : The queue used to send data to the process
        result_queue (Queue) : The queue used to get the result from the process

        model (Model) : The game model, containing teams_data in which we place the response
        team_id (string) : The team identifier, for placing the result in the correct teams_data

        stopwatch (TimeManager) : Used to monitor process response time
    """

    def __init__(self, model, team_id, player):
        """
        Creates a new process to run a player's tick.

        Arguments:
            model (Model) : Access to the model of the game
            team_id (string) : The team to operate
            player (Player) : The player to call
        """

        self._target = runPlayerProcess

        self._data = None
        self._data_queue = Queue()
        self._result_queue = Queue()

        self._model = model
        self._team_id = team_id

        self._stopwatch = TimeManager()

        self._args = (self._data_queue, self._result_queue, player)

        self._process = Process(target=self._target, args=self._args)

        self.last_response_time = None

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
        self._data_queue.put(self._data)

    def check(self):
        """
        Checks if the player has sent a response, and places it in teams_data[team]

        If no response is given, None is placed.
        """
        try: 
            result = self._result_queue.get(False)
            self.last_response_time = self._stopwatch.DeltaTimeMs()
            
        except:
            if self._model.teams_data[self._team_id] == None:
                result = None
            else:
                result = self._model.teams_data[self._team_id]

        self._model.teams_data[self._team_id] = result

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

def runPlayerProcess(data_queue, result_queue, player):
        while True:
            pollingData = data_queue.get()
            result_queue.put(player.poll(pollingData))