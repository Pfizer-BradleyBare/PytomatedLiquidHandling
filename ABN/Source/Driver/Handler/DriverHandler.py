from ...Tools.AbstractClasses import ServerHandlerABC
from ..Tools.Command import CommandTracker
from .Endpoints import Request, Respond


class DriverHandler(ServerHandlerABC):
    def __init__(self):
        ServerHandlerABC.__init__(self)
        self.CommandTrackerInstance: CommandTracker = CommandTracker()

    def GetName(self) -> str:
        return "Driver"

    def GetEndpoints(self) -> tuple:
        urls = ()
        urls += Request.urls
        urls += Respond.urls
        return urls

    def Kill(self):
        if self.CommandTrackerInstance.GetNumObjects() != 0:
            self.CommandTrackerInstance.GetObjectsAsList()[0].ResponseEvent.set()
