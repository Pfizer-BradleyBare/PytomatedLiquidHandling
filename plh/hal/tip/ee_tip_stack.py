from __future__ import annotations

from dataclasses import field

from pydantic import dataclasses, field_validator

from plh.hal import layout_item


@dataclasses.dataclass(kw_only=True)
class EETipStack:
    """Entry exit containing a stack of tips."""

    tip_rack: layout_item.TipRack
    """Rack layout item that will be used to retrieve a tip rack from the EE stack."""

    module_number: int
    """EE module number"""

    stack_number: int
    """EE stack number"""

    stack_count: int = field(init=False, default=0)
    """Number of items in the stack."""

    @field_validator("tip_rack", mode="before")
    @classmethod
    def __tip_rack_validate(
        cls: type[EETipStack],
        v: str | layout_item.LayoutItemBase,
    ) -> layout_item.LayoutItemBase:
        if isinstance(v, layout_item.LayoutItemBase):
            return v

        objects = layout_item.devices
        identifier = v

        if identifier not in objects:
            raise ValueError(
                identifier
                + " is not found in "
                + layout_item.LayoutItemBase.__name__
                + " objects.",
            )

        return objects[identifier]
