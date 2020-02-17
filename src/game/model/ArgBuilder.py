from abc import (ABCMeta, abstractmethod)

class ArgBuilder(ABCMeta):
    @abstractmethod
    def reset(self):
        ...
    
    @abstractmethod
    def begin_argument(self):
        ...

    @abstractmethod
    def end_argument(self):
        ...

    @abstractmethod
    def add_bot(self):
        ...

    @abstractmethod
    def add_life(self):
        ...

    @abstractmethod
    def add_flag(self):
        ...

    @abstractmethod
    def add_cooldown(self):
        ...