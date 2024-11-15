from __future__ import annotations

import dataclasses

from plh.hamilton_venus.backend import HamiltonResponseBase


@dataclasses.dataclass(kw_only=True)
class Response(HamiltonResponseBase):
    SelectedPositions: list[str]
