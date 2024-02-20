from __future__ import annotations

from abc import abstractmethod
from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.hal import layout_item
from plh.hal.tools import HALDevice, Interface

from .filter_plate_configuration import FilterPlateConfiguration


@dataclasses.dataclass(kw_only=True, eq=False)
class VacuumBase(Interface, HALDevice):
    """Describes an on deck vacuum device."""

    manifold_park: Annotated[
        layout_item.VacuumManifold, BeforeValidator(layout_item.validate_instance)
    ]
    """Park position for the vacuum manifold."""

    manifold_processing: Annotated[
        layout_item.VacuumManifold, BeforeValidator(layout_item.validate_instance)
    ]
    """Vacuum position for the vacuum manifold."""

    filter_plate_configurations: dict[str, FilterPlateConfiguration]
    """Operational configurations for each filter plate supported by the vacuum device."""

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
