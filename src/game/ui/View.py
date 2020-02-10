
# Interface for the Game View
# Displays the current state of the game
class View:

    def __init__(self):
        raise NotImplementedError

    def tick(self, deltaTime):
        raise NotImplementedError