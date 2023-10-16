from dataclasses import dataclass

from ....Backend import HamiltonResponseABC


@dataclass
class Response(HamiltonResponseABC):
    @HamiltonResponseABC.Decorator_ExpectedResponseProperty(SuccessProperty=True)
    def GetAvailablePositions(self) -> list[tuple[str, str]]:
        ...
