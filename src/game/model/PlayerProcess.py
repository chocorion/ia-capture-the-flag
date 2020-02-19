
from service.TimeManager import TimeManager
from multiprocessing import Process, Queue
import sys

class PlayerProcess():
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

    def setData(self, pollingData):
        self._data = pollingData

    def execute(self):
        self._stopwatch.StartTimer()
        self._data_queue.put(self._data)

    def check(self):
        try: 
            result = self._result_queue.get(False)

            print("Result obtained in {} ms".format(self._stopwatch.DeltaTimeMs()))
        except:
            if self._model.teams_data[self._team_id] == None:
                result = None
            else:
                result = self._model.teams_data[self._team_id]

        self._model.teams_data[self._team_id] = result

    def start(self):
        self._process.start()

    def join(self, timeout):
        self._process.join(timeout)

    def kill(self):
        self._process.kill()

def runPlayerProcess(data_queue, result_queue, player):
        while True:
            pollingData = data_queue.get()
            result_queue.put(player.poll(pollingData))