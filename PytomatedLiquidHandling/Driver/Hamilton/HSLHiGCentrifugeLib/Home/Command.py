from dataclasses import dataclass

from ...Backend import HamiltonActionCommandABC


@dataclass(kw_only=True)
class Command(HamiltonActionCommandABC):
    ...
