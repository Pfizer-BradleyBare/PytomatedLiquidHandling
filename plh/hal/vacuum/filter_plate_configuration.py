from __future__ import annotations

from pydantic import dataclasses, field_validator

from plh.hal import layout_item


@dataclasses.dataclass(kw_only=True)
class DefaultVacuumPressures:
    """Facilitates simple selection of vacuum pressures. Each filter plate has "ideal" pressures.
    NOTE: This is subjective."""

    low: float
    """Slow flow of liquid through the filter plate."""

    medium: float
    """Average flow of liquid through the filter plate."""

    high: float
    """Fast flow of liquid through the filter plate."""


@dataclasses.dataclass(kw_only=True)
class FilterPlateConfiguration:
    """Compatibilities with a certain vacuum filter plate."""

    filter_plate: layout_item.FilterPlate | layout_item.CoverableFilterPlate
    """The filter plate."""

    collection_plate: layout_item.Plate
    """The compatible plate for eluate collection."""

    max_pressure: float
    """The max pressure of the filter plate. Typically this the pressure at which you have filter flex occuring and airflow skyrockets."""

    default_vacuum_pressures: DefaultVacuumPressures
    """Default vacuum pressures object."""

    @field_validator("filter_plate", "collection_plate", mode="before")
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
