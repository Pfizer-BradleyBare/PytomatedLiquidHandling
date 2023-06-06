from ....Tools.AbstractClasses import (
    CommandOptionsTracker,
    Exception_Unhandled,
    ExceptionABC,
)
from dataclasses import dataclass
from ...Backend import HamiltonActionCommandABC
from .OptionsTracker import OptionsTracker


@HamiltonActionCommandABC.Decorator_Command(__file__)
@dataclass
class Command(CommandOptionsTracker[OptionsTracker], HamiltonActionCommandABC):
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


@dataclass
class Exception_LiquidClassDoesNotExist(ExceptionABC[Command, Command.Response]):
    ...
