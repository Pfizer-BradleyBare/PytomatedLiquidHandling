import dataclasses

from plh.device.hamilton_venus.backend import HamiltonCommandStateBase
from plh.device.tools import CommandOptionsListMixin

from .options import Options


@dataclasses.dataclass(kw_only=True)
class Command(CommandOptionsListMixin[list[Options]], HamiltonCommandStateBase): ...
