from pydantic import dataclasses

from .Base import LabwareABC


@dataclasses.dataclass(kw_only=True)
class NonPipettableLabware(LabwareABC):
    ...
