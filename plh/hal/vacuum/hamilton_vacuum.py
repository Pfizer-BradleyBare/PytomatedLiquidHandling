from pydantic import dataclasses

from plh.driver.HAMILTON.backend import HamiltonBackendBase

from .vacuum_base import VacuumBase


@dataclasses.dataclass(kw_only=True)
class HamiltonVacuum(VacuumBase):
    backend: HamiltonBackendBase
