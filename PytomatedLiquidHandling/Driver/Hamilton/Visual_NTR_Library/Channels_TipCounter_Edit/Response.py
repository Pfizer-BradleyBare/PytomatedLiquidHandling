from dataclasses import dataclass

from typing_extensions import TypedDict

from ...Backend import HamiltonResponseABC


class SequencePositionDict(TypedDict):
    LabwareID: str
    PositionID: str


class Response(HamiltonResponseABC):
    AvailablePositions: list[SequencePositionDict]
