from .....Tools.AbstractClasses import CommandOptions
from ....Backend import HamiltonActionCommandABC
from .Options import Options


from dataclasses import dataclass


@HamiltonActionCommandABC.Decorator_Command(__file__)
@dataclass
class Command(CommandOptions[Options], HamiltonActionCommandABC):
    def ParseResponseRaiseExceptions(
        self, ResponseInstance: HamiltonActionCommandABC.Response
    ):
        HamiltonActionCommandABC.ParseResponseRaiseExceptions(self, ResponseInstance)

    class Response(HamiltonActionCommandABC.Response):
        @HamiltonActionCommandABC.Response.Decorator_ExpectedSuccessResponseProperty
        def GetHandleID(self) -> int:
            ...
