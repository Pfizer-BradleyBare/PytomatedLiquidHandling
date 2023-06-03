from ....Tools.AbstractClasses import (
    CommandOptionsTracker,
    Exception_Unhandled,
    ExceptionABC,
)
from ...Backend import HamiltonActionCommandABC
from .OptionsTracker import OptionsTracker


@HamiltonActionCommandABC.Decorator_Command(__file__)
class Command(HamiltonActionCommandABC, CommandOptionsTracker[OptionsTracker]):
    def __init__(
        self,
        *,
        CustomErrorHandling: bool,
        OptionsTrackerInstance: OptionsTracker,
        Identifier: str = "None"
    ):
        HamiltonActionCommandABC.__init__(self, Identifier, CustomErrorHandling)
        CommandOptionsTracker.__init__(self, OptionsTrackerInstance)

    class Response(HamiltonActionCommandABC.Response):
        @HamiltonActionCommandABC.Response.Decorator_ExpectedErrorResponseProperty
        def GetFailedLiquidClasses(self) -> list[str]:
            ...

    def ParseResponseRaiseExceptions(self, ResponseInstance: Response):
        HamiltonActionCommandABC.ParseResponseRaiseExceptions(self, ResponseInstance)

        if ResponseInstance.GetState() == False:
            Details = ResponseInstance.GetDetails()

            if "Liquid class does not exist" in Details:
                raise Exception_LiquidClassDoesNotExist(self, ResponseInstance)

            raise Exception_Unhandled(self, ResponseInstance)


class Exception_LiquidClassDoesNotExist(ExceptionABC[Command, Command.Response]):
    ...
