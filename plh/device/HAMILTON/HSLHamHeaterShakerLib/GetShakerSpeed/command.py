import dataclasses

from plh.device.HAMILTON.backend import HamiltonCommandStateBase
from plh.device.tools import CommandOptionsMixin

from .options import Options


@dataclasses.dataclass(kw_only=True)
class Command(CommandOptionsMixin[Options], HamiltonCommandStateBase): ...
