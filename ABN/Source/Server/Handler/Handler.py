from ...Tools.AbstractClasses import ServerHandlerABC
from .Endpoints import IsActive, Kill


class Handler(ServerHandlerABC):
    def GetName(self) -> str:
        return "Server"

    def GetEndpoints(self) -> tuple:
        urls = ()
        urls += IsActive.urls
        urls += Kill.urls
        return urls

    def Kill(self):
        pass
