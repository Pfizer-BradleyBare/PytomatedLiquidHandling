from pydantic import dataclasses

from PytomatedLiquidHandling.Driver.Hamilton import Backend

from .Base import VacuumABC


@dataclasses.dataclass(kw_only=True)
class HamiltonVacuum(VacuumABC):
    Backend: Backend.HamiltonBackendABC
