from __future__ import annotations

import dataclasses

from plh.device.UnchainedLabs_Instruments.backend import UnchainedLabsResponseBase


@dataclasses.dataclass(kw_only=True)
class Response(UnchainedLabsResponseBase):
    defined_plate_ids: list[str]
