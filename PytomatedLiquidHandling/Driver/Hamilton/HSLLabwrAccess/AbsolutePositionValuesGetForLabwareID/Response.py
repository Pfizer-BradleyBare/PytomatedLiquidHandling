from pydantic import BaseModel

from ...Backend import HamiltonResponseABC


class LabwarePosition(BaseModel):
    XPosition: float
    YPosition: float
    ZPosition: float
    ZRotation: float


class Response(HamiltonResponseABC):
    LabwarePositions: list[LabwarePosition]
