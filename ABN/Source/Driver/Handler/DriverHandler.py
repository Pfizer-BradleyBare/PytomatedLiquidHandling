from ...Tools.AbstractClasses import ServerHandlerABC
from ..Tools import Command, CommandTracker, ExecuteCallback
from .Endpoints import IsReady, Request, Respond


class DriverHandler(ServerHandlerABC):
    def __init__(self):
        self.CommandTrackerInstance: CommandTracker = CommandTracker()

    def GetName(self) -> str:
        return "Driver"

    def GetEndpoints(self) -> tuple:
        urls = ()
        urls += IsReady.urls
        urls += Request.urls
        urls += Respond.urls
        return urls

    def Kill(self):
        if self.CommandTrackerInstance.GetNumObjects() != 0:
            self.CommandTrackerInstance.GetObjectsAsList()[0].ResponseEvent.set()

    def ExecuteCommand(
        self, CommandInstance: Command, Timeout: float | None = None
    ) -> bool:

        self.CommandTrackerInstance.ManualLoad(CommandInstance)

        TimeoutFlag = CommandInstance.ResponseEvent.wait(Timeout)

        if TimeoutFlag is True:  # This means it did not timeout

            ExecuteCallback(
                CommandInstance.CallbackFunction,
                CommandInstance,
                CommandInstance.CallbackArgs,
            )

        self.CommandTrackerInstance.ManualUnload(CommandInstance)

        return TimeoutFlag
