
# This class may interact with the game
class Player:

    def __init__(self, map):
        raise NotImplementedError

    # Poll the player in order to obtain its current actions
    def poll(self, pollingData):
        raise NotImplementedError