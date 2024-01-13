import dataclasses

from ...Backend import HamiltonResponseABC


@dataclasses.dataclass(kw_only=True)
class Response(HamiltonResponseABC):
    FailedLabwareIDs: list[str]
