from .....Tools.AbstractClasses import CommandOptions
from ....Backend import HamiltonStateCommandABC
from .Options import Options


from dataclasses import dataclass


@HamiltonStateCommandABC.Decorator_Command(__file__)
@dataclass
class Command(CommandOptions[Options], HamiltonStateCommandABC):
    def ParseResponseRaiseExceptions(
        self, ResponseInstance: HamiltonStateCommandABC.Response
    ):
        HamiltonStateCommandABC.ParseResponseRaiseExceptions(self, ResponseInstance)

    class Response(HamiltonStateCommandABC.Response):
        @HamiltonStateCommandABC.Response.Decorator_ExpectedSuccessResponseProperty
        def GetNumRemaining(self) -> int:
            ...
