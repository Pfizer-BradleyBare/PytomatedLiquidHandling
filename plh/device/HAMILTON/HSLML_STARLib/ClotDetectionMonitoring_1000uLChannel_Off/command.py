import dataclasses

from plh.device.HAMILTON.backend import HamiltonCommandActionBase


@dataclasses.dataclass(kw_only=True)
class Command(HamiltonCommandActionBase): ...
