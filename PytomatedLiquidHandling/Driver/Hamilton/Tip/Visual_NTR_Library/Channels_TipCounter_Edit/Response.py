from dataclasses import dataclass
from typing import TypedDict

from ....Backend import HamiltonResponseABC


class SequencePositionDict(TypedDict):
    LabwareID: str
    PositionID: str


@dataclass
class Response(HamiltonResponseABC):
    @HamiltonResponseABC.Decorator_ExpectedResponseProperty(SuccessProperty=True)
    def GetAvailablePositions(self) -> list[SequencePositionDict]:
        ...
