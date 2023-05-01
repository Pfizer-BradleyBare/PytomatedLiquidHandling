from ...Server.Handler import GetHandler as ServerGetHandler
from ...Server.Handler import Handler as ServerHandler
from ...Tools.AbstractClasses import ServerHandlerABC
from ...Tools.Logger import Logger
from ..Tools import Command
from .Endpoints import Request, Respond


class Handler(ServerHandlerABC):
    def __init__(self, LoggerInstance: Logger):
        ServerHandlerABC.__init__(self, LoggerInstance)

        global _HandlerInstance
        _HandlerInstance = self

        try:
            ServerGetHandler()
        except:
            ServerHandler(LoggerInstance)

        self.CommandTrackerInstance: Command.CommandTracker = Command.CommandTracker()

    def GetUniqueIdentifier(self) -> str:
        return "Driver"

    def GetEndpoints(self) -> tuple:
        urls = ()
        urls += Request.urls
        urls += Respond.urls
        return urls

    def Kill(self):
        if self.CommandTrackerInstance.GetNumObjects() != 0:
            self.CommandTrackerInstance.GetObjectsAsList()[0].ResponseEvent.set()


_HandlerInstance: Handler | None = None


def GetHandler() -> Handler:
    if _HandlerInstance is None:
        raise Exception("Driver Handler not created. Please Create")

    else:
        return _HandlerInstance
