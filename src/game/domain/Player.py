
# This class may interact with the game
class Player:

    def __init__(self, map):
        raise NotImplementedError

    # Poll the player for its current actions
    def poll(self, pollingData):
        raise NotImplementedError