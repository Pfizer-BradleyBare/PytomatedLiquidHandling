from pydantic import dataclasses

from plh.device.HAMILTON.backend import HamiltonResponseBase


@dataclasses.dataclass(kw_only=True)
class LabwarePosition:
    XPosition: float
    YPosition: float
    ZPosition: float
    ZRotation: float


@dataclasses.dataclass(kw_only=True)
class Response(HamiltonResponseBase):
    LabwarePositions: list[LabwarePosition]