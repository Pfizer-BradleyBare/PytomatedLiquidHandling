import dataclasses

from plh.device.HAMILTON.backend import HamiltonCommandStateBase


@dataclasses.dataclass(kw_only=True)
class Command(HamiltonCommandStateBase): ...
