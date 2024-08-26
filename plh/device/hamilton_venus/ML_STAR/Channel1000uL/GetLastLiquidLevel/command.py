import dataclasses

from plh.device.hamilton_venus.backend import HamiltonCommandStateBase


@dataclasses.dataclass(kw_only=True)
class Command(HamiltonCommandStateBase): ...
