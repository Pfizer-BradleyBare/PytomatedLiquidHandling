from __future__ import annotations

from .hamilton_vacuum import HamiltonVacuum
from .vacuum_base import DefaultVacuumPressures, FilterPlateConfiguration, VacuumBase

__all__ = [
    "VacuumBase",
    "FilterPlateConfiguration",
    "DefaultVacuumPressures",
    "HamiltonVacuum",
]

identifier = str
devices: dict[identifier, VacuumBase] = {}
