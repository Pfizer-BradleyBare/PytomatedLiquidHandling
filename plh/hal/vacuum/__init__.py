from __future__ import annotations

from .filter_plate_configuration import DefaultVacuumPressures, FilterPlateConfiguration
from .hamilton_vacuum import HamiltonVacuum
from .vacuum_base import VacuumBase

__all__ = [
    "VacuumBase",
    "FilterPlateConfiguration",
    "DefaultVacuumPressures",
    "HamiltonVacuum",
]

identifier = str
devices: dict[identifier, VacuumBase] = {}
