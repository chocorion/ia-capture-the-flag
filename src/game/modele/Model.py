
# Interface for the Model
class Model:

    # Initialize game data
    def __init__(self):
        raise NotImplementedError

    # Update and handle the game data
    def tick(self, deltaTime):
        raise NotImplementedError

    # Add a new player to the game and provide it with necessary data
    def register(self, player):
        raise NotImplementedError