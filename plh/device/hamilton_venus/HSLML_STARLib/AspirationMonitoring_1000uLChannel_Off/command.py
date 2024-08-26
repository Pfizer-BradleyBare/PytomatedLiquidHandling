import dataclasses

from plh.device.hamilton_venus.backend import HamiltonCommandActionBase


@dataclasses.dataclass(kw_only=True)
class Command(HamiltonCommandActionBase): ...
