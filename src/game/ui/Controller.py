
class Controller:
    """
    Interface for the Game Controller, which handles interface interactions.
    """

    def __init__(self):
        """ 
        The constructor for a Controller. 
        """
        raise NotImplementedError

    def tick(self, deltaTime):
        """ 
        Called each tick to refresh the Controller.
  
        Parameters: 
           deltaTime (int): The time in milliseconds since the last call to this function.
        """
        raise NotImplementedError