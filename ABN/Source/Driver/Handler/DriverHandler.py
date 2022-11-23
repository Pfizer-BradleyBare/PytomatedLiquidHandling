from ...Tools.AbstractClasses import ServerHandlerABC
from ..Tools.Command.CommandTracker import CommandTracker
from .Endpoints import IsReady, Request, Respond


class DriverHandler(ServerHandlerABC):
    def __init__(self):
        self.CommandTrackerInstance: CommandTracker = CommandTracker()

    def GetCommandTracker(self) -> CommandTracker:
        return self.CommandTrackerInstance

    def GetEndpoints(self) -> tuple:
        urls = ()
        urls += IsReady.urls
        urls += Request.urls
        urls += Respond.urls
        return urls

    def Kill(self):
        if self.CommandTrackerInstance.GetNumObjects() != 0:
            self.CommandTrackerInstance.GetObjectsAsList()[0].ResponseEvent.set()
