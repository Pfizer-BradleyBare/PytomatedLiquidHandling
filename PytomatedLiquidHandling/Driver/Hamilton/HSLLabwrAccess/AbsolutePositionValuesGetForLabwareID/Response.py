from pydantic import BaseModel

from ...Backend import HamiltonResponseABC


class LabwarePosition(BaseModel):
    XPosition: float
    YPosition: float
    ZPosition: float
    ZRotation: float


from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class Response(HamiltonResponseABC):
    LabwarePositions: list[LabwarePosition]
