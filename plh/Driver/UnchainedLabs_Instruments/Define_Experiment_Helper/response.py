from __future__ import annotations

import dataclasses

from plh.driver.UnchainedLabs.backend import UnchainedLabsResponseBase


@dataclasses.dataclass(kw_only=True)
class Response(UnchainedLabsResponseBase):
    experiment_definition: str
    sample_definitiion: str
