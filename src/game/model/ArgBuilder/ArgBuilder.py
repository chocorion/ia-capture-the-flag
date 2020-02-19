from abc import (ABCMeta, abstractmethod)

class ArgBuilder(metaclass=ABCMeta):
    """
    This class represent the interface to implements for building the
    argument of player's polling.
    """

    @abstractmethod
    def begin_argument(self):
        """
        Begin a new argument. All datas about old argument will be lost.
        """
        ...

    @abstractmethod
    def end_argument(self):
        """
        End the argument. Argument must be valid at this point.
        """
        ...

    @abstractmethod
    def add_bot(self, bot):
        """
        Add a new bot to the argument.

        Parameters:
            bot (Bot): domain.Bot
        """
        ...