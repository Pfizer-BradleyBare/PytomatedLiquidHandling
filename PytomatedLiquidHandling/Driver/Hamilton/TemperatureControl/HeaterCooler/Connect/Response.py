from ....Backend import HamiltonResponseABC
from dataclasses import dataclass


@dataclass
class Response(HamiltonResponseABC):
    @HamiltonResponseABC.Decorator_ExpectedResponseProperty(SuccessProperty=True)
    def GetHandleID(self) -> str:
        ...
