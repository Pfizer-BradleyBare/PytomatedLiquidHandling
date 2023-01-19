from ...Tools.AbstractClasses import ServerHandlerABC
from ..Tools import Command, CommandTracker, ExecuteCallback
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

    def ExecuteCommand(
        self, CommandInstance: Command, Timeout: float | None = None
    ) -> bool:

        TimeoutFlag = True

        if type(CommandInstance).__name__ != "NOPCommand":

            self.CommandTrackerInstance.ManualLoad(CommandInstance)

            TimeoutFlag = CommandInstance.ResponseEvent.wait(Timeout)

            self.CommandTrackerInstance.ManualUnload(CommandInstance)

        if TimeoutFlag is True:  # This means it did not timeout

            if CommandInstance.ResponseInstance is None:
                raise Exception("Response is not set. This should never happen...")

            ExecuteCallback(
                CommandInstance.CallbackFunction,
                CommandInstance,
                CommandInstance.CallbackArgs,
            )
            # Callback is executed before the error handling. Callback is responsible for checking for errors as well

            if CommandInstance.ResponseInstance.State is False:
                if CommandInstance.CustomErrorHandlingFunction is not None:
                    CommandInstance.CustomErrorHandlingFunction(CommandInstance)
            # If response indicates a failure then we need to run error handling if it is set.
            # Most error handling will just rerun the step. FIY

        return TimeoutFlag
