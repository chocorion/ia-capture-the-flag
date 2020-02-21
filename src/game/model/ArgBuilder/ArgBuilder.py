from abc import (ABCMeta, abstractmethod)

class ArgBuilder(metaclass=ABCMeta):
    """
    This class represent the interface to implements for building the
    argument of player's polling.
    """

    @abstractmethod
    def beginArgument(self):
        """
        Begin a new argument. All datas about old argument will be lost.
        """
        ...

    @abstractmethod
    def endArgument(self):
        """
        End the argument. Argument must be valid at this point.
        """
        ...

    @abstractmethod
    def addBot(self, bot):
        """
        Add a new bot to the argument.

        Parameters:
            bot (Bot): domain.Bot
        """
        ...

    @abstractmethod
    def addFlag(self, team, currentPosition):
        """
        Add a flag event to the argument.

        Parameters :
            team (int): flag owner
            currentPosition (int, int): x and y coord of the flag
        """