from __future__ import annotations

from pydantic import Field, dataclasses, field_validator

from plh.hal import labware

from .layout_item_base import LayoutItemBase
from .lid import Lid


@dataclasses.dataclass(kw_only=True)
class CoverablePlate(LayoutItemBase):
    labware: labware.PipettableLabware
    lid: Lid
    is_covered: bool = Field(exclude=True, default=False)

    @field_validator("Lid", mode="before")
    @classmethod
    def __lid_validate(
        cls: type[CoverablePlate],
        v: str | LayoutItemBase,
    ) -> LayoutItemBase:
        if isinstance(v, LayoutItemBase):
            return v

        from . import devices

        objects = devices
        identifier = v

        if identifier not in objects:
            raise ValueError(
                identifier
                + " is not found in "
                + LayoutItemBase.__name__
                + " objects.",
            )

        return objects[identifier]
