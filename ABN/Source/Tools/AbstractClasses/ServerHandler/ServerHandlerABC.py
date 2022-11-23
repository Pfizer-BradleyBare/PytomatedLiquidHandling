from abc import abstractmethod


class ServerHandlerABC:
    def __init__(self):
        pass

    @abstractmethod
    def GetEndpoints(self) -> tuple:
        raise NotImplementedError

    @abstractmethod
    def Kill(self):
        raise NotImplementedError
