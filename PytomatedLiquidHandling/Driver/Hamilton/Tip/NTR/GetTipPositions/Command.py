from dataclasses import dataclass

from .....Tools.AbstractClasses import CommandOptions
from ....Backend import HamiltonActionCommandABC
from .Options import Options


@HamiltonActionCommandABC.Decorator_Command(__file__)
@dataclass
class Command(CommandOptions[Options], HamiltonActionCommandABC):
    ...

    class Response(HamiltonActionCommandABC.Response):
        @HamiltonActionCommandABC.Response.Decorator_ExpectedResponseProperty(
            SuccessProperty=True
        )
        def GetTipPositions(self) -> list[int]:
            ...
