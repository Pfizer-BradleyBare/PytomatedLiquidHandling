from pydantic import dataclasses

from plh.hal import Labware

from .Base import LayoutItemABC


@dataclasses.dataclass(kw_only=True)
class VacuumManifold(LayoutItemABC):
    Labware: Labware.NonPipettableLabware
