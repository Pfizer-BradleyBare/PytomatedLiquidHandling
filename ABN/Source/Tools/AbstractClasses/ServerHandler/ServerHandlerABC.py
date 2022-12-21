from abc import abstractmethod

from ..Object.ObjectABC import ObjectABC


class ServerHandlerABC(ObjectABC):
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
