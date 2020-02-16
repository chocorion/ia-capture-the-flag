
class Model:
    """
    Interface for the Game Model, which stores the current state of the game.
    """

    def __init__(self, Player1, Player2):
        """
        Initialize game data.
  
        Parameters: 
           Player1 (Player): The player in control of the Red team.
           Player2 (Player): The player in control of the Blue team.
        """
        raise NotImplementedError

    def tick(self, deltaTime):
        """
        Update and handle the game data.
  
        Parameters: 
           deltaTime (int): The time in milliseconds since the last call to this function.
        """
        raise NotImplementedError

    def register(self, player):
        """
        Add a new player to the game and provide it with necessary data.

        Returns:
            data : Contains all the data a player can have at it's init.
        """
        raise NotImplementedError