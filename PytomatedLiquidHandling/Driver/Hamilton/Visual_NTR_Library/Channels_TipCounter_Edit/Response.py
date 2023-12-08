from pydantic import dataclasses
from typing_extensions import TypedDict

from ...Backend import HamiltonResponseABC


class SequencePositionDict(TypedDict):
    LabwareID: str
    PositionID: str


from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class Response(HamiltonResponseABC):
    AvailablePositions: list[SequencePositionDict]
