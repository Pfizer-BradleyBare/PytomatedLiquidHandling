from __future__ import annotations

from pydantic import dataclasses, field_validator

from plh.hal import layout_item


@dataclasses.dataclass(kw_only=True)
class DefaultVacuumPressures:
    low: float
    medium: float
    high: float


@dataclasses.dataclass(kw_only=True)
class FilterPlateConfiguration:
    filter_plate: layout_item.FilterPlate | layout_item.CoverableFilterPlate
    collection_plate: layout_item.Plate
    max_pressure: float
    default_vacuum_pressures: DefaultVacuumPressures

    @field_validator("FilterPlate", "CollectionPlate", mode="before")
    @classmethod
    def __plates_validate(
        cls: type[FilterPlateConfiguration],
        v: str | layout_item.LayoutItemBase,
    ) -> layout_item.LayoutItemBase:
        if isinstance(v, layout_item.LayoutItemBase):
            return v

        identifier = v

        objects = layout_item.devices

        if identifier not in objects:
            raise ValueError(
                identifier
                + " is not found in "
                + layout_item.LayoutItemBase.__name__
                + " objects.",
            )

        return objects[identifier]
