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
    def add_bot(self):
        """
        Add a new bot to the argument.
        """
        ...

    @abstractmethod
    def add_life(self, life_amount):
        """
        Add life parameter for the current bot.

        Parameters:
            life_amount (int) : Total life of the current bot.
        """
        ...

    @abstractmethod
    def add_flag(self, flag_num):
        """
        Add flag parameter for the current bot.

        Parameters:
            flag_num (int) : 
                0 if bot doesn't have any flag.
                1 if the bot has flag of this team.
                2 if the bot has enemy flag.
        """
        ...

    @abstractmethod
    def add_cooldown(self, cooldown_millis):
        """
        Add cooldown for current bot.

        Parameters :
            cooldown_millis (int) : Cooldown in milliseconds.
        """
        ...