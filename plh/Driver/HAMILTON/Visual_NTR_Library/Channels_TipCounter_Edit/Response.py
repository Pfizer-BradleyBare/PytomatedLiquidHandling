import dataclasses

from typing_extensions import TypedDict

from ...Backend import HamiltonResponseBase


class SequencePositionDict(TypedDict):
    LabwareID: str
    PositionID: str


import dataclasses


@dataclasses.dataclass(kw_only=True)
class Response(HamiltonResponseBase):
    AvailablePositions: list[SequencePositionDict]
