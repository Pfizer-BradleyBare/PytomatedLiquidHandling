from abc import abstractmethod
from threading import Event

from ....Server.Globals import GetDriverHandler
from ....Tools.AbstractClasses import ObjectABC
from .Response.Response import Response


class Command(ObjectABC):
    def __init__(
        self,
        Name: str,
        CustomErrorHandling: bool,
    ):
        self.Name: str = Name
        self.CustomErrorHandling: bool = CustomErrorHandling

        self.ResponseInstance: Response | None = None
        self.ResponseEvent: Event = Event()

    def GetName(self) -> str:
        return self.Name

    def GetResponse(self) -> Response:
        if self.ResponseInstance is None:
            raise Exception("Response not set. Did the command timeout?")

        return self.ResponseInstance

    def Execute(self, Timeout: float | None = None):
        TimeoutFlag = True

        CommandTrackerInstance = (
            GetDriverHandler().CommandTrackerInstance  # type:ignore
        )

        if type(self).__name__ != "NOPCommand":

            CommandTrackerInstance.ManualLoad(self)

            TimeoutFlag = self.ResponseEvent.wait(Timeout)

            CommandTrackerInstance.ManualUnload(self)

        if TimeoutFlag is True:  # This means it did not timeout

            if self.ResponseInstance is None:
                raise Exception("Response is not set. This should never happen...")

            if self.ResponseInstance.State is False:
                if self.CustomErrorHandling is not False:
                    self.HandleErrors()
            # If response indicates a failure then we need to run error handling if it is set.
            # Most error handling will just rerun the step. FIY

        else:
            raise Exception("Command Timed out. Uh oh!")

    @abstractmethod
    def GetModuleName(self) -> str:
        ...

    @abstractmethod
    def GetCommandName(self) -> str:
        ...

    @abstractmethod
    def GetResponseKeys(self) -> list[str]:
        ...

    @abstractmethod
    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        ...

    @abstractmethod
    def HandleErrors(self):
        ...
