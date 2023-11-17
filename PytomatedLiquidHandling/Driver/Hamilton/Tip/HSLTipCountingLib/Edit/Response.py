from dataclasses import dataclass
from typing import TypedDict

from ....Backend import HamiltonResponseABC


class SequencePositionDict(TypedDict):
    LabwareID: str
    PositionID: str


@dataclass
class Response(HamiltonResponseABC):
    AvailablePositions: list[SequencePositionDict]
