from PytomatedLiquidHandling.Driver.Hamilton import Backend

from .Base import VacuumABC


class HamiltonVacuum(VacuumABC):
    Backend: Backend.HamiltonBackendABC
