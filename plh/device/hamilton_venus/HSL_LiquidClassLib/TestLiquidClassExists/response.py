import dataclasses

from plh.device.hamilton_venus.backend import HamiltonResponseBase


@dataclasses.dataclass(kw_only=True)
class Response(HamiltonResponseBase):
    BadLiquidClasses: list[str]
