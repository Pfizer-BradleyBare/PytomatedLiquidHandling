from .Base import LabwareABC

from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class NonPipettableLabware(LabwareABC):
    ...
