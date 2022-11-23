from abc import abstractmethod


class ServerHandlerABC:
    def __init__(self):
        self.IsAliveFlag: bool = True

    def IsAlive(self) -> bool:
        return self.IsAliveFlag

    @abstractmethod
    def GetEndpoints(self) -> tuple:
        raise NotImplementedError

    @abstractmethod
    def Kill(self):
        raise NotImplementedError
