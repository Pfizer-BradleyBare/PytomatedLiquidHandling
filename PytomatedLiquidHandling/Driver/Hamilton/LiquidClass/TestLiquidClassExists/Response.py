from ...Backend import HamiltonResponseABC
from dataclasses import dataclass


@dataclass
class Response(HamiltonResponseABC):
    HamiltonResponseABC.Decorator_ExpectedResponseProperty(ErrorProperty=True)

    def GetFailedLiquidClasses(self) -> list[str]:
        ...
