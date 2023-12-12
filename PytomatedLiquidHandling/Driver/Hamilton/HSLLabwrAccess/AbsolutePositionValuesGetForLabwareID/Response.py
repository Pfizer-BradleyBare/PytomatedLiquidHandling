from ...Backend import HamiltonResponseABC
from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class LabwarePosition:
    XPosition: float
    YPosition: float
    ZPosition: float
    ZRotation: float


@dataclasses.dataclass(kw_only=True)
class Response(HamiltonResponseABC):
    LabwarePositions: list[LabwarePosition]
