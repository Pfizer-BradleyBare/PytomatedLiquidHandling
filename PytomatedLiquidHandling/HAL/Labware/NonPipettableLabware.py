from pydantic.dataclasses import dataclass

from .Base import LabwareABC


@dataclass
class NonPipettableLabware(LabwareABC):
    ...
