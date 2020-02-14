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