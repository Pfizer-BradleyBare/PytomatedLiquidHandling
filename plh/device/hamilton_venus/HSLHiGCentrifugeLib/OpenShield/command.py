import dataclasses

from plh.device.hamilton_venus.backend import HamiltonCommandActionBase
from plh.device.tools import CommandOptionsMixin

from .options import Options


@dataclasses.dataclass(kw_only=True)
class Command(HamiltonCommandActionBase, CommandOptionsMixin[Options]): ...
