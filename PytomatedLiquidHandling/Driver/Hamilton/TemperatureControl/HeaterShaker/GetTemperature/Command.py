from dataclasses import dataclass

from .....Tools.AbstractClasses import CommandOptions
from ....Backend import HamiltonStateCommandABC
from .Options import Options


@dataclass
class Command(CommandOptions[Options], HamiltonStateCommandABC):
    def ParseResponseRaiseExceptions(
        self, ResponseInstance: HamiltonStateCommandABC.Response
    ):
        HamiltonStateCommandABC.ParseResponseRaiseExceptions(self, ResponseInstance)

    class Response(HamiltonStateCommandABC.Response):
        @HamiltonStateCommandABC.Response.Decorator_ExpectedResponseProperty(
            SuccessProperty=True
        )
        def GetTemperature(self) -> float:
            ...
