
class View:
    """
    Interface for the Game View, which displays the current state of the game.

    Attributes:
        model (Model): The data to represent.
    """

    def __init__(self, model):
        """ 
        The constructor for a View. 
  
        Parameters: 
           model (Model): The data to represent.
        """
        raise NotImplementedError

    def tick(self, deltaTime):
        """ 
        Called each tick to refresh the View.
  
        Parameters: 
           deltaTime (int): The time in milliseconds since the last call to this function.
        """
        raise NotImplementedError