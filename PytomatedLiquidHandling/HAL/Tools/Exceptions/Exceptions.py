from dataclasses import dataclass
from PytomatedLiquidHandling.HAL import Labware


@dataclass
class LabwareNotSupportedError(BaseException):
    Labwares: list[Labware.Base.LabwareABC]
