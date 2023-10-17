from dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Hamilton import Tools

from ....Backend import HamiltonResponseABC


@dataclass
class Response(HamiltonResponseABC):
    @HamiltonResponseABC.Decorator_ExpectedResponseProperty(SuccessProperty=True)
    def GetAvailablePositions(self) -> list[Tools.SequencePositionDict]:
        ...
