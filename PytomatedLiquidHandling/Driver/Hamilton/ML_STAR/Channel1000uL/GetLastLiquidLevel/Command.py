from dataclasses import dataclass

from ....Backend import HamiltonStateCommandABC


@dataclass(kw_only=True)
class Command(HamiltonStateCommandABC):
    ...
