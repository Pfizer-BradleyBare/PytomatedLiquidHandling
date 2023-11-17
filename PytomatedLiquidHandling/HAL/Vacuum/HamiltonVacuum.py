from PytomatedLiquidHandling.Driver.Hamilton.Backend import HamiltonBackendABC

from .Base import VacuumABC


class HamiltonVacuum(VacuumABC):
    Backend: HamiltonBackendABC
