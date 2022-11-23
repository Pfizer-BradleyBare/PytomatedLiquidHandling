from ...Tools.AbstractClasses import ServerHandlerABC
from .Endpoints import IsActive, Kill


class ServerHandler(ServerHandlerABC):
    def __init__(self):
        self.IsAliveFlag: bool = True

    def IsAlive(self) -> bool:
        return self.IsAliveFlag

    def GetEndpoints(self) -> tuple:
        urls = ()
        urls += IsActive.urls
        urls += Kill.urls
        return urls

    def Kill(self):
        pass
