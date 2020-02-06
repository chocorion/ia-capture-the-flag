
# Interface for the Game Controller
# Handles the game events and interactions
class Controller:

    def __init__(self):
        raise NotImplementedError

    # Handle events and interactions
    def tick(self, deltaTime):
        raise NotImplementedError