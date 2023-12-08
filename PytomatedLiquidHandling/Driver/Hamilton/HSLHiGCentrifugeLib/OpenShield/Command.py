from pydantic import dataclasses

from ...Backend import HamiltonActionCommandABC


@dataclasses.dataclass(kw_only=True)
class Command(HamiltonActionCommandABC):
    ...
