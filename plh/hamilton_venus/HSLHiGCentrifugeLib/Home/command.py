import dataclasses

from plh.hamilton_venus.backend import HamiltonCommandActionBase


@dataclasses.dataclass(kw_only=True)
class Command(HamiltonCommandActionBase): ...
