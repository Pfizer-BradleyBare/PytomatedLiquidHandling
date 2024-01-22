from dataclasses import field

from pydantic import dataclasses

from plh.driver.HAMILTON.backend import HamiltonBackendBase

from .vacuum_base import VacuumBase


@dataclasses.dataclass(kw_only=True)
class HamiltonVacuum(VacuumBase):
    com_port: str
    backend: HamiltonBackendBase
    handle_id: int = field(init=False, default=0)
