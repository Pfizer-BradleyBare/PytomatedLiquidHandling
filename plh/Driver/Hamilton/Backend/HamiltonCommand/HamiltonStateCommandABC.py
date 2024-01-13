import dataclasses

from .HamiltonCommandABC import HamiltonCommandABC


@dataclasses.dataclass(kw_only=True)
class HamiltonStateCommandABC(HamiltonCommandABC):
    ...
