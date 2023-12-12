from PytomatedLiquidHandling.Driver.Hamilton import Backend

from .Base import VacuumABC

from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class HamiltonVacuum(VacuumABC):
    Backend: Backend.HamiltonBackendABC
