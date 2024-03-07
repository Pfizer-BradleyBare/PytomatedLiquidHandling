from __future__ import annotations

import dataclasses

from plh.driver.HAMILTON.backend import HamiltonResponseBase


@dataclasses.dataclass(kw_only=True)
class Response(HamiltonResponseBase):
    mLVolumes: list[float]
    uLVolumes: list[float] = dataclasses.field(init=False)

    def __post_init__(self: Response) -> None:
        HamiltonResponseBase.__post_init__(self)

        self.uLVolumes = [v * 1000 for v in self.mLVolumes]
