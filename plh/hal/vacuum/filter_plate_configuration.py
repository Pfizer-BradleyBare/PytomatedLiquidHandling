from __future__ import annotations

from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.hal import layout_item


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
