from __future__ import annotations

from abc import abstractmethod

from pydantic import dataclasses, field_validator

from plh.hal import layout_item
from plh.hal.tools import HALDevice, Interface

from .filter_plate_configuration import FilterPlateConfiguration


@dataclasses.dataclass(kw_only=True, eq=False)
class VacuumBase(Interface, HALDevice):
    """Describes an on deck vacuum device."""

    manifold_park: layout_item.VacuumManifold
    """Park position for the vacuum manifold."""

    manifold_processing: layout_item.VacuumManifold
    """Vacuum position for the vacuum manifold."""

    filter_plate_configurations: dict[str, FilterPlateConfiguration]
    """Operational configurations for each filter plate supported by the vacuum device."""

    @field_validator("manifold_park", "manifold_processing", mode="before")
    @classmethod
    def __manifolds_validate(
        cls: type[VacuumBase],
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

    def assert_options(
        self: VacuumBase,
        layout_item: layout_item.CoverablePlate | layout_item.Plate,
        pressure: None | float = None,
    ) -> None:
        """TODO

        Must called before calling ...

        If any exceptions are thrown then you are trying to use an incompatible device.

        Raises ExceptionGroup of the following:

        """

    @abstractmethod
    def set_vacuum_pressure(self: VacuumBase, pressure: float) -> None:
        """Turns the vacuum on at the specified absolute pressure."""
        ...

    @abstractmethod
    def get_vacuum_pressure(self: VacuumBase) -> float:
        """Get the current absolute pressure."""
        ...
