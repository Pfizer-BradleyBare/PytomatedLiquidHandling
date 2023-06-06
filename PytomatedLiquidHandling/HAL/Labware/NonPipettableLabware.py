from .BaseLabware import Dimensions, LabwareABC
from dataclasses import dataclass


@dataclass
class NonPipettableLabware(LabwareABC):
    ...
