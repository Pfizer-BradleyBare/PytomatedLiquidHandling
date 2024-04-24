from __future__ import annotations

import dataclasses

from plh.device.HAMILTON.backend import HamiltonResponseBase


@dataclasses.dataclass(kw_only=True)
class Response(HamiltonResponseBase):
    SelectedPositions: list[str]
