from ...Tools.AbstractClasses import ServerHandlerABC
from ...Tools.Logger import Logger
from .Endpoints import IsActive, Kill


class Handler(ServerHandlerABC):
    def __init__(self, LoggerInstance: Logger):
        ServerHandlerABC.__init__(self, LoggerInstance)

        global _HandlerInstance
        _HandlerInstance = self

    def GetName(self) -> str:
        return "Server"

    def GetEndpoints(self) -> tuple:
        urls = ()
        urls += IsActive.urls
        urls += Kill.urls
        return urls

    def Kill(self):
        pass


_HandlerInstance: Handler | None = None


def GetHandler() -> Handler:

    if _HandlerInstance is None:
        raise Exception("Driver Handler not created. Please Create")

    else:
        return _HandlerInstance
