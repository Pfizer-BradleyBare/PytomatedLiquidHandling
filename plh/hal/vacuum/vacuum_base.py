from __future__ import annotations

from abc import abstractmethod
from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.hal import layout_item
from plh.hal.tools import HALDevice, Interface


@dataclasses.dataclass(kw_only=True)
class DefaultVacuumPressures:
    """Facilitates simple selection of vacuum pressures. Each filter plate has "ideal" pressures.
    NOTE: This is subjective.
    """

    low: float
    """Slow flow of liquid through the filter plate."""

    medium: float
    """Average flow of liquid through the filter plate."""

    high: float
    """Fast flow of liquid through the filter plate."""


@dataclasses.dataclass(kw_only=True)
class FilterPlateConfiguration:
    """Compatibilities with a certain vacuum filter plate."""

    filter_plate: Annotated[
        layout_item.FilterPlate | layout_item.CoverableFilterPlate,
        BeforeValidator(layout_item.validate_instance),
    ]
    """The filter plate."""

    collection_plate: layout_item.Plate
    """The compatible plate for eluate collection."""

    max_pressure: float
    """The max pressure of the filter plate. Typically this the pressure at which you have filter flex occuring and airflow skyrockets."""

    default_vacuum_pressures: DefaultVacuumPressures
    """Default vacuum pressures object."""


@dataclasses.dataclass(kw_only=True, eq=False)
class VacuumBase(Interface, HALDevice):
    """Describes an on deck vacuum device."""

    manifold_park: Annotated[
        layout_item.VacuumManifold,
        BeforeValidator(layout_item.validate_instance),
    ]
    """Park position for the vacuum manifold."""

    manifold_processing: Annotated[
        layout_item.VacuumManifold,
        BeforeValidator(layout_item.validate_instance),
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
