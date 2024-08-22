from __future__ import annotations

from abc import abstractmethod
from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.implementation import layout_item
from plh.implementation.tools import Resource


@dataclasses.dataclass(kw_only=True)
class FilterPlateConfiguration:
    """Compatibilities with a certain vacuum filter plate."""

    filter_plate: Annotated[
        layout_item.FilterPlateBase | layout_item.CoverableFilterPlateBase,
        BeforeValidator(layout_item.validate_instance),
    ]
    """The filter plate."""

    collection_plate: layout_item.PlateBase
    """The compatible plate for eluate collection."""

    max_pressure: float
    """The max pressure of the filter plate. Typically this the pressure at which you have filter flex occuring and airflow skyrockets."""

    default_pressure_low: float
    """Slow flow of liquid through the filter plate."""

    default_pressure_medium: float
    """Average flow of liquid through the filter plate."""

    default_pressure_high: float
    """Fast flow of liquid through the filter plate."""


@dataclasses.dataclass(kw_only=True, eq=False)
class VacuumBase(Resource):
    """Describes an on deck vacuum device."""

    manifold_park: Annotated[
        layout_item.VacuumManifoldBase,
        BeforeValidator(layout_item.validate_instance),
    ]
    """Park position for the vacuum manifold."""

    manifold_processing: Annotated[
        layout_item.VacuumManifoldBase,
        BeforeValidator(layout_item.validate_instance),
    ]
    """Vacuum position for the vacuum manifold."""

    filter_plate_configurations: dict[str, FilterPlateConfiguration]
    """Operational configurations for each filter plate supported by the vacuum device."""

    def assert_options(
        self: VacuumBase,
        layout_item: layout_item.CoverablePlateBase | layout_item.PlateBase,
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
