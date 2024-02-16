from dataclasses import field

from pydantic import dataclasses

from plh.driver.HAMILTON.backend import HamiltonBackendBase

from .vacuum_base import VacuumBase


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonVacuum(VacuumBase):
    """Hamilton vacuubrand pump device."""

    backend: HamiltonBackendBase
    """Only Hamilton backends."""

    com_port: str
    """Port to connect. "COM4"."""

    handle_id: int = field(init=False, default=0)
    """The handle to use for all actions post connection."""
