import dataclasses

from typing_extensions import TypedDict

from plh.driver.HAMILTON.backend import HamiltonResponseBase


class SequencePositionDict(TypedDict):
    LabwareID: str
    PositionID: str


@dataclasses.dataclass(kw_only=True)
class Response(HamiltonResponseBase):
    AvailablePositions: list[SequencePositionDict]
