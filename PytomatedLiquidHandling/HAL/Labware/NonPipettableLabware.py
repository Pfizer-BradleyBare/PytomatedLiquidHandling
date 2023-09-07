from dataclasses import dataclass

from .Base import Dimensions, LabwareABC


@dataclass
class NonPipettableLabware(LabwareABC):
    ...
