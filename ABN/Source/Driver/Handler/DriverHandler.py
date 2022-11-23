from ...Tools.AbstractClasses import ServerHandlerABC
from ..Tools.Command.Command import Command
from ..Tools.Command.CommandTracker import CommandTracker
from .Endpoints import IsReady, Request, Respond


class DriverHandler(ServerHandlerABC):
    def __init__(self):
        self.CommandTrackerInstance: CommandTracker = CommandTracker()

    def GetEndpoints(self) -> tuple:
        urls = ()
        urls += IsReady.urls
        urls += Request.urls
        urls += Respond.urls
        return urls

    def Kill(self):
        if self.CommandTrackerInstance.GetNumObjects() != 0:
            self.CommandTrackerInstance.GetObjectsAsList()[0].ResponseEvent.set()

    def ExecuteCommand(self, CommandInstance: Command):
        self.CommandTrackerInstance.ManualLoad(CommandInstance)

    def WaitOnExecute(self, timeout: float | None = None) -> Command:
        if self.CommandTrackerInstance.GetNumObjects() == 0:
            raise Exception("No Command running. You did something wrong.")

        CommandInstance = self.CommandTrackerInstance.GetObjectsAsList()[0]

        CommandInstance.ResponseEvent.wait(timeout)
        self.CommandTrackerInstance.ManualUnload(CommandInstance)
        return CommandInstance
