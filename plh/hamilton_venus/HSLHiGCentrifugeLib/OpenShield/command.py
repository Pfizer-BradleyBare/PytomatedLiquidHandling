import dataclasses

from plh.hamilton_venus.backend import HamiltonCommandActionBase
from plh.tools import CommandOptionsMixin

from .options import Options


@dataclasses.dataclass(kw_only=True)
class Command(HamiltonCommandActionBase, CommandOptionsMixin[Options]): ...
