import dataclasses

from plh.driver.HAMILTON.backend import HamiltonResponseBase


@dataclasses.dataclass(kw_only=True)
class Response(HamiltonResponseBase):
    IsSpinning: bool
