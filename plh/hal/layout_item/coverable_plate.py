from __future__ import annotations

from pydantic import dataclasses, field_validator

from plh.hal import labware

from .layout_item_base import *
from .layout_item_base import LayoutItemBase
from .lid import Lid


@dataclasses.dataclass(kw_only=True)
class CoverablePlate(LayoutItemBase):
    """A plate that can be covered and uncovered."""

    labware: labware.PipettableLabware
    """Plates are by definition possible to pipetted to/from."""

    lid: Lid
    """Lid object associated with this plate."""

    @field_validator("lid", mode="before")
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
