from abc import ABC, abstractmethod


class ServerHandlerABC(ABC):
    def __init__(self):
        self.IsAliveFlag: bool = True

    def IsAlive(self) -> bool:
        return self.IsAliveFlag

    @abstractmethod
    def GetEndpoints(self) -> tuple:
        ...

    @abstractmethod
    def Kill(self):
        ...
