import dataclasses

from plh.hamilton_venus.backend import HamiltonCommandStateBase


@dataclasses.dataclass(kw_only=True)
class Command(HamiltonCommandStateBase): ...
