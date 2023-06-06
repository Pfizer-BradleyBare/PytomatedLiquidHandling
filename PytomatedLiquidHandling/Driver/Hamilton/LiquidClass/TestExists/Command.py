from dataclasses import dataclass
from typing import TypeVar

from ....Tools.AbstractClasses import CommandOptionsTracker
from ...Backend import HamiltonActionCommandABC
from .OptionsTracker import OptionsTracker

CommandSelf = TypeVar("CommandSelf", bound="Command")


@HamiltonActionCommandABC.Decorator_Command(__file__)
@dataclass
class Command(CommandOptionsTracker[OptionsTracker], HamiltonActionCommandABC):
    class Response(HamiltonActionCommandABC.Response):
        @HamiltonActionCommandABC.Response.Decorator_ExpectedResponseProperty(
            ErrorProperty=True
        )
        def GetFailedLiquidClasses(self) -> list[str]:
            ...

    def ParseResponseRaiseExceptions(self, ResponseInstance: Response):
        HamiltonActionCommandABC.ParseResponseRaiseExceptions(self, ResponseInstance)

        if ResponseInstance.GetState() == False:
            Details = ResponseInstance.GetDetails()

            if "Liquid class does not exist" in Details:
                raise self.Exception_LiquidClassDoesNotExist(self, ResponseInstance)

            raise self.Exception_Unhandled(self, ResponseInstance)

    @dataclass
    class Exception_LiquidClassDoesNotExist(
        HamiltonActionCommandABC.ExceptionABC[CommandSelf, Response]
    ):
        ...
