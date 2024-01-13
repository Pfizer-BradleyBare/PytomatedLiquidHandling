import dataclasses

from ....Backend import HamiltonStateCommandABC


@dataclasses.dataclass(kw_only=True)
class Command(HamiltonStateCommandABC):
    ...
