from pydantic import dataclasses

from ...Backend import HamiltonResponseABC


@dataclasses.dataclass(kw_only=True)
class Response(HamiltonResponseABC):
    HandleID: int
